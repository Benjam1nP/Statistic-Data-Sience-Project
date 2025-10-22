import sys, os
from pathlib import Path

# Projekt-Root bestimmen (eine Ebene über notebooks)
ROOT = Path.cwd().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

print("Projekt-Root hinzugefügt:", ROOT)