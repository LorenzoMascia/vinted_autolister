# ============================================================================
# FILE: src/core/content_generator.py
# Generazione contenuti AI
# ============================================================================

import json
import re
from typing import Optional, Dict, Any
from ..models.product import ProductData
from ..models.listing import ListingData
from ..services.openai_service import OpenAIService
from ..utils.text_utils import TextValidator
from ..config.settings import Settings

class ContentGenerator:
    """Genera titoli e descrizioni ottimizzate per Vinted"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.openai_service = OpenAIService(api_key) if api_key else None
        self.text_validator = TextValidator()
        self.settings = Settings()
    
    def generate_listing_content(
        self,
        product_data: ProductData,
        size: str,
        condition: str,
        price: float,
        style: str = "friendly"
    ) -> Dict[str, str]:
        """Genera titolo e descrizione per il listing"""
        
        if self.openai_service:
            return self._generate_with_ai(product_data, size, condition, price, style)
        else:
            return self._generate_with_templates(product_data, size, condition, price, style)
    
    def _generate_with_ai(
        self,
        product_data: ProductData,
        size: str, 
        condition: str,
        price: float,
        style: str
    ) -> Dict[str, str]:
        """Genera contenuto usando OpenAI"""
        
        prompt = self._build_generation_prompt(product_data, size, condition, price, style)
        
        try:
            response = self.openai_service.text_completion(
                prompt=prompt,
                max_tokens=self.settings.TEXT_MAX_TOKENS,
                temperature=0.7
            )
            
            content = self._parse_ai_response(response)
            
            # Validazione e cleanup
            content = self._validate_and_clean_content(content)
            
            return content
            
        except Exception as e:
            print(f"AI generation failed: {e}")
            return self._generate_with_templates(product_data, size, condition, price, style)
    
    def _build_generation_prompt(
        self,
        product_data: ProductData,
        size: str,
        condition: str, 
        price: float,
        style: str
    ) -> str:
        """Costruisce prompt ottimizzato per generazione contenuti"""
        
        style_instructions = {
            "friendly": "Usa un tono amichevole e caloroso, come se stessi parlando a un amico",
            "professional": "Mantieni un tono professionale ma accessibile",
            "trendy": "Usa un linguaggio moderno e alla moda, con emoji appropriate"
        }
        
        features_text = ""
        if product_data.additional_features:
            features_text = f"Caratteristiche aggiuntive: {product_data.additional_features}"
        
        return f"""
        Genera un titolo e una descrizione per un annuncio Vinted in italiano.
        
        DATI PRODOTTO:
        - Marca: {product_data.brand}
        - Tipo: {product_data.type.value}
        - Colore: {product_data.color}
        - Materiale: {product_data.material}
        - Taglia: {size}
        - Condizione: {condition}
        - Prezzo: {price}€
        {features_text}
        
        STILE: {style_instructions.get(style, style_instructions["friendly"])}
        
        REQUISITI:
        - Titolo: massimo 60 caratteri, accattivante e informativo
        - Descrizione: 150-250 parole, include dettagli utili e call-to-action
        - Includi hashtag rilevanti
        - Evidenzia punti di forza del capo
        - Invita al contatto per domande
        
        Restituisci SOLO un JSON valido:
        {{
          "title": "titolo qui",
          "description": "descrizione completa qui"
        }}
        """
    
    def _parse_ai_response(self, response: dict) -> Dict[str, str]:
        """Parsa risposta AI ed estrae contenuto"""
        
        try:
            content = response['choices'][0]['message']['content']
            
            # Cerca JSON nella risposta
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return {
                    "title": data.get("title", ""),
                    "description": data.get("description", "")
                }
            else:
                raise ValueError("No JSON found in AI response")
                
        except (json.JSONDecodeError, KeyError, ValueError):
            raise ContentGenerationError("Failed to parse AI response")
    
    def _generate_with_templates(
        self,
        product_data: ProductData,
        size: str,
        condition: str,
        price: float,
        style: str
    ) -> Dict[str, str]:
        """Genera contenuto usando template predefiniti"""
        
        # Template per titoli
        title_templates = [
            f"{product_data.brand} {product_data.type.value} {product_data.color} - Taglia {size}",
            f"{product_data.type.value.title()} {product_data.brand} taglia {size} - {condition}",
            f"✨ {product_data.brand} {product_data.type.value} {product_data.color} T.{size}"
        ]
        
        # Seleziona titolo che rispetta limite caratteri
        title = next((t for t in title_templates if len(t) <= 60), title_templates[0][:60])
        
        # Template descrizione basato su stile
        if style == "trendy":
            description = self._generate_trendy_description(product_data, size, condition, price)
        elif style == "professional":
            description = self._generate_professional_description(product_data, size, condition, price)
        else:
            description = self._generate_friendly_description(product_data, size, condition, price)
        
        return {"title": title, "description": description}
    
    def _generate_friendly_description(
        self, product_data: ProductData, size: str, condition: str, price: float
    ) -> str:
        """Template descrizione amichevole"""
        
        return f"""Ciao! Vendo questo bellissimo {product_data.type.value.lower()} {product_data.brand} 😊

