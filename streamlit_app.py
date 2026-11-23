"""
COSMATRIX — Root Streamlit Cloud Entrypoint
Automatically runs Cosmatrix/app.py
"""

import sys
import os
from pathlib import Path

# Add Cosmatrix folder to sys.path so all imports resolve smoothly
COS_DIR = Path(__file__).resolve().parent / "Cosmatrix"
if str(COS_DIR) not in sys.path:
    sys.path.insert(0, str(COS_DIR))

# Execute the main application
app_path = COS_DIR / "app.py"
with open(app_path, "r", encoding="utf-8") as f:
    code = f.read()

exec(code, {"__name__": "__main__", "__file__": str(app_path)})
