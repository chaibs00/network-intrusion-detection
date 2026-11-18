"""Entry point of the demo app.  Run from the project root:  streamlit run app.py"""
import sys
from pathlib import Path

import streamlit as st

# Let the pages in app/ import common.py
APP_DIR = str(Path(__file__).parent / "app")
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

st.set_page_config(page_title="Network Intrusion Detection", layout="wide")

st.sidebar.markdown("## 🛡️ Intrusion Detection")
st.sidebar.caption("Model: Random Forest · CSE-CIC-IDS2018")

pages = [
    st.Page("app/overview.py", title="Overview", icon=":material/dashboard:", default=True),
    st.Page("app/analyse.py", title="Analyse a flow", icon=":material/search:"),
    st.Page("app/live.py", title="Live traffic", icon=":material/monitoring:"),
]
st.navigation(pages).run()