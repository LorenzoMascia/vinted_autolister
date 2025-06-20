# ============================================================================
# FILE: src/cli.py
# CLI interface
# ============================================================================

import click
import asyncio
from typing import Optional
from pathlib import Path
from src.core.autolister import VintedAutoLister

@click.group()
def cli():
    """Vinted AutoLister - CLI Tool"""
    pass

@cli.command()
@click.argument("image_path", type=click.Path(exists=True))
@click.option("--size", "-s", required=True, help="Taglia capo (XS, S, M, L, XL, XXL, Unica)")
@click.option("--condition", "-c", required=True, 
              type=click.Choice(["Nuovo con etichetta", "Ottimo", "Buono", "Discreto", "Rovinato"]),
              help="Condizione capo")
@click.option("--openai-key", "-k", help="OpenAI API Key (opzionale)")
def analyze(image_path: str, size: str, condition: str, openai_key: Optional[str]):
    """Analizza immagine e genera annuncio"""
    
    click.echo("🚀 Avvio analisi immagine...")
    
    try:
        autolister = VintedAutoLister(openai_key)
        result = asyncio.run(
            autolister.process_image(
                image_path=image_path,
                size=size,
                condition=condition
            )
        )
        
        click.echo("\n✅ Annuncio generato con successo!")
        click.echo(f"\n📌 Titolo: {result.listing.title}")
        click.echo(f"💰 Prezzo: {result.listing.price}€")
        click.echo(f"\n📝 Descrizione:\n{result.listing.description}")
        
        click.echo("\n📊 Analisi di Mercato:")
        click.echo(f"- Range prezzi: {result.market_analysis.price_range}")
        click.echo(f"- Articoli analizzati: {result.market_analysis.total_listings}")
        click.echo(f"- Posizionamento: {result.market_analysis.market_position}")
        
    except Exception as e:
        click.echo(f"\n❌ Errore: {str(e)}", err=True)

@cli.command()
@click.argument("brand", required=True)
@click.argument("item_type", required=True)
@click.argument("size", required=True)
@click.argument("condition", required=True)
def price_check(brand: str, item_type: str, size: str, condition: str):
    """Controlla prezzi di mercato senza analisi immagine"""
    
    click.echo(f"🔍 Ricerco prezzi per {brand} {item_type} taglia {size}...")
    
    try:
        autolister = VintedAutoLister()
        result = asyncio.run(
            autolister.analyze_price_only(
                brand=brand,
                item_type=item_type,
                size=size,
                condition=condition
            )
        )
        
        click.echo("\n📊 Risultati Analisi Prezzi:")
        click.echo(f"- Prezzo suggerito: {result.suggested_price}€")
        click.echo(f"- Range prezzi: {result.price_range}")
        click.echo(f"- Prezzo medio: {result.distribution.mean_price}€")
        click.echo(f"- Mediana: {result.distribution.median_price}€")
        click.echo(f"- Articoli analizzati: {result.total_listings}")
        
    except Exception as e:
        click.echo(f"\n❌ Errore: {str(e)}", err=True)

if __name__ == "__main__":
    cli()