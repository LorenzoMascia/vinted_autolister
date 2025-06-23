# ============================================================================
# FILE: src/ui/pages/main.py
# Pagina principale Streamlit
# ============================================================================


import streamlit as st
from typing import Optional, Dict, Any
from core.autolister import VintedAutoLister
from models.listing import ListingResult
from ui.components.upload import ImageUploadComponent
from ui.components.preview import PreviewComponent
from ui.components.export import ExportComponent

class MainPage:
    """Pagina principale dell'applicazione"""
    
    def __init__(self):
        self.upload_component = ImageUploadComponent()
        self.preview_component = PreviewComponent()
        self.export_component = ExportComponent()
    
    def render_sidebar(self):
        """Renderizza sidebar"""
        
        with st.sidebar:
            st.header("⚙️ Configurazione")
            
            self.openai_key = st.text_input(
                "OpenAI API Key (opzionale)",
                type="password",
                help="Per analisi AI avanzata. Lascia vuoto per usare template predefiniti."
            )
            
            self.target_speed = st.selectbox(
                "Strategia di Prezzo",
                options=["fast", "normal", "premium"],
                index=1,
                help="Vendita rapida (prezzo basso), normale o premium (prezzo alto)"
            )
            
            self.content_style = st.selectbox(
                "Stile Descrizione",
                options=["friendly", "professional", "trendy"],
                index=0,
                help="Tono della descrizione dell'annuncio"
            )
            
            st.markdown("---")
            st.markdown("**📋 Come usare:**")
            st.markdown("1. Carica foto del capo")
            st.markdown("2. Inserisci taglia e condizione")
            st.markdown("3. Clicca 'Genera Annuncio'")
            st.markdown("4. Copia il risultato!")
    
    def render_input_form(self) -> Optional[Dict[str, Any]]:
        """Renderizza form input e ritorna dati"""
        
        st.subheader("📝 Dettagli Prodotto")
        
        col1, col2 = st.columns(2)
        
        with col1:
            size = st.selectbox(
                "Taglia",
                options=["XS", "S", "M", "L", "XL", "XXL", "Unica"],
                index=2
            )
        
        with col2:
            condition = st.selectbox(
                "Condizione",
                options=["Nuovo con etichetta", "Ottimo", "Buono", "Discreto", "Rovinato"],
                index=1
            )
        
        return {
            "size": size,
            "condition": condition
        }
    
    def render(self):
        """Renderizza pagina principale"""
        
        st.set_page_config(
            page_title="Vinted AutoLister",
            page_icon="👕",
            layout="wide"
        )
        
        st.title("👕 Vinted AutoLister")
        st.markdown("*Trasforma le tue foto in annunci pronti per la pubblicazione*")
        
        self.render_sidebar()
        
        # Layout principale
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Upload immagine
            image_data = self.upload_component.render()
            
            # Input form
            form_data = self.render_input_form()
            
            # Pulsante genera
            generate_btn = st.button("🚀 Genera Annuncio", type="primary")
        
        with col2:
            if generate_btn and image_data and form_data:
                with st.spinner("Analizzo l'immagine e genero l'annuncio..."):
                    try:
                        autolister = VintedAutoLister(self.openai_key)
                        
                        # Esegui processing (nota: Streamlit non supporta async nativamente)
                        import asyncio
                        result = asyncio.run(
                            autolister.process_image(
                                image_data=image_data,
                                size=form_data["size"],
                                condition=form_data["condition"],
                                target_sale_speed=self.target_speed,
                                content_style=self.content_style
                            )
                        )
                        
                        # Mostra risultati
                        st.success("✅ Annuncio generato con successo!")
                        
                        # Preview
                        self.preview_component.render(
                            result.listing,
                            {
                                "price_range": result.market_analysis.price_range,
                                "total_listings": result.market_analysis.total_listings,
                                "market_position": result.market_analysis.market_position
                            }
                        )
                        
                        # Esportazione
                        self.export_component.render(result.listing)
                        
                    except Exception as e:
                        st.error(f"Errore nella generazione annuncio: {str(e)}")
            
            elif generate_btn:
                st.warning("⚠️ Completa tutti i campi per generare l'annuncio")