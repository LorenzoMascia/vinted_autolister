# ============================================================================
# FILE: src/core/autolister.py
# Main orchestrator - coordina tutti i componenti
# ============================================================================

import time
from typing import Optional, Dict, Any
from pathlib import Path

from ..models.product import ProductData
from ..models.listing import ListingData, ListingResult
from ..models.price import PriceAnalysis
from .vision_analyzer import VisionAnalyzer
from .price_scraper import VintedPriceScraper
from .price_analyzer import PriceAnalyzer
from .content_generator import ContentGenerator

class VintedAutoLister:
    """Orchestrator principale per il processo di listing automatico"""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        self.vision_analyzer = VisionAnalyzer(openai_api_key)
        self.price_scraper = VintedPriceScraper()
        self.price_analyzer = PriceAnalyzer()
        self.content_generator = ContentGenerator(openai_api_key)
    
    async def process_image(
        self,
        image_path: str,
        size: str,
        condition: str,
        target_sale_speed: str = "normal",
        content_style: str = "friendly"
    ) -> ListingResult:
        """Processo completo: da immagine a listing pronto"""
        
        start_time = time.time()
        
        try:
            # 1. Analisi immagine
            print("🔍 Analyzing image...")
            image_data = self._load_image(image_path)
            product_data = self.vision_analyzer.analyze_image(image_data)
            
            # 2. Ricerca prezzi
            print("💰 Searching market prices...")
            similar_listings = await self.price_scraper.search_similar_items(
                brand=product_data.brand,
                item_type=product_data.type.value,
                size=size
            )
            
            # 3. Analisi prezzi
            print("📊 Analyzing price data...")
            price_analysis = self.price_analyzer.analyze_prices(
                listings=similar_listings,
                condition=condition,
                target_sale_speed=target_sale_speed
            )
            
            # 4. Generazione contenuti
            print("✍️ Generating content...")
            content = self.content_generator.generate_listing_content(
                product_data=product_data,
                size=size,
                condition=condition,
                price=price_analysis.suggested_price,
                style=content_style
            )
            
            # 5. Assembla risultato finale
            listing_data = ListingData(
                title=content["title"],
                description=content["description"],
                price=price_analysis.suggested_price,
                condition=condition,
                category=product_data.category,
                size=size,
                brand=product_data.brand,
                type=product_data.type.value,
                color=product_data.color
            )
            
            processing_time = time.time() - start_time
            
            # Calcola confidence score complessivo
            overall_confidence = self._calculate_overall_confidence(
                product_data.confidence_score,
                price_analysis.confidence_level,
                len(similar_listings)
            )
            
            result = ListingResult(
                listing=listing_data,
                product_data=product_data,
                market_analysis=price_analysis,
                generation_time=processing_time,
                confidence_score=overall_confidence
            )
            
            print(f"✅ Processing completed in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            print(f"❌ Error during processing: {str(e)}")
            raise AutoListerError(f"Processing failed: {str(e)}")
    
    def _load_image(self, image_path: str) -> bytes:
        """Carica immagine da file"""
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        return path.read_bytes()
    
    def _calculate_overall_confidence(
        self,
        vision_confidence: float,
        price_confidence: float, 
        market_data_points: int
    ) -> float:
        """Calcola confidence score complessivo"""
        
        # Weighted average con pesi basati su importanza
        weights = {
            'vision': 0.4,
            'price': 0.4, 
            'market_data': 0.2
        }
        
        # Normalizza market data points
        market_score = min(1.0, market_data_points / 20)
        
        overall = (
            vision_confidence * weights['vision'] +
            price_confidence * weights['price'] +
            market_score * weights['market_data']
        )
        
        return round(overall, 2)
    
    async def analyze_price_only(
        self,
        brand: str,
        item_type: str, 
        size: str,
        condition: str
    ) -> PriceAnalysis:
        """Solo analisi prezzi senza processare immagine"""
        
        similar_listings = await self.price_scraper.search_similar_items(
            brand=brand,
            item_type=item_type,
            size=size
        )
        
        return self.price_analyzer.analyze_prices(
            listings=similar_listings,
            condition=condition
        )

class AutoListerError(Exception):
    """Errore generico AutoLister"""
    pass
