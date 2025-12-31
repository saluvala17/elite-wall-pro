"""
Frontend Configuration for Elite Wall Pro (Streamlit)
"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env explicitly for Streamlit
load_dotenv()


def normalize_url(url: str) -> str:
    """Remove trailing slash to avoid double-slash bugs"""
    return url.rstrip("/")


@dataclass(frozen=True)
class Settings:
    api_url: str = normalize_url(
        os.getenv("FRONTEND_API_URL", "http://localhost:8000")
    )
    app_name: str = "Elite Wall Pro"
    version: str = "2.0.0"


settings = Settings()
