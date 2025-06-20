# ============================================================================
# FILE: src/services/openai_service.py
# Wrapper per OpenAI API
# ============================================================================

import openai
from typing import Optional, Dict, Any
import asyncio
from ..config.settings import Settings

class OpenAIService:
    """Service per interazioni con OpenAI API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.settings = Settings()
        if api_key:
            openai.api_key = api_key
            self.enabled = True
        else:
            self.enabled = False
    
    def vision_analyze(self, image_base64: str, prompt: str, max_tokens: int = 300) -> Dict[str, Any]:
        """Analizza immagine con GPT-4 Vision"""
        
        if not self.enabled:
            raise OpenAIServiceError("OpenAI API key not configured")
        
        try:
            response = openai.ChatCompletion.create(
                model=self.settings.OPENAI_VISION_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                            }
                        ]
                    }
                ],
                max_tokens=max_tokens,
                temperature=0.1
            )
            
            return response
            
        except Exception as e:
            raise OpenAIServiceError(f"Vision API call failed: {str(e)}")
    
    def text_completion(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> Dict[str, Any]:
        """Genera testo con GPT-4"""
        
        if not self.enabled:
            raise OpenAIServiceError("OpenAI API key not configured")
        
        try:
            response = openai.ChatCompletion.create(
                model=self.settings.OPENAI_TEXT_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response
            
        except Exception as e:
            raise OpenAIServiceError(f"Text completion failed: {str(e)}")

class OpenAIServiceError(Exception):
    """Errore OpenAI Service"""
    pass