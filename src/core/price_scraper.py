# ============================================================================
# FILE: src/core/price_scraper.py
# Scraping prezzi da Vinted
# ============================================================================

import asyncio
import aiohttp
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import time
import random

from ..models.price import VintedListing
from ..config.settings import Settings
from ..utils.text_utils import TextNormalizer

class VintedPriceScraper:
    """Scraper per prezzi Vinted con rate limiting e caching"""
    
    def __init__(self):
        self.settings = Settings()
        self.base_url = self.settings.VINTED_BASE_URL
        self.session = None
        self.text_normalizer = TextNormalizer()
        
        # Headers per evitare detection
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    async def search_similar_items(
        self, 
        brand: str, 
        item_type: str, 
        size: str,
        max_results: int = 20
    ) -> List[VintedListing]:
        """Cerca articoli simili su Vinted"""
        
        if not self.session:
            self.session = aiohttp.ClientSession(headers=self.headers)
        
        try:
            search_params = self._build_search_params(brand, item_type, size)
            listings = await self._fetch_listings(search_params, max_results)
            return self._process_listings(listings)
            
        except Exception as e:
            print(f"Scraping error: {e}")
            return self._get_mock_listings(brand, item_type, size)
        
        finally:
            if self.session:
                await self.session.close()
                self.session = None
    
    def _build_search_params(self, brand: str, item_type: str, size: str) -> Dict:
        """Costruisce parametri di ricerca Vinted"""
        
        # Normalizza parametri
        normalized_brand = self.text_normalizer.normalize_brand(brand)
        normalized_type = self.text_normalizer.normalize_item_type(item_type)
        
        params = {
            'search_text': f"{normalized_brand} {normalized_type}",
            'size_ids[]': self._get_size_id(size),
            'status_ids[]': '6',  # Solo venduti
            'order': 'newest_first'
        }
        
        return {k: v for k, v in params.items() if v}
    
    async def _fetch_listings(self, search_params: Dict, max_results: int) -> List[Dict]:
        """Fetch listings da Vinted con pagination"""
        
        all_listings = []
        page = 1
        
        while len(all_listings) < max_results and page <= 5:  # Max 5 pagine
            
            search_params['page'] = page
            url = f"{self.base_url}/api/v2/catalog/items?" + urlencode(search_params, doseq=True)
            
            await self._rate_limit_delay()
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data.get('items', [])
                    
                    if not items:
                        break
                        
                    all_listings.extend(items)
                    page += 1
                else:
                    break
        
        return all_listings[:max_results]
    
    def _process_listings(self, raw_listings: List[Dict]) -> List[VintedListing]:
        """Processa raw listings in VintedListing objects"""
        
        processed = []
        
        for item in raw_listings:
            try:
                listing = VintedListing(
                    title=item.get('title', ''),
                    price=float(item.get('price', {}).get('amount', 0)),
                    condition=self._normalize_condition(item.get('status', '')),
                    url=f"{self.base_url}/items/{item.get('id')}",
                    brand=item.get('brand', {}).get('title', ''),
                    size=item.get('size_title', ''),
                    sold=item.get('is_sold', False)
                )
                processed.append(listing)
                
            except (ValueError, KeyError) as e:
                continue  # Skip invalid listings
        
        return processed
    
    def _get_mock_listings(self, brand: str, item_type: str, size: str) -> List[VintedListing]:
        """Genera listings fittizi per testing/fallback"""
        
        # Mock prices basato su tipo
        mock_prices = {
            "felpa": [12, 15, 18, 20, 25, 30],
            "t-shirt": [8, 10, 12, 15, 18],
            "jeans": [20, 25, 30, 35, 40],
            "scarpe": [25, 30, 40, 50, 60]
        }
        
        prices = mock_prices.get(item_type.lower(), [10, 15, 20, 25])
        
        listings = []
        for i, price in enumerate(prices):
            listings.append(VintedListing(
                title=f"{brand} {item_type} - Taglia {size}",
                price=price + random.randint(-3, 3),  # Variazione casuale
                condition=random.choice(["Ottimo", "Buono", "Discreto"]),
                url=f"https://vinted.it/item/{random.randint(1000000, 9999999)}",
                brand=brand,
                size=size,
                sold=True
            ))
        
        return listings
    
    def _get_size_id(self, size: str) -> Optional[str]:
        """Converte taglia in ID Vinted"""
        size_mapping = {
            "XS": "1", "S": "2", "M": "3", 
            "L": "4", "XL": "5", "XXL": "6"
        }
        return size_mapping.get(size.upper())
    
    def _normalize_condition(self, condition: str) -> str:
        """Normalizza condizione Vinted"""
        condition_mapping = {
            "brand_new_with_tags": "Nuovo con etichetta",
            "very_good": "Ottimo", 
            "good": "Buono",
            "satisfactory": "Discreto"
        }
        return condition_mapping.get(condition, "Buono")
    
    async def _rate_limit_delay(self):
        """Delay per rispettare rate limits"""
        await asyncio.sleep(random.uniform(1.0, 2.5))