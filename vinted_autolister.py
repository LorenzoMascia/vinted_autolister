import streamlit as st
import requests
import json
import base64
from PIL import Image
import io
from dataclasses import dataclass
from typing import Dict, List, Optional
import re
import statistics
from bs4 import BeautifulSoup
import time
import random

@dataclass
class ProductData:
    brand: str
    type: str
    color: str
    material: str
    category: str = ""

@dataclass
class ListingData:
    title: str
    description: str
    price: float
    condition: str
    category: str
    size: str
    brand: str
    type: str
    color: str

class VintedScraper:
    """Simulatore di scraping Vinted per prezzi"""
    
    def __init__(self):
        # Prezzi di esempio per diversi tipi di abbigliamento
        self.mock_prices = {
            "felpa": {"nike": [12, 15, 18, 20, 25], "adidas": [10, 13, 16, 22], "generic": [8, 10, 12, 15]},
            "t-shirt": {"nike": [8, 10, 12, 15], "adidas": [7, 9, 11, 14], "generic": [5, 7, 9, 12]},
            "jeans": {"levis": [25, 30, 35, 40], "diesel": [20, 25, 30], "generic": [15, 18, 22, 25]},
            "scarpe": {"nike": [30, 40, 50, 60], "adidas": [25, 35, 45], "generic": [20, 25, 30]}
        }
    
    def search_similar_items(self, brand: str, item_type: str, size: str) -> List[Dict]:
        """Simula la ricerca di articoli simili su Vinted"""
        time.sleep(1)  # Simula tempo di ricerca
        
        brand_lower = brand.lower()
        type_lower = item_type.lower()
        
        # Trova prezzi basati su brand e tipo
        prices = []
        if type_lower in self.mock_prices:
            if brand_lower in self.mock_prices[type_lower]:
                prices = self.mock_prices[type_lower][brand_lower]
            else:
                prices = self.mock_prices[type_lower]["generic"]
        else:
            # Prezzi generici se tipo non trovato
            prices = [10, 12, 15, 18, 20]
        
        # Aggiungi variazione per la taglia
        size_multiplier = {"XS": 0.9, "S": 0.95, "M": 1.0, "L": 1.05, "XL": 1.1}.get(size, 1.0)
        prices = [int(p * size_multiplier) for p in prices]
        
        # Crea listings fittizi
        listings = []
        for i, price in enumerate(prices):
            listings.append({
                "title": f"{brand} {item_type} - Taglia {size}",
                "price": price,
                "condition": random.choice(["Ottimo", "Buono", "Discreto"]),
                "url": f"https://vinted.it/item/{random.randint(1000000, 9999999)}"
            })
        
        return listings

class PriceAnalyzer:
    """Analizza i prezzi e suggerisce un prezzo ottimale"""
    
    @staticmethod
    def analyze_prices(listings: List[Dict], condition: str) -> Dict:
        if not listings:
            return {"suggested_price": 15, "analysis": "Prezzo base stimato"}
        
        prices = [item["price"] for item in listings]
        
        # Calcola statistiche
        mean_price = statistics.mean(prices)
        median_price = statistics.median(prices)
        min_price = min(prices)
        max_price = max(prices)
        
        # Aggiusta prezzo basato su condizione
        condition_multiplier = {
            "Nuovo con etichetta": 1.2,
            "Ottimo": 1.0,
            "Buono": 0.85,
            "Discreto": 0.7,
            "Rovinato": 0.5
        }.get(condition, 1.0)
        
        suggested_price = int(median_price * condition_multiplier)
        
        return {
            "suggested_price": suggested_price,
            "mean_price": round(mean_price, 2),
            "median_price": median_price,
            "price_range": f"{min_price}€ - {max_price}€",
            "analysis": f"Analizzati {len(listings)} articoli simili"
        }

