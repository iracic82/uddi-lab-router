# app.py
from __future__ import annotations

import time
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from starlette.middleware.base import BaseHTTPMiddleware

from core.logging import logger
from api.routes import router
from core.config import settings   # ← already exists in your repo


# ──────────────────────────────
# Logging
# ──────────────────────────────
class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response: Response = await call_next(request)
        logger.info(
            {
                "client": request.client.host,
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "duration_ms": round((time.time() - start) * 1000, 2),
            }
        )
        return response


# ──────────────────────────────
# Factory
# ──────────────────────────────
def create_app() -> FastAPI:
    app = FastAPI(
        title="Instruqt Lab Router",
        description=(
            "Maps natural-language prompts to Instruqt labs and returns one-click "
            "invite links."
        ),
        version="0.3.0",
        docs_url=None,       # disable vanilla Swagger
        redoc_url=None,
        swagger_ui_parameters={
            "tryItOutEnabled": True,
            "persistAuthorization": True,
            "defaultModelsExpandDepth": -1,
            # auto-inject Bearer token so people can click “Try it out”
            "requestInterceptor": (
                f"(req) => {{req.headers['Authorization'] = "
                f"'Bearer {settings.router_api_key}'; return req;}}"
            ),
        },
    )

    # ─── Core plumbing ──────────────────────────────────────────────
    app.add_middleware(LogMiddleware)
    app.include_router(router)

    # 1️⃣  Static – compiled React bundle + assets
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")

    @app.get("/", include_in_schema=False)
    async def spa_index() -> FileResponse:
        return FileResponse("static/index.html")

    # 2️⃣  Swagger UI (dark-/light-mode aware)
    @app.get("/docs", include_in_schema=False)
    async def swagger_docs() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=f"{app.title} • Docs",
            swagger_favicon_url="/static/logo32.png",
            swagger_css_url="/static/swagger.css",      # optional – theme file
            swagger_ui_parameters=app.swagger_ui_parameters,
        )

    # 2️⃣½ ReDoc two-pane “Portal” – Infoblox WAPI look-and-feel
    @app.get("/portal", include_in_schema=False)
    @app.get("/portal", include_in_schema=False)
    async def redoc_portal() -> HTMLResponse:
        return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} – ReDoc",
        # (optional) point to a custom JS bundle
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
    )

    # 3️⃣  Health-check for load-balancers / Docker
    @app.get("/health", include_in_schema=False)
    async def health():
        return {"status": "ok"}

    # 4️⃣  Global error handler
    @app.exception_handler(Exception)
    async def global_exc(_: Request, exc: Exception):
        logger.error("Unhandled exception", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={"error": {"type": exc.__class__.__name__, "detail": str(exc)}},
        )

    return app


# For `uvicorn main:api`
api = create_app()