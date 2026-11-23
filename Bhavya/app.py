"""
COSMATRIX — Streamlit Dashboard
Contributor: Bhavya (Dashboard & Integration)

Connects Purva's data pipeline with Suyash's analysis modules
in an interactive Streamlit dashboard.

For the full integrated project, see the Cosmatrix/ folder.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Cosmatrix"))

# Re-export the full dashboard app from Cosmatrix
exec(open(os.path.join(os.path.dirname(__file__), "..", "Cosmatrix", "app.py")).read())
