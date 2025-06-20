# ============================================================================
# FILE: src/utils/validation.py
# Validazione input utente
# ============================================================================

from typing import Optional, Tuple
from pathlib import Path
from src.models.product import Condition

class InputValidator:
    """Validazione input utente e file"""
    
    @staticmethod
    def validate_image_file(file_path: str) -> Tuple[bool, Optional[str]]:
        """Valida file immagine"""
        
        path = Path(file_path)
        
        if not path.exists():
            return False, "File non trovato"
            
        if path.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
            return False, "Formato non supportato (usa JPG o PNG)"
            
        if path.stat().st_size > 5 * 1024 * 1024:  # 5MB
            return False, "File troppo grande (max 5MB)"
            
        return True, None
    
    @staticmethod
    def validate_size(size: str) -> Tuple[bool, Optional[str]]:
        """Valida taglia abbigliamento"""
        
        valid_sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'UNICA']
        
        if size.upper() not in valid_sizes:
            return False, f"Taglia non valida (usa {', '.join(valid_sizes)})"
            
        return True, None
    
    @staticmethod
    def validate_condition(condition: str) -> Tuple[bool, Optional[str]]:
        """Valida condizione articolo"""
        
        try:
            Condition(condition)
            return True, None
        except ValueError:
            valid_conditions = [c.value for c in Condition]
            return False, f"Condizione non valida (usa {', '.join(valid_conditions)})"