"""
DARKVERSE — Streamlit Dashboard
Person 3: Dashboard & Integration

This is the Person 3 contribution — connects Person 1's data pipeline
with Person 2's analysis modules in an interactive Streamlit dashboard.

For the full integrated project, see the Darkverse/ folder.
"""

# ── This file intentionally imports from the Darkverse/ package.
# ── To run standalone, copy this file + requirements.txt into the Darkverse/ folder
# ── and run:  streamlit run app.py

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Darkverse"))

# Re-export the full dashboard app
exec(open(os.path.join(os.path.dirname(__file__), "..", "Darkverse", "app.py")).read())

