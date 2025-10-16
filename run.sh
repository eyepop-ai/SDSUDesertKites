#!/bin/bash

# Activate virtual environment and run Streamlit
. /home/appuser/venv/bin/activate
streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false --client.toolbarMode=minimal

