# ============================================================================
# FILE: src/services/scraping_service.py
# Utilities per web scraping
# ============================================================================

import asyncio
import aiohttp
from typing import Optional, Dict, Any
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from utils.text_utils import TextNormalizer
from services.cache_service import CacheService

class ScrapingService:
    """Service per operazioni di scraping generiche"""
    
    def __init__(self):
        self.cache = CacheService()
        self.user_agent = UserAgent()
        self.text_normalizer = TextNormalizer()
    
    async def fetch_page(
        self, 
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Optional[str]:
        """Fetch pagina web con caching"""
        
        cache_key = {"url": url, "params": params}
        cached = self.cache.get(cache_key)
        if cached:
            return cached.get("content")
        
        default_headers = {
            "User-Agent": self.user_agent.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3"
        }
        
        final_headers = {**default_headers, **(headers or {})}
        
        try:
            async with aiohttp.ClientSession(headers=final_headers) as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        content = await response.text()
                        self.cache.set(cache_key, {"content": content})
                        return content
                    return None
        except Exception as e:
            print(f"Scraping error: {str(e)}")
            return None
    
    async def scrape_product_details(self, url: str) -> Optional[Dict[str, Any]]:
        """Scrape dettagli prodotto da pagina Vinted"""
        
        html = await self.fetch_page(url)
        if not html:
            return None
            
        soup = BeautifulSoup(html, 'html.parser')
        
        try:
            # Estrai dati da pagina prodotto
            title = soup.find("h1", {"class": "details-title"}).text.strip()
            price = float(soup.find("div", {"class": "price"}).text.replace("€", "").strip())
            description = soup.find("div", {"class": "description"}).text.strip()
            
            details = {}
            for row in soup.find_all("div", {"class": "details-list__item"}):
                key = row.find("div", {"class": "details-list__item-title"}).text.strip().lower()
                value = row.find("div", {"class": "details-list__item-value"}).text.strip()
                details[key] = value
            
            return {
                "title": title,
                "price": price,
                "description": description,
                "details": details
            }
        except Exception as e:
            print(f"Failed to parse product page: {str(e)}")
            return None