class VisionAnalyzer:
    """Analizza immagini usando OpenAI Vision API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    def analyze_image(self, image_data: bytes) -> ProductData:
        """Analizza l'immagine e estrae dati del prodotto"""
        
        # Converti immagine in base64
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analizza questa immagine di un capo di abbigliamento. 
                            Restituisci un JSON con i seguenti campi:
                            - brand: marca del prodotto (se visibile)
                            - type: tipo di capo (es. felpa, t-shirt, jeans, scarpe)
                            - color: colore principale
                            - material: materiale (se identificabile)
                            - category: categoria Vinted appropriata
                            
                            Rispondi SOLO con il JSON, senza altro testo."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Estrai JSON dalla risposta
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group())
                    return ProductData(
                        brand=data.get('brand', 'Sconosciuto'),
                        type=data.get('type', 'Abbigliamento'),
                        color=data.get('color', 'Vario'),
                        material=data.get('material', 'Misto'),
                        category=data.get('category', 'Abbigliamento')
                    )
            
            # Fallback se API non funziona
            return ProductData(
                brand="Analisi non disponibile",
                type="Abbigliamento",
                color="Da specificare",
                material="Misto",
                category="Abbigliamento"
            )
            
        except Exception as e:
            st.error(f"Errore nell'analisi dell'immagine: {str(e)}")
            return ProductData(
                brand="Errore analisi",
                type="Abbigliamento", 
                color="Da specificare",
                material="Misto",
                category="Abbigliamento"
            )

class DescriptionGenerator:
    """Genera titoli e descrizioni per i prodotti"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        } if api_key else None
    
    def generate_listing(self, product_data: ProductData, size: str, condition: str, price: float) -> ListingData:
        """Genera titolo e descrizione per il listing"""
        
        if self.api_key and self.headers:
            return self._generate_with_ai(product_data, size, condition, price)
        else:
            return self._generate_template(product_data, size, condition, price)
    
    def _generate_with_ai(self, product_data: ProductData, size: str, condition: str, price: float) -> ListingData:
        """Genera contenuto usando OpenAI"""
        
        prompt = f"""
        Genera un titolo e una descrizione per un annuncio Vinted in italiano.
        
        Dati prodotto:
        - Marca: {product_data.brand}
        - Tipo: {product_data.type}
        - Colore: {product_data.color}
        - Materiale: {product_data.material}
        - Taglia: {size}
        - Condizione: {condition}
        - Prezzo: {price}€
        
        Restituisci un JSON con:
        - title: titolo accattivante (max 60 caratteri)
        - description: descrizione dettagliata e amichevole (100-200 parole)
        
        Usa un tono amichevole e includi dettagli utili per l'acquirente.
        """
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=self.headers,
                json={
                    "model": "gpt-4o",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 500
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group())
                    return ListingData(
                        title=data.get('title', ''),
                        description=data.get('description', ''),
                        price=price,
                        condition=condition,
                        category=product_data.category,
                        size=size,
                        brand=product_data.brand,
                        type=product_data.type,
                        color=product_data.color
                    )
        except Exception as e:
            st.warning(f"Errore generazione AI: {str(e)}. Uso template di fallback.")
        
        return self._generate_template(product_data, size, condition, price)
    
    def _generate_template(self, product_data: ProductData, size: str, condition: str, price: float) -> ListingData:
        """Genera contenuto usando template predefiniti"""
        
        # Titolo template
        title = f"{product_data.brand} {product_data.type} {product_data.color} - Taglia {size}"
        if len(title) > 60:
            title = f"{product_data.brand} {product_data.type} - Taglia {size}"
        
        # Descrizione template
        description = f"""Vendo {product_data.type.lower()} {product_data.brand} in ottime condizioni!

📏 Taglia: {size}
🎨 Colore: {product_data.color}
🧵 Materiale: {product_data.material}
✨ Condizione: {condition}

Capo curato e ben conservato, perfetto per il tuo guardaroba!
Spedizione veloce e imballaggio accurato.

💰 Prezzo: {price}€
💬 Contattami per foto aggiuntive o domande!

#vinted #abbigliamento #secondamano #sostenibile"""
        
        return ListingData(
            title=title,
            description=description,
            price=price,
            condition=condition,
            category=product_data.category,
            size=size,
            brand=product_data.brand,
            type=product_data.type,
            color=product_data.color
        )

