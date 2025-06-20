# ============================================================================
# FILE: src/services/cache_service.py
# Gestione cache
# ============================================================================

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import hashlib

class CacheService:
    """Gestione cache locale per risultati API e scraping"""
    
    def __init__(self, cache_dir: str = "cache", ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.ttl = timedelta(hours=ttl_hours)
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_cache_key(self, data: Dict[str, Any]) -> str:
        """Genera chiave cache univoca"""
        
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def _is_cache_valid(self, cache_file: Path) -> bool:
        """Verifica se cache è ancora valida"""
        
        if not cache_file.exists():
            return False
            
        mod_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
        return datetime.now() - mod_time < self.ttl
    
    def get(self, key_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Recupera dati dalla cache"""
        
        cache_key = self._get_cache_key(key_data)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if self._is_cache_valid(cache_file):
            try:
                return json.loads(cache_file.read_text())
            except (json.JSONDecodeError, IOError):
                return None
        return None
    
    def set(self, key_data: Dict[str, Any], value: Dict[str, Any]):
        """Salva dati in cache"""
        
        cache_key = self._get_cache_key(key_data)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            cache_file.write_text(json.dumps(value))
        except IOError as e:
            print(f"Cache save failed: {str(e)}")
