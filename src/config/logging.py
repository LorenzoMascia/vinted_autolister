# ============================================================================
# FILE: src/config/logging.py
# Configurazione logging
# ============================================================================

import logging
from pathlib import Path
from datetime import datetime
from ..config.settings import Settings

def setup_logging():
    """Configura sistema di logging"""
    
    settings = Settings()
    
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"autolister_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    # Riduci log level per alcune librerie
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)