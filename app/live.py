import time

import numpy as np
import pandas as pd
import streamlit as st

from common import load_class_names, load_demo_flows, load_features, load_model

model = load_model()
class_names = np.array(load_class_names())
features = load_features()
demo = load_demo_flows()

st.title("📡 Live traffic simulation")
st.caption("Unseen flows arrive in batches; the model classifies each batch and raises alerts.")

# ---- Settings
c1, c2, c3, c4 = st.columns(4)
n_batches = c1.slider("Number of batches", 1, 30, 10)
batch_size = c2.slider("Flows per batch", 10, 200, 50)
benign_share = c3.slider("Share of Benign traffic (%)", 0, 100, 70)
delay = c4.slider("Delay between batches (s)", 0.0, 2.0, 0.5)

start = st.button("Start", type="primary")

# Empty boxes, filled while the simulation runs
progress = st.progress(0)
metrics_box = st.empty()
log_col, chart_col = st.columns(2)
log_box = log_col.empty()
chart_box = chart_col.empty()

if start:
    benign_rows = demo.index[demo["Label"] == "Benign"]
    attack_rows = demo.index[demo["Label"] != "Benign"]
    n_benign = int(batch_size * benign_share / 100)

    total = alerts = missed = false_alarms = 0
    log = []
    alert_types = pd.Series(dtype=int)

    for b in range(1, n_batches + 1):
        # Build a batch with the chosen share of Benign flows
        rows = np.concatenate([np.random.choice(benign_rows, n_benign),
                               np.random.choice(attack_rows, batch_size - n_benign)])
        true = demo.loc[rows, "Label"].to_numpy()
        pred = class_names[model.predict(demo.loc[rows, features])]

        # Update the counters
        is_attack, pred_attack = true != "Benign", pred != "Benign"
        total += len(rows)
        alerts += pred_attack.sum()
        missed += (is_attack & ~pred_attack).sum()
        false_alarms += (~is_attack & pred_attack).sum()

        batch_alerts = pd.Series(pred[pred_attack]).value_counts()
        alert_types = alert_types.add(batch_alerts, fill_value=0)
        top3 = ", ".join(f"{name} ×{n}" for name, n in batch_alerts.head(3).items())
        log.append({"Time": time.strftime("%H:%M:%S"), "Batch": b,
                    "Alerts": int(pred_attack.sum()), "Main attack types": top3})

        # Refresh the display
        progress.progress(b / n_batches, text=f"Batch {b} / {n_batches}")
        with metrics_box.container():
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Flows analysed", total)
            m2.metric("Alerts raised", int(alerts))
            m3.metric("Attacks missed", int(missed))
            m4.metric("False alarms", int(false_alarms))
        log_box.dataframe(pd.DataFrame(log[::-1]), hide_index=True)
        chart_box.bar_chart(alert_types.sort_values(ascending=False), color="#FF4B4B")

        time.sleep(delay)