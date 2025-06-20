# ============================================================================
# FILE: src/core/price_analyzer.py
# Analisi statistiche dei prezzi
# ============================================================================

import statistics
from typing import List, Dict
from ..models.price import VintedListing, PriceDistribution, PriceAnalysis
from ..config.settings import Settings

class PriceAnalyzer:
    """Analizza prezzi e suggerisce pricing ottimale"""
    
    def __init__(self):
        self.settings = Settings()
    
    def analyze_prices(
        self, 
        listings: List[VintedListing], 
        condition: str,
        target_sale_speed: str = "normal"  # fast, normal, premium
    ) -> PriceAnalysis:
        """Analizza prezzi e genera raccomandazione"""
        
        if not listings:
            return self._create_fallback_analysis()
        
        # Filtra solo listings venduti con prezzo valido
        valid_listings = [l for l in listings if l.sold and l.price > 0]
        
        if not valid_listings:
            return self._create_fallback_analysis()
        
        prices = [listing.price for listing in valid_listings]
        
        # Calcola distribuzione
        distribution = self._calculate_distribution(prices)
        
        # Suggerisce prezzo basato su strategia
        suggested_price = self._calculate_suggested_price(
            distribution, condition, target_sale_speed
        )
        
        # Determina posizione nel mercato
        market_position = self._determine_market_position(suggested_price, distribution)
        
        # Genera analisi testuale
        analysis_summary = self._generate_analysis_summary(
            distribution, len(valid_listings), market_position
        )
        
        return PriceAnalysis(
            suggested_price=suggested_price,
            distribution=distribution,
            total_listings=len(valid_listings),
            price_range=f"{distribution.min_price}€ - {distribution.max_price}€",
            confidence_level=self._calculate_confidence(len(valid_listings)),
            market_position=market_position,
            analysis_summary=analysis_summary
        )
    
    def _calculate_distribution(self, prices: List[float]) -> PriceDistribution:
        """Calcola distribuzione statistica dei prezzi"""
        
        sorted_prices = sorted(prices)
        
        return PriceDistribution(
            min_price=min(prices),
            max_price=max(prices),
            mean_price=round(statistics.mean(prices), 2),
            median_price=statistics.median(prices),
            mode_price=statistics.mode(prices) if len(set(prices)) < len(prices) else statistics.median(prices),
            std_dev=round(statistics.stdev(prices) if len(prices) > 1 else 0, 2),
            quartiles={
                "Q1": sorted_prices[len(sorted_prices)//4],
                "Q2": statistics.median(prices),
                "Q3": sorted_prices[3*len(sorted_prices)//4]
            }
        )
    
    def _calculate_suggested_price(
        self, 
        distribution: PriceDistribution, 
        condition: str,
        target_sale_speed: str
    ) -> float:
        """Calcola prezzo suggerito basato su condizione e strategia"""
        
        # Base price (mediana è più robusta della media)
        base_price = distribution.median_price
        
        # Aggiustamento per condizione
        condition_multiplier = self.settings.CONDITION_MULTIPLIERS.get(condition, 1.0)
        
        # Aggiustamento per velocità vendita desiderata
        speed_multipliers = {
            "fast": 0.85,      # Prezzo aggressivo per vendita rapida
            "normal": 1.0,     # Prezzo di mercato
            "premium": 1.15    # Prezzo premium per massimizzare profitto
        }
        speed_multiplier = speed_multipliers.get(target_sale_speed, 1.0)
        
        suggested = base_price * condition_multiplier * speed_multiplier
        
        # Arrotonda a numero sensato
        return max(1, round(suggested))
    
    def _determine_market_position(self, suggested_price: float, distribution: PriceDistribution) -> str:
        """Determina posizione nel mercato"""
        
        q1, q3 = distribution.quartiles["Q1"], distribution.quartiles["Q3"]
        
        if suggested_price <= q1:
            return "low"
        elif suggested_price >= q3:
            return "high"
        else:
            return "average"
    
    def _calculate_confidence(self, sample_size: int) -> float:
        """Calcola livello di confidenza basato su sample size"""
        
        if sample_size >= 20:
            return 0.9
        elif sample_size >= 10:
            return 0.75
        elif sample_size >= 5:
            return 0.6
        else:
            return 0.4
    
    def _generate_analysis_summary(
        self, 
        distribution: PriceDistribution, 
        sample_size: int,
        market_position: str
    ) -> str:
        """Genera summary testuale dell'analisi"""
        
        position_text = {
            "low": "competitivo",
            "average": "allineato al mercato", 
            "high": "premium"
        }
        
        return f"""
        Analizzati {sample_size} articoli simili venduti.
        Prezzo medio di mercato: {distribution.mean_price}€
        Il prezzo suggerito è {position_text[market_position]}.
        Variabilità prezzi: ±{distribution.std_dev}€
        """.strip()
    
    def _create_fallback_analysis(self) -> PriceAnalysis:
        """Crea analisi fallback quando non ci sono dati"""
        
        fallback_distribution = PriceDistribution(
            min_price=10.0,
            max_price=25.0,
            mean_price=15.0,
            median_price=15.0,
            mode_price=15.0,
            std_dev=5.0,
            quartiles={"Q1": 12.0, "Q2": 15.0, "Q3": 18.0}
        )
        
        return PriceAnalysis(
            suggested_price=15.0,
            distribution=fallback_distribution,
            total_listings=0,
            price_range="10€ - 25€",
            confidence_level=0.3,
            market_position="average",
            analysis_summary="Stima basata su dati generici - dati di mercato limitati"
        )