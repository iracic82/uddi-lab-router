from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    instruqt_api_token: str
    instruqt_api_url: str = "https://play.instruqt.com/graphql"
    instruqt_team_slug: str
    
    openai_api_key: str | None = None      # ← NEW LINE
    router_api_key: str | None = None  

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

settings = Settings()
print(f"Router API key: {settings.router_api_key!r}")
