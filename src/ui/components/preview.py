# ============================================================================
# FILE: src/ui/components/preview.py
# Componente preview risultati
# ============================================================================

import streamlit as st
from typing import Dict, Any
from models.listing import ListingData

class PreviewComponent:
    """Componente per preview dei risultati"""
    
    def render(self, listing_data: ListingData, market_data: Dict[str, Any]):
        """Renderizza preview dell'annuncio generato"""
        
        st.subheader("📝 Anteprima Annuncio")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_area("Titolo", 
                        value=listing_data.title, 
                        height=50,
                        key="preview_title")
            
            st.text_area("Descrizione", 
                        value=listing_data.description, 
                        height=200,
                        key="preview_desc")
        
        with col2:
            st.metric("Prezzo Suggerito", f"{listing_data.price}€")
            st.metric("Condizione", listing_data.condition)
            st.metric("Taglia", listing_data.size)
            
            st.markdown("---")
            st.markdown("**Analisi di Mercato**")
            st.markdown(f"- Range prezzi: {market_data.get('price_range', 'N/A')}")
            st.markdown(f"- Articoli analizzati: {market_data.get('total_listings', 0)}")
            st.markdown(f"- Posizionamento: {market_data.get('market_position', 'N/A')}")