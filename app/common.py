"""Shared by all pages: file paths, loading (done once, then cached), attack families."""
import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]          # project root
ASSETS = ROOT / "assets"                            # figures/, models/, results/
MODEL_NAME = "RandomForest"
MODEL_PATH = ASSETS / "models" / "ML" / f"{MODEL_NAME}.joblib"
SHARED_DIR = ASSETS / "models" / "shared"
FIG_DIR = ASSETS / "figures"
RESULTS_PATH = ASSETS / "results" / "final_comparison.csv"
DEMO_PATH = ROOT / "data" / "demo_flows.parquet"


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_resource
def load_class_names():
    encoder = joblib.load(SHARED_DIR / "label_encoder.joblib")
    return list(encoder.classes_)


@st.cache_data
def load_features():
    return json.load(open(SHARED_DIR / "features.json"))


@st.cache_data
def load_demo_flows():
    return pd.read_parquet(DEMO_PATH)


@st.cache_data
def load_results():
    return pd.read_csv(RESULTS_PATH, index_col=0)


@st.cache_resource
def load_explainer():
    import shap
    return shap.TreeExplainer(load_model())


def family(label):
    if label == "Benign":
        return "Benign"
    if "DDOS" in label.upper():
        return "DDoS"
    if "DoS" in label:
        return "DoS"
    if "Brute" in label:
        return "Brute force"
    if label == "Web-Attack":
        return "Web attack"
    if label == "Bot":
        return "Botnet"
    if label == "Infilteration":
        return "Infiltration"
    return "Other"


RESPONSE = {
    "Benign": "No action.",
    "DoS": "Rate-limit the source, protect the web server (timeouts, connection limits).",
    "DDoS": "Activate upstream DDoS filtering, rate-limit at the edge router.",
    "Brute force": "Block the source IP, lock the targeted accounts, enforce MFA.",
    "Web attack": "Block the request at the web firewall, check the application logs.",
    "Botnet": "Isolate the infected machine (quarantine VLAN), block its remote control traffic.",
    "Infiltration": "Isolate the machine immediately and start incident response.",
    "Other": "Investigate.",
}