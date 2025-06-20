# ============================================================================
# FILE: src/utils/image_utils.py
# Utilities per processamento immagini
# ============================================================================

from PIL import Image, ImageEnhance, ImageFilter
import io
from typing import Tuple

class ImageProcessor:
    """Utilities per processamento e ottimizzazione immagini"""
    
    @staticmethod
    def resize_maintain_aspect(image: Image.Image, max_size: int) -> Image.Image:
        """Ridimensiona mantenendo aspect ratio"""
        
        width, height = image.size
        
        if width > height:
            new_width = max_size
            new_height = int((height * max_size) / width)
        else:
            new_height = max_size
            new_width = int((width * max_size) / height)
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    @staticmethod
    def enhance_quality(image: Image.Image) -> Image.Image:
        """Migliora qualità immagine per analisi AI"""
        
        # Contrasto
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)
        
        # Nitidezza
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.05)
        
        # Slight denoising
        image = image.filter(ImageFilter.SMOOTH_MORE)
        
        return image
    
    @staticmethod
    def validate_image(image_data: bytes) -> Tuple[bool, str]:
        """Valida se immagine è utilizzabile"""
        
        try:
            image = Image.open(io.BytesIO(image_data))
            
            # Check formato
            if image.format not in ['JPEG', 'PNG', 'WEBP']:
                return False, "Formato non supportato"
            
            # Check dimensioni minime
            if image.width < 200 or image.height < 200:
                return False, "Immagine troppo piccola (min 200x200)"
            
            # Check dimensioni massime
            if image.width > 4000 or image.height > 4000:
                return False, "Immagine troppo grande (max 4000x4000)"
            
            return True, "OK"
            
        except Exception as e:
            return False, f"Errore validazione: {str(e)}"