📏 Taglia: {size}
🎨 Colore: {product_data.color}
🧵 Materiale: {product_data.material}
✨ Condizione: {condition}

Il capo è stato curato con amore e si presenta in ottime condizioni! Perfetto per arricchire il tuo guardaroba con un tocco di stile.

💰 Prezzo: {price}€ (trattabile per acquisti multipli!)
📦 Spedizione veloce e imballaggio accurato
💬 Contattami pure per foto aggiuntive o qualsiasi domanda!

#vinted #abbigliamento #secondamano #sostenibile #{product_data.brand.lower()} #{product_data.type.value.replace('-', '')}"""
    
    def _generate_professional_description(
        self, product_data: ProductData, size: str, condition: str, price: float
    ) -> str:
        """Template descrizione professionale"""
        
        return f"""In vendita {product_data.type.value.lower()} {product_data.brand} in {condition.lower()}.

DETTAGLI PRODOTTO:
• Marca: {product_data.brand}
• Tipo: {product_data.type.value}
• Taglia: {size}
• Colore: {product_data.color}
• Materiale: {product_data.material}
• Condizione: {condition}

Il capo è stato conservato con cura e non presenta difetti evidenti. Ideale per chi cerca qualità a prezzo conveniente.

CONDIZIONI DI VENDITA:
• Prezzo: {price}€
• Spedizione: disponibile con tracking
• Pagamento: solo tramite piattaforma Vinted
• Restituzione: secondo policy Vinted

Per ulteriori informazioni o foto aggiuntive, non esitate a contattarmi.

#abbigliamento #preloved #{product_data.brand.lower()}"""
    
    def _generate_trendy_description(
        self, product_data: ProductData, size: str, condition: str, price: float
    ) -> str:
        """Template descrizione trendy"""
        
        return f"""🔥 SUPER FIND 🔥

{product_data.type.value.title()} {product_data.brand} che non può mancare nel tuo closet! 💅

✨ SPECS:
📐 Size: {size}
🌈 Color: {product_data.color}
🔗 Material: {product_data.material}
💯 Condition: {condition}

Questo piece è davvero special e ti darà quel look che stavi cercando! Perfect per ogni occasion 🌟

💸 Price: {price}€ 
📲 DM me per più info!
🚚 Fast shipping guaranteed

#vintedfinds #thrifted #sustainable #fashion #{product_data.brand.lower()} #ootd #preloved"""
    
    def _validate_and_clean_content(self, content: Dict[str, str]) -> Dict[str, str]:
        """Valida e pulisce contenuto generato"""
        
        # Valida titolo
        title = content.get("title", "").strip()
        if len(title) > 60:
            title = title[:57] + "..."
        
        # Valida descrizione
        description = content.get("description", "").strip()
        if len(description) > 2000:  # Limite Vinted
            description = description[:1997] + "..."
        
        # Remove caratteri problematici
        title = self.text_validator.clean_text(title)
        description = self.text_validator.clean_text(description)
        
        return {"title": title, "description": description}

class ContentGenerationError(Exception):
    """Errore nella generazione contenuti"""
    pass