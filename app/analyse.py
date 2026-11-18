import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from common import (RESPONSE, family, load_class_names, load_demo_flows, load_explainer,
                    load_features, load_model)

model = load_model()
class_names = load_class_names()
features = load_features()
demo = load_demo_flows()

st.title("🔍 Analyse a flow")
st.caption("Pick an unseen test flow and see what the model decides, and why.")

# ---- Pick a flow
choice = st.selectbox("Class to sample from", ["Random (any class)"] + class_names)

if st.button("Pick a random flow", type="primary") or "flow" not in st.session_state:
    if choice.startswith("Random"):
        pool = demo.index
    else:
        pool = demo.index[demo["Label"] == choice]
    st.session_state.flow = int(np.random.choice(pool))

i = st.session_state.flow
x = demo.loc[[i], features]
true_label = demo.loc[i, "Label"]

# ---- Prediction
proba = model.predict_proba(x)[0]
k = int(proba.argmax())
predicted = class_names[k]

left, right = st.columns(2)

with left:
    st.subheader(f"Flow #{i}")
    show = ["Dst Port", "Protocol", "Flow Duration", "Tot Fwd Pkts", "Tot Bwd Pkts", "Flow Byts/s", "Flow Pkts/s"]
    show = [c for c in show if c in features]
    st.dataframe(x[show].T.rename(columns={i: "value"}))

with right:
    if predicted == "Benign":
        st.success(f"Normal traffic (confidence {proba[k]:.1%})")
    else:
        st.error(f"ALERT: {predicted} [{family(predicted)}] (confidence {proba[k]:.1%})")

    if predicted == true_label:
        st.write(f"True label: **{true_label}** (correct)")
    else:
        st.write(f"True label: **{true_label}** (wrong)")

    st.info(f"Suggested response: {RESPONSE[family(predicted)]}")

    st.write("Model output (top 5 classes)")
    st.bar_chart(pd.Series(proba, index=class_names).sort_values(ascending=False).head(5), color="#FF4B4B")

# ---- Why this decision? (SHAP)
if st.checkbox("Show SHAP explanation"):
    import shap

    explainer = load_explainer()
    sv = explainer.shap_values(x)
    if isinstance(sv, list):                     # older SHAP versions: one array per class
        sv = np.stack(sv, axis=-1)
    base = np.atleast_1d(explainer.expected_value)

    explanation = shap.Explanation(values=sv[0, :, k], base_values=base[k] if len(base) > 1 else base[0],
                                   data=x.iloc[0].to_numpy(), feature_names=features)
    shap.plots.waterfall(explanation, max_display=10, show=False)
    st.pyplot(plt.gcf())
    plt.close("all")