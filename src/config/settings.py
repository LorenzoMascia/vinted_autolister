# ============================================================================
# FILE: src/config/settings.py
# Configurazioni e costanti
# ============================================================================

from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Configurazioni applicazione"""
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_VISION_MODEL: str = "gpt-4-vision-preview"
    OPENAI_TEXT_MODEL: str = "gpt-4"
    VISION_MAX_TOKENS: int = 300
    TEXT_MAX_TOKENS: int = 500
    
    # Vinted
    VINTED_BASE_URL: str = "https://www.vinted.it"
    VINTED_API_TIMEOUT: int = 30
    VINTED_MAX_RETRIES: int = 3
    
    # Pricing
    CONDITION_MULTIPLIERS: dict = {
        "Nuovo con etichetta": 1.2,
        "Ottimo": 1.0,
        "Buono": 0.85,
        "Discreto": 0.7,
        "Rovinato": 0.5
    }
    
    # Performance
    MAX_IMAGE_SIZE: int = 1024  # px
    IMAGE_QUALITY: int = 85  # %
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"