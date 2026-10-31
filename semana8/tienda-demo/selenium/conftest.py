"""Configuración mínima de pytest para localizar los Page Objects Selenium."""
from pathlib import Path
import sys

SELENIUM_DIR = Path(__file__).resolve().parent
if str(SELENIUM_DIR) not in sys.path:
    sys.path.insert(0, str(SELENIUM_DIR))
