# ============================================================================
# FILE: src/ui/components/upload.py
# Componente upload immagine
# ============================================================================

import streamlit as st
from PIL import Image
import io
from typing import List, Dict, Optional
from src.utils.image_utils import ImageProcessor  
from src.utils.validation import InputValidator  

class ImageUploadComponent:
    """Componente per upload e preview immagine"""
    
    def __init__(self):
        self.processor = ImageProcessor()
        self.validator = InputValidator()
    
    def render(self) -> Optional[bytes]:
        """Renderizza componente e ritorna dati immagine"""
        
        st.subheader("📷 Carica foto del capo")
        
        uploaded_file = st.file_uploader(
            "Seleziona un'immagine",
            type=['png', 'jpg', 'jpeg'],
            help="Carica una foto chiara del capo di abbigliamento"
        )
        
        if uploaded_file:
            try:
                image_data = uploaded_file.getvalue()
                
                # Validazione
                valid, msg = self.validator.validate_image_file(uploaded_file.name)
                if not valid:
                    st.warning(f"Problema con l'immagine: {msg}")
                    return None
                
                # Preview
                image = Image.open(io.BytesIO(image_data))
                st.image(image, caption="Anteprima immagine", width=300)
                
                return image_data
                
            except Exception as e:
                st.error(f"Errore nel caricamento dell'immagine: {str(e)}")
                return None
        
        return None