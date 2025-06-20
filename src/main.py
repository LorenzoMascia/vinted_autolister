# ============================================================================
# FILE: src/main.py
# Entry point Streamlit
# ============================================================================

from src.ui.pages.main import MainPage

def main():
    """Entry point applicazione Streamlit"""
    
    page = MainPage()
    page.render()

if __name__ == "__main__":
    main()