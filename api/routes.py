# api/routes.py
from __future__ import annotations

import json
import os
import asyncio
from typing import Annotated, FrozenSet

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel

from adapters.instruqt_graphql import list_tracks, create_invite
from core.config import settings
from core.logging import logger

from openai import AsyncOpenAI, RateLimitError


# ────────────────────────────────────────────────
# ───────────────  Auth helper  ──────────────────
# ────────────────────────────────────────────────
def verify_api_key(
    authorization: Annotated[str | None, Header()] = None,
) -> None:
    """
    Require `Authorization: Bearer <router_api_key>`.

    If the header is wrong (or missing) we raise 401.
    """
    expected = f"Bearer {settings.router_api_key}"
    logger.debug("Authorization seen: %r  | expected: %r", authorization, expected)

    if authorization != expected:
        raise HTTPException(status_code=401, detail="Invalid API key")


# ────────────────────────────────────────────────
# ───────────────  OpenAI setup  ────────────────
# ────────────────────────────────────────────────
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


# ────────────────────────────────────────────────
# ───────────────  Pydantic models  ──────────────
# ────────────────────────────────────────────────
class TrackOut(BaseModel):
    id: str
    slug: str
    title: str | None = None
    description: str | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "track_0e4d...",
                "slug": "infoblox-threat-defense",
                "title": "Infoblox Threat Defense",
                "description": "Hands-on lab covering..."
            }
        }
    }


class InviteOut(BaseModel):
    slug: str
    invite_url: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "slug": "infoblox-threat-defense",
                "invite_url": "https://play.instruqt.com/infoblox/invite/abc123"
            }
        }
    }


class PromptIn(BaseModel):
    prompt: str


# ────────────────────────────────────────────────
# ───────────────  FastAPI router  ───────────────
# ────────────────────────────────────────────────
router = APIRouter()

# ---------- /tracks ----------
@router.get(
    "/tracks",
    summary="List all tracks visible to this token",
    operation_id="listTracks",
    response_model=list[TrackOut],
    dependencies=[Depends(verify_api_key)],
)
async def tracks():
    try:
        return await list_tracks()
    except Exception as exc:
        logger.error(f"/tracks error: {exc}")
        raise HTTPException(status_code=502, detail="Failed to list tracks")


# ---------- /invite ----------
@router.post(
    "/invite",
    dependencies=[Depends(verify_api_key)],
    response_model=InviteOut,
    summary="Create a fresh invite link for the given slug",
)
async def invite(slug: str):
    try:
        url = await create_invite(slug)
        return {"slug": slug, "invite_url": url}
    except Exception as exc:
        logger.error(f"/invite error: {exc}")
        raise HTTPException(status_code=502, detail=f"Invite creation failed: {exc}")


# ────────────────────────────────────────────────
# ───────────────  Prompt → slug  ────────────────
# ────────────────────────────────────────────────
_INTENT_MAP: dict[FrozenSet[str], str] = {
    frozenset({"uddi", "aws", "azure"}): "infoblox-uddi-ipam",
    frozenset({"dns"}): "infoblox-lab1",
}


async def gpt_choose_slug(prompt: str, tracks: list[dict]) -> str | None:
    """
    Last-chance fallback: ask GPT to pick the best slug from the menu.
    """
    menu = "\n".join(f"- {t['slug']}: {t['title']}" for t in tracks[:50])

    fn_spec = {
        "name": "choose_slug",
        "description": "Select the slug of the most relevant lab.",
        "parameters": {
            "type": "object",
            "properties": {"slug": {"type": "string"}},
            "required": ["slug"],
        },
    }

    try:
        resp = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You map prompts to lab slugs."},
                {
                    "role": "user",
                    "content": f"Prompt: {prompt}\n\nAvailable labs:\n{menu}",
                },
            ],
            functions=[fn_spec],
            function_call={"name": "choose_slug"},
        )
        # resp.choices[0].message.function_call.arguments is a JSON string
        return json.loads(resp.choices[0].message.function_call.arguments).get("slug")
    except RateLimitError:
        logger.warning("GPT quota exceeded; skipping fallback")
        return None


async def _slug_from_prompt(prompt: str) -> str | None:
    """Return the slug that best matches the prompt (or None)."""
    tokens = {w.lower() for w in prompt.split()}

    # 1) static map
    for keyset, slug in _INTENT_MAP.items():
        if keyset.issubset(tokens):
            return slug

    # 2) fuzzy title match
    tracks = await list_tracks()
    for t in tracks:
        if tokens.issubset(t["title"].lower().split()):
            return t["slug"]

    # 3) GPT fallback
    return await gpt_choose_slug(prompt, tracks)


# ---------- /resolve ----------
@router.post(
    "/resolve",
    dependencies=[Depends(verify_api_key)],
    response_model=InviteOut,
    summary="Resolve a natural-language prompt into an invite link",
)
async def resolve(prompt_in: PromptIn):
    slug = await _slug_from_prompt(prompt_in.prompt)
    if not slug:
        raise HTTPException(status_code=404, detail="No matching lab")

    url = await create_invite(slug)
    return {"slug": slug, "invite_url": url}
