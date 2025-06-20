# ============================================================================
# FILE: src/models/price.py
# Modelli per analisi prezzi
# ============================================================================

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class VintedListing:
    """Singolo listing trovato su Vinted"""
    title: str
    price: float
    condition: str
    url: str
    brand: str
    size: str
    date_posted: Optional[datetime] = None  # Ora Optional è importato
    sold: bool = False
    
@dataclass
class PriceDistribution:
    """Distribuzione prezzi per un tipo di prodotto"""
    min_price: float
    max_price: float
    mean_price: float
    median_price: float
    mode_price: float
    std_dev: float
    quartiles: Dict[str, float]  # Q1, Q2, Q3

@dataclass
class PriceAnalysis:
    """Analisi completa dei prezzi"""
    suggested_price: float
    distribution: PriceDistribution
    total_listings: int
    price_range: str
    confidence_level: float
    market_position: str  # "low", "average", "high"
    analysis_summary: str