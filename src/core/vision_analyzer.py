# ============================================================================
# FILE: src/core/vision_analyzer.py
# Analisi immagini con OpenAI Vision
# ============================================================================

import json
import re
from typing import Optional
from PIL import Image
import io
import base64

from ..models.product import ProductData, ProductType
from ..services.openai_service import OpenAIService
from ..utils.image_utils import ImageProcessor
from ..config.settings import Settings

class VisionAnalyzer:
    """Analizza immagini di abbigliamento usando GPT-4 Vision"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.openai_service = OpenAIService(api_key)
        self.image_processor = ImageProcessor()
        self.settings = Settings()
    
    def analyze_image(self, image_data: bytes) -> ProductData:
        """Analizza immagine e ritorna dati strutturati del prodotto"""
        
        # Preprocessing immagine
        processed_image = self._preprocess_image(image_data)
        
        # Chiamata Vision API
        analysis_result = self._call_vision_api(processed_image)
        
        # Parsing e validazione risultato
        product_data = self._parse_vision_result(analysis_result)
        
        return product_data
    
    def _preprocess_image(self, image_data: bytes) -> bytes:
        """Preprocessa immagine per ottimizzare analisi"""
        image = Image.open(io.BytesIO(image_data))
        
        # Resize se troppo grande
        if image.width > 1024 or image.height > 1024:
            image = self.image_processor.resize_maintain_aspect(
                image, max_size=1024
            )
        
        # Ottimizzazione qualità
        image = self.image_processor.enhance_quality(image)
        
        # Converti a bytes
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=85)
        return buffer.getvalue()
    
    def _call_vision_api(self, image_data: bytes) -> dict:
        """Chiama OpenAI Vision API"""
        
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        prompt = self._get_analysis_prompt()
        
        try:
            response = self.openai_service.vision_analyze(
                image_base64=base64_image,
                prompt=prompt,
                max_tokens=self.settings.VISION_MAX_TOKENS
            )
            return response
            
        except Exception as e:
            raise VisionAnalysisError(f"Vision API error: {str(e)}")
    
    def _get_analysis_prompt(self) -> str:
        """Genera prompt ottimizzato per analisi prodotto"""
        return """
        Analizza questa immagine di un capo di abbigliamento.
        
        Restituisci SOLO un JSON valido con questi campi:
        {
          "brand": "nome del brand se visibile, altrimenti 'Sconosciuto'",
          "type": "tipo specifico (felpa, t-shirt, jeans, scarpe, giacca, camicia)",
          "color": "colore principale",
          "material": "materiale principale se identificabile",
          "category": "categoria Vinted appropriata",
          "confidence_score": "score 0-1 sulla sicurezza dell'analisi",
          "additional_features": {
            "pattern": "descrizione pattern/stampe se presenti",
            "style": "stile (casual, elegante, sportivo, etc)",
            "season": "stagione appropriata"
          }
        }
        
        Sii preciso e usa termini italiani standard.
        """
    
    def _parse_vision_result(self, api_response: dict) -> ProductData:
        """Parsa e valida risultato Vision API"""
        
        try:
            content = api_response['choices'][0]['message']['content']
            
            # Estrai JSON dalla risposta
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if not json_match:
                raise ValueError("No JSON found in response")
            
            data = json.loads(json_match.group())
            
            # Validazione e conversione
            product_type = self._normalize_product_type(data.get('type', 'abbigliamento'))
            
            return ProductData(
                brand=data.get('brand', 'Sconosciuto'),
                type=product_type,
                color=data.get('color', 'Vario'),
                material=data.get('material', 'Misto'),
                category=data.get('category', 'Abbigliamento'),
                confidence_score=float(data.get('confidence_score', 0.5)),
                additional_features=data.get('additional_features', {})
            )
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            # Fallback con dati di base
            return self._create_fallback_product_data()
    
    def _normalize_product_type(self, type_str: str) -> ProductType:
        """Normalizza tipo prodotto a enum"""
        type_mapping = {
            'felpa': ProductType.FELPA,
            'hoodie': ProductType.FELPA,
            't-shirt': ProductType.T_SHIRT,
            'maglietta': ProductType.T_SHIRT,
            'jeans': ProductType.JEANS,
            'scarpe': ProductType.SCARPE,
            'giacca': ProductType.GIACCA,
            'camicia': ProductType.CAMICIA
        }
        
        normalized = type_str.lower().strip()
        return type_mapping.get(normalized, ProductType.T_SHIRT)
    
    def _create_fallback_product_data(self) -> ProductData:
        """Crea dati fallback se Vision API fallisce"""
        return ProductData(
            brand="Da specificare",
            type=ProductType.T_SHIRT,
            color="Da specificare", 
            material="Misto",
            category="Abbigliamento",
            confidence_score=0.1
        )

class VisionAnalysisError(Exception):
    """Errore durante analisi Vision"""
    pass
