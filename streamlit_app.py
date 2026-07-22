import sys
from pathlib import Path

PRODUTO_DIR = Path(__file__).resolve().parent / "Tese" / "03-Produto-Copiloto"
sys.path.insert(0, str(PRODUTO_DIR))

from app.app import *
