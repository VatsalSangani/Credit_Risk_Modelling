from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import joblib, json

# ── load artefacts ────────────────────────────────────────────────
ARTIFACT_DIR = Path(__file__).resolve().parent.parent / "artifacts"
MODEL_PATH   = ARTIFACT_DIR / "gbm_credit_risk_model.pkl"
FEATS_PATH   = ARTIFACT_DIR / "gbm_features.json"

model    = joblib.load(MODEL_PATH)
FEATURES = json.loads(FEATS_PATH.read_text())

# ── FastAPI app ───────────────────────────────────────────────────
app = FastAPI(title="Credit-Risk API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# input schema (numbers only, categorical handled by Streamlit)
class Loan(BaseModel):
    person_age: int
    person_income: float
    person_emp_length: int
    loan_amnt: float
    loan_int_rate: float
    cb_person_cred_hist_length: int

    # one-hots
    person_home_ownership_OWN: int = 0
    person_home_ownership_RENT: int = 0
    person_home_ownership_OTHER: int = 0

    loan_intent_EDUCATION: int = 0
    loan_intent_HOMEIMPROVEMENT: int = 0
    loan_intent_MEDICAL: int = 0
    loan_intent_PERSONAL: int = 0
    loan_intent_VENTURE: int = 0

    loan_grade_C: int = 0
    loan_grade_D: int = 0
    loan_grade_E: int = 0
    loan_grade_F: int = 0
    loan_grade_G: int = 0

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: Loan):
    try:
        sample = data.dict()
        # derived feature
        sample["loan_percent_income"] = (
            sample["loan_amnt"] / sample["person_income"] * 100
            if sample["person_income"] > 0 else 0.0
        )

        df = pd.DataFrame([sample])
        for col in FEATURES:
            if col not in df:
                df[col] = 0
        df = df[FEATURES]

        prob = float(model.predict_proba(df)[0, 1])
        pred = int(model.predict(df)[0])
        return {"prediction": pred, "probability": round(prob, 4)}

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

