# ============================================================================
# FILE: src/ui/components/export.py
# Componente esportazione
# ============================================================================

import streamlit as st
import json
from ..models.listing import ListingData

class ExportComponent:
    """Componente per esportazione risultati"""
    
    def render(self, listing_data: ListingData):
        """Renderizza opzioni di esportazione"""
        
        with st.expander("📤 Esporta Annuncio"):
            st.subheader("Formati di Esportazione")
            
            # JSON
            json_data = {
                "title": listing_data.title,
                "description": listing_data.description,
                "price": listing_data.price,
                "size": listing_data.size,
                "condition": listing_data.condition,
                "brand": listing_data.brand,
                "type": listing_data.type,
                "color": listing_data.color,
                "category": listing_data.category
            }
            
            st.download_button(
                label="Scarica JSON",
                data=json.dumps(json_data, indent=2, ensure_ascii=False),
                file_name="vinted_listing.json",
                mime="application/json"
            )
            
            # Testo semplice
            text_data = f"""
            {listing_data.title}
            {listing_data.price}€
            
            {listing_data.description}
            """
            
            st.download_button(
                label="Scarica TXT",
                data=text_data.strip(),
                file_name="vinted_listing.txt",
                mime="text/plain"
            )