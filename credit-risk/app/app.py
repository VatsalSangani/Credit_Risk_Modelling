# ────────────────────────────────────────────────────────────────────────────────
# Credit-Risk scoring UI – Streamlit (calling FastAPI backend)
# author : you 😊
# ────────────────────────────────────────────────────────────────────────────────
import json
import requests
from pathlib import Path

import pandas as pd
import streamlit as st

# ----------------------------------------------------------------------
# 1. Streamlit config
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Credit-Risk Scoring",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("💳 Credit-Risk Scoring (Applicant default probability)")

user_vals = {}

# ----------------------------------------------------------------------
# 2. Sidebar Inputs – Clean UI
# ----------------------------------------------------------------------
st.sidebar.header("📋 Applicant / Loan Details")

numeric_fields = {
    "person_age": ("Person Age", 18, 75, 1),
    "person_income": ("Annual Income (USD)", 1000, 500000, 1000),
    "person_emp_length": ("Employment Length (Years)", 0, 40, 1),
    "loan_amnt": ("Loan Amount (USD)", 500, 50000, 500),
    "loan_int_rate": ("Interest Rate (%)", 0.0, 50.0, 0.1),
    "cb_person_cred_hist_length": ("Credit History Length (Years)", 0, 30, 1),
}

for col, (label, min_val, max_val, step) in numeric_fields.items():
    user_vals[col] = st.sidebar.number_input(label, min_value=min_val, max_value=max_val, step=step)

# Auto-calculate loan_percent_income
loan_amnt = user_vals["loan_amnt"]
income = user_vals["person_income"]
loan_pct = (loan_amnt / income * 100) if income > 0 else 0.0
user_vals["loan_percent_income"] = loan_pct

st.sidebar.markdown(f"📈 **Loan % of Income:** `{loan_pct:.2f}%`")

# Single-select categorical fields
home_opts = ["OWN", "RENT", "OTHER"]
intent_opts = ["EDUCATION", "HOMEIMPROVEMENT", "MEDICAL", "PERSONAL", "VENTURE"]
grade_opts = ["C", "D", "E", "F", "G"]

st.sidebar.subheader("🏠 Home Ownership")
home_choice = st.sidebar.radio("Select home ownership", home_opts, index=1)
for opt in home_opts:
    user_vals[f"person_home_ownership_{opt}"] = 1 if opt == home_choice else 0

st.sidebar.subheader("🎯 Loan Purpose")
intent_choice = st.sidebar.radio("Select loan purpose", intent_opts)
for opt in intent_opts:
    user_vals[f"loan_intent_{opt}"] = 1 if opt == intent_choice else 0

st.sidebar.subheader("🏷️ Loan Grade")
grade_choice = st.sidebar.radio("Select loan grade", grade_opts)
for grade in grade_opts:
    user_vals[f"loan_grade_{grade}"] = 1 if grade == grade_choice else 0

# ----------------------------------------------------------------------
# 3. Predict via FastAPI
# ----------------------------------------------------------------------
API_URL = "http://127.0.0.1:8000/predict"  # change if needed

if st.sidebar.button("✅ Predict default risk"):
    with st.spinner("Scoring…"):
        try:
            res = requests.post(API_URL, json=user_vals, timeout=10)
            res.raise_for_status()
            output = res.json()

            prob = output["probability"]
            pred = output["prediction"]

            st.markdown("## 🧾 Result")
            st.metric("Probability of default", f"{prob*100:.2f}%")
            st.write(
                "### Prediction",
                "❌ **High risk**" if pred else "✅ **Likely safe**"
            )

            st.markdown("---")
            st.caption("Future: Add SHAP force plots for individual prediction explanations.")

        except Exception as err:
            st.error("⚠️ Prediction failed — check backend/API.")
            st.code(str(err))
            with st.expander("Payload sent to API"):
                st.json(user_vals)
else:
    st.write(
        "👈 Adjust parameters in the sidebar and click **“Predict default risk”** "
        "to score an applicant."
    )

