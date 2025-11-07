import sys
from pathlib import Path

# Add /app/src to sys.path so imports like 'from config import config' work in the container
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
