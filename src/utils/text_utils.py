# ============================================================================
# FILE: src/utils/text_utils.py
# Utilities per processamento testo
# ============================================================================

import re
from typing import List, Dict

class TextNormalizer:
    """Normalizza testi per ricerche e confronti"""
    
    @staticmethod
    def normalize_brand(brand: str) -> str:
        """Normalizza nome brand"""
        
        # Mapping brand comuni
        brand_aliases = {
            'nike': ['nike', 'just do it'],
            'adidas': ['adidas', 'three stripes'],
            'zara': ['zara', 'zara man', 'zara woman'],
            'h&m': ['h&m', 'hm', 'hennes mauritz'],
            'uniqlo': ['uniqlo', 'uniqlo u']
        }
        
        normalized = brand.lower().strip()
        
        # Trova brand principale
        for main_brand, aliases in brand_aliases.items():
            if any(alias in normalized for alias in aliases):
                return main_brand
        
        return normalized
    
    @staticmethod
    def normalize_item_type(item_type: str) -> str:
        """Normalizza tipo articolo"""
        
        type_aliases = {
            'felpa': ['felpa', 'hoodie', 'sweatshirt', 'pullover'],
            't-shirt': ['t-shirt', 'tshirt', 'maglietta', 'maglia'],
            'jeans': ['jeans', 'denim', 'pantaloni'],
            'scarpe': ['scarpe', 'scarpa', 'sneakers', 'tennis', 'shoes'],
            'giacca': ['giacca', 'giacche', 'giaccone', 'giubbotto', 'jacket'],
            'camicia': ['camicia', 'shirt', 'button down']
        }
        
        normalized = item_type.lower().strip()
        
        # Trova tipo principale
        for main_type, aliases in type_aliases.items():
            if any(alias in normalized for alias in aliases):
                return main_type
        
        return normalized
    
    @staticmethod
    def normalize_size(size: str) -> str:
        """Normalizza taglia abbigliamento"""
        
        size_mapping = {
            'xs': ['xs', 'extra small'],
            's': ['s', 'small'],
            'm': ['m', 'medium'],
            'l': ['l', 'large'],
            'xl': ['xl', 'extra large'],
            'xxl': ['xxl', '2xl', 'extra extra large'],
            'unica': ['unica', 'one size', 'os']
        }
        
        normalized = size.lower().strip()
        
        for main_size, aliases in size_mapping.items():
            if normalized in aliases:
                return main_size.upper()
        
        return size.upper()

class TextValidator:
    """Validazione e pulizia testi per listing"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Pulisce testo rimuovendo caratteri problematici"""
        
        # Rimuovi emoji eccessive
        cleaned = re.sub(r'([^\w\s])\1{2,}', r'\1', text)
        
        # Rimuovi caratteri speciali pericolosi
        cleaned = re.sub(r'[^\w\s.,!?€$#@%&*+-]', '', cleaned)
        
        # Normalizza spazi
        cleaned = ' '.join(cleaned.split())
        
        return cleaned
    
    @staticmethod
    def validate_title(title: str) -> bool:
        """Valida titolo per requisiti Vinted"""
        
        if len(title) < 5 or len(title) > 60:
            return False
        
        if not any(c.isalpha() for c in title):
            return False
            
        return True
    
    @staticmethod
    def validate_description(desc: str) -> bool:
        """Valida descrizione per requisiti Vinted"""
        
        if len(desc) < 20 or len(desc) > 2000:
            return False
            
        if not any(c.isalpha() for c in desc):
            return False
            
        return True