# ============================================================================
# FILE: src/models/listing.py  
# Modelli per i listing generati
# ============================================================================

from dataclasses import dataclass
from typing import List, Optional
from .product import ProductData, Condition

@dataclass
class ListingData:
    """Dati del listing finale"""
    title: str
    description: str
    price: float
    condition: Condition
    category: str
    size: str
    brand: str
    type: str
    color: str
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

@dataclass 
class ListingResult:
    """Risultato completo del processo"""
    listing: ListingData
    product_data: ProductData
    market_analysis: 'PriceAnalysis'
    generation_time: float
    confidence_score: float