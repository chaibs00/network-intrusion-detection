import pandas as pd
import streamlit as st

from common import FIG_DIR, MODEL_NAME, family, load_class_names, load_features, load_results

class_names = load_class_names()
features = load_features()
results = load_results()

# ---- Title and description
st.title("Network Intrusion Detection")
st.caption("Attack type classification · CSE-CIC-IDS2018")
st.write(
    "A machine learning model reads the statistics of each network flow (one connection between "
    "two machines) and predicts whether it is normal traffic or **which type of attack** it is."
)

# ---- Classes and features
st.subheader("What the model recognises")
classes = pd.DataFrame({"Class": class_names, "Family": [family(c) for c in class_names]})
st.dataframe(classes.groupby("Family")["Class"].apply(", ".join))

with st.expander(f"Input: {len(features)} flow features"):
    st.write(", ".join(features))

# ---- Models and their scores
st.subheader("Models trained (test set)")
table = pd.DataFrame({
    "Macro-F1": results["macro_f1"].round(4),
    "Attacks detected (%)": (100 * results["detection_rate"]).round(1),
    "False alarms (%)": (100 * results["false_alarm_rate"]).round(1),
    "Accuracy": results["accuracy"].round(4),
})
st.dataframe(table.sort_values("Macro-F1", ascending=False))

col1, col2 = st.columns(2)
for col, name, caption in [(col1, "08_confusion_matrix.png", "Confusion matrix of the best model"),
                           (col2, "08_f1_per_class.png", "F1-score per class and per model")]:
    if (FIG_DIR / name).exists():
        col.image(str(FIG_DIR / name), caption=caption)

# ---- Model picked
best = results.loc[MODEL_NAME]
st.subheader("Model picked: Random Forest")
st.markdown(f"""
- Best single model: macro-F1 **{best['macro_f1']:.3f}** (soft voting is about the same but needs 3 models)
- Fewest false alarms: **{100 * best['false_alarm_rate']:.1f}%** of normal flows flagged
- Detects **{100 * best['detection_rate']:.1f}%** of the attacks
- Fast to predict and explainable with SHAP
""")
st.caption("Main weakness: Infiltration flows look like normal traffic, so most false alarms come from that class.")