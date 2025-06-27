# ────────────────────────────────────────────────────────────────────────────────
# Credit-Risk scoring UI  – Streamlit
# author : you 😊
# ────────────────────────────────────────────────────────────────────────────────
import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

# ------------------------------------------------------------------------------
# 1. Load artefacts
# ------------------------------------------------------------------------------
ARTIFACT_DIR = Path("artifacts")
MODEL_PATH   = ARTIFACT_DIR / "gbm_credit_risk_model.pkl"
FEATS_PATH   = ARTIFACT_DIR / "gbm_features.json"

model    = joblib.load(MODEL_PATH)
FEATURES = json.loads(FEATS_PATH.read_text())

# ------------------------------------------------------------------------------
# 2. Streamlit config
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Credit-Risk Scoring",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("💳 Credit-Risk Scoring (Applicant default probability)")

user_vals = {}

# ------------------------------------------------------------------------------
# 3. Sidebar Inputs – Clean UI
# ------------------------------------------------------------------------------
st.sidebar.header("📋 Applicant / Loan Details")

# Numeric inputs (excluding loan_percent_income)
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

# Single-selection (radio) for categorical features
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

# ------------------------------------------------------------------------------
# 4. Predict button
# ------------------------------------------------------------------------------
if st.sidebar.button("✅ Predict default risk"):
    X_inf = pd.DataFrame([user_vals])
    for col in FEATURES:
        if col not in X_inf:
            X_inf[col] = 0
    X_inf = X_inf[FEATURES]

    prob = float(model.predict_proba(X_inf)[0, 1])
    pred = int(model.predict(X_inf)[0])

    st.markdown("## 🧾 Result")
    st.metric("Probability of default", f"{prob:.2%}")
    st.write("### Prediction", "❌ **High risk**" if pred else "✅ **Likely safe**")

    st.markdown("---")
    st.caption("Future: Add SHAP force plots for individual prediction explanations.")
else:
    st.write(
        "👈 Adjust parameters in the sidebar and click **“Predict default risk”** "
        "to score an applicant."
    )
