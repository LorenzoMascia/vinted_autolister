# ============================================================================
# FILE: src/api/routes.py
# API routes FastAPI
# ============================================================================

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
import asyncio
from pathlib import Path
import tempfile
from ..core.autolister import VintedAutoLister
from ..models.listing import ListingResult

router = APIRouter()

@router.post("/analyze")
async def analyze_image(
    image: UploadFile = File(...),
    size: str = "M",
    condition: str = "Buono",
    openai_key: Optional[str] = None,
    target_speed: str = "normal",
    content_style: str = "friendly"
) -> ListingResult:
    """Endpoint per analisi immagine e generazione annuncio"""
    
    try:
        # Salva file temporaneo
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await image.read())
            tmp_path = tmp.name
        
        # Esegui analisi
        autolister = VintedAutoLister(openai_key)
        result = await autolister.process_image(
            image_path=tmp_path,
            size=size,
            condition=condition,
            target_sale_speed=target_speed,
            content_style=content_style
        )
        
        # Cleanup
        Path(tmp_path).unlink(missing_ok=True)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/price-check")
async def price_check(
    brand: str,
    item_type: str,
    size: str,
    condition: str = "Buono"
):
    """Endpoint per controllo prezzi senza immagine"""
    
    try:
        autolister = VintedAutoLister()
        result = await autolister.analyze_price_only(
            brand=brand,
            item_type=item_type,
            size=size,
            condition=condition
        )
        
        return {
            "suggested_price": result.suggested_price,
            "price_range": result.price_range,
            "market_position": result.market_position,
            "total_listings": result.total_listings
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))