def main():
    st.set_page_config(
        page_title="Vinted AutoLister",
        page_icon="👕",
        layout="wide"
    )
    
    st.title("👕 Vinted AutoLister")
    st.markdown("*Trasforma le tue foto in annunci pronti per la pubblicazione*")
    
    # Sidebar per configurazione
    with st.sidebar:
        st.header("⚙️ Configurazione")
        openai_api_key = st.text_input(
            "OpenAI API Key (opzionale)",
            type="password",
            help="Per analisi AI avanzata. Lascia vuoto per usare template predefiniti."
        )
        
        st.markdown("---")
        st.markdown("**📋 Come usare:**")
        st.markdown("1. Carica foto del capo")
        st.markdown("2. Inserisci taglia e condizione")
        st.markdown("3. Clicca 'Genera Annuncio'")
        st.markdown("4. Copia il risultato!")
    
    # Layout principale
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📷 Upload & Dettagli")
        
        # Upload immagine
        uploaded_file = st.file_uploader(
            "Carica foto del capo",
            type=['png', 'jpg', 'jpeg'],
            help="Carica una foto chiara del capo di abbigliamento"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Foto caricata", width=300)
        
        # Input utente
        col1a, col1b = st.columns(2)
        with col1a:
            size = st.selectbox(
                "Taglia",
                ["XS", "S", "M", "L", "XL", "XXL", "Unica"]
            )
        
        with col1b:
            condition = st.selectbox(
                "Condizione",
                ["Nuovo con etichetta", "Ottimo", "Buono", "Discreto", "Rovinato"]
            )
        
        # Pulsante genera
        generate_button = st.button("🚀 Genera Annuncio", type="primary")
    
    with col2:
        st.header("📝 Risultato")
        
        if generate_button and uploaded_file:
            with st.spinner("Analizzo l'immagine e genero l'annuncio..."):
                # Inizializza componenti
                scraper = VintedScraper()
                analyzer = PriceAnalyzer()
                
                # Analisi immagine
                if openai_api_key:
                    vision_analyzer = VisionAnalyzer(openai_api_key)
                    image_bytes = uploaded_file.getvalue()
                    product_data = vision_analyzer.analyze_image(image_bytes)
                else:
                    # Usa dati di esempio se no API key
                    product_data = ProductData(
                        brand="Marca da specificare",
                        type="Abbigliamento",
                        color="Da specificare",
                        material="Misto",
                        category="Abbigliamento"
                    )
                
                # Ricerca prezzi
                listings = scraper.search_similar_items(
                    product_data.brand, 
                    product_data.type, 
                    size
                )
                
                # Analisi prezzi
                price_analysis = analyzer.analyze_prices(listings, condition)
                suggested_price = price_analysis["suggested_price"]
                
                # Generazione descrizione
                desc_generator = DescriptionGenerator(openai_api_key)
                listing_data = desc_generator.generate_listing(
                    product_data, size, condition, suggested_price
                )
            
            # Mostra risultati
            st.success("✅ Annuncio generato con successo!")
            
            # Dati rilevati
            with st.expander("🔍 Dati rilevati dall'immagine"):
                col2a, col2b = st.columns(2)
                with col2a:
                    st.write(f"**Marca:** {product_data.brand}")
                    st.write(f"**Tipo:** {product_data.type}")
                with col2b:
                    st.write(f"**Colore:** {product_data.color}")
                    st.write(f"**Materiale:** {product_data.material}")
            
            # Analisi prezzi
            with st.expander("💰 Analisi prezzi"):
                st.write(f"**Prezzo suggerito:** {suggested_price}€")
                st.write(f"**Range di mercato:** {price_analysis['price_range']}")
                st.write(f"**Analisi:** {price_analysis['analysis']}")
            
            # Risultato finale
            st.subheader("📋 Annuncio finale")
            
            # Titolo
            st.text_area("Titolo", value=listing_data.title, height=50)
            
            # Descrizione
            st.text_area("Descrizione", value=listing_data.description, height=200)
            
            # Dati aggiuntivi
            col2c, col2d, col2e = st.columns(3)
            with col2c:
                st.metric("Prezzo", f"{listing_data.price}€")
            with col2d:
                st.metric("Taglia", listing_data.size)
            with col2e:
                st.metric("Condizione", listing_data.condition)
            
            # JSON export
            with st.expander("📄 Esporta JSON"):
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
                st.json(json_data)
                
                # Pulsante copia
                st.code(json.dumps(json_data, indent=2, ensure_ascii=False))
        
        elif generate_button:
            st.warning("⚠️ Carica prima un'immagine!")
    
    # Footer
    st.markdown("---")
    st.markdown("*Vinted AutoLister - Creato per semplificare la vendita online* 🛍️")

if __name__ == "__main__":
    main()