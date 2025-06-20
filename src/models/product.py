# ============================================================================
# FILE: src/models/product.py
# Modelli dati per i prodotti
# ============================================================================

from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum

class ProductType(Enum):
    FELPA = "felpa"
    T_SHIRT = "t-shirt"
    JEANS = "jeans"
    SCARPE = "scarpe"
    GIACCA = "giacca"
    CAMICIA = "camicia"

class Condition(Enum):
    NUOVO_ETICHETTA = "Nuovo con etichetta"
    OTTIMO = "Ottimo"
    BUONO = "Buono"
    DISCRETO = "Discreto"
    ROVINATO = "Rovinato"

@dataclass
class ProductData:
    """Dati prodotto estratti dall'immagine"""
    brand: str
    type: ProductType
    color: str
    material: str
    category: str
    confidence_score: float = 0.0
    additional_features: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.additional_features is None:
            self.additional_features = {}
# ============================================================================
# FILE: src/models/product.py
# Modelli dati per i prodotti
# ============================================================================

from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum

class ProductType(Enum):
    FELPA = "felpa"
    T_SHIRT = "t-shirt"
    JEANS = "jeans"
    SCARPE = "scarpe"
    GIACCA = "giacca"
    CAMICIA = "camicia"

class Condition(Enum):
    NUOVO_ETICHETTA = "Nuovo con etichetta"
    OTTIMO = "Ottimo"
    BUONO = "Buono"
    DISCRETO = "Discreto"
    ROVINATO = "Rovinato"

@dataclass
class ProductData:
    """Dati prodotto estratti dall'immagine"""
    brand: str
    type: ProductType
    color: str
    material: str
    category: str
    confidence_score: float = 0.0
    additional_features: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.additional_features is None:
            self.additional_features = {}
