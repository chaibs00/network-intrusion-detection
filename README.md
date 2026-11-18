# Partie 2 — IA : classification des attaques réseau (CSE-CIC-IDS2018)

Projet 5 — Réseau bancaire sécurisé.

&nbsp;

```bash
    streamlit run app.py
```


```bash
Network-Intrusion-Detection/
├── app/                          ← NEW: the Streamlit app
│   ├── Overview.py               ← entry point
│   ├── common.py                 ← loads model, encoder, features, demo flows
│   └── pages/
│       ├── 1_Analyse_a_flow.py
│       └── 2_Live_traffic.py
├── data/
│   └── demo_flows.parquet        ← the flows the app analyses
├── models/
│   ├── ML/                       ← RandomForest.joblib is used by the app
│   ├── DL/                       ← not used by the app
│   └── shared/                   ← features.json, label_encoder.joblib
├── results/
│   ├── metrics/
│   └── final_comparison.csv      ← Overview table
├── figures/                      ← Overview figures
├── notebooks/
├── README.md
└── requirements.txt


Network-Intrusion-Detection/
├── app.py                 ← entry point: only lists the 3 pages (about 10 lines)
├── app/
│   ├── common.py          ← loads model, encoder, features, demo flows
│   ├── overview.py
│   ├── analyse.py
│   └── live.py
├── data/ models/ results/ figures/ notebooks/
└── requirements.txt
```


&nbsp;

| \# | Notebook |
| :---- | :---- |
| 01 | Download and merge (done) |
| 02 | Data quality inspection (+ conversion and sampling) |
| 03 | Cleaning |
| 04 | EDA on the clean data |
| 05 | Preprocessing for models (encode, split, scale) |
| 06+ | ML models, deep learning, evaluation, demo |

&nbsp;

## Setup (Google Colab \+ Drive)

1. Create the folder `MyDrive/ids2018_project/` on Google Drive.  
2. Upload `utils.py` into it (re-upload it whenever it changes).  
3. Open the notebooks in Colab and run them **in order**. Each one saves its outputs to Drive.

| Notebook | Purpose | Reads | Writes |
| :---- | :---- | :---- | :---- |
| `01_download_and_explore` | Download from AWS S3, first exploration | S3 bucket | `data/combined_raw.parquet` |
| `01b_eda` | Problem analysis \+ visual EDA (distributions, ports, correlations, PCA) | `combined_raw.parquet` | `figures/01b_*` |
| `02_preprocessing` | Cleaning, leakage removal, split, scaling | `combined_raw.parquet` | `data/processed/*` |
| `03_ml_models` | LogReg, DecisionTree, RandomForest, XGBoost, LightGBM, soft-voting ensemble, Optuna | `processed/` | `models/`, `results/` |
| `04_deep_learning` | MLP, 1D-CNN (Keras) | `processed/` | `models/`, `results/` |
| `05_evaluation_analysis` | Comparison, confusion matrices, errors, SHAP | `results/`, `models/` | `figures/`, `results/final_comparison.csv` |
| `06_demo` | Soutenance demo: predictions, live stream simulation, SHAP per flow | `models/`, `processed/` | — |

Use a GPU runtime for notebook 04 (Runtime → Change runtime type → GPU).

## Dataset

CSE-CIC-IDS2018 (CIC & CSE), "Processed Traffic Data for ML Algorithms". [https\://www\.unb.ca/cic/datasets/ids-2018.html](https://www.unb.ca/cic/datasets/ids-2018.html) — public bucket `s3://cse-cic-ids2018/` (ca-central-1).

Sharafaldin, I., Habibi Lashkari, A., Ghorbani, A. (2018). *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization.* ICISSP 2018\.