import streamlit as st
import pickle
import numpy as np

# --------------------------------------------------
# 1. Load the Model & Scaler
# --------------------------------------------------
model  = pickle.load(open("model_base_1.pkl",      "rb"))
scaler = pickle.load(open("standard_scaler.pkl", "rb"))

# --------------------------------------------------
# 2. Title and Description
# --------------------------------------------------
st.title("Health Insurance Fraud Detection")
st.write("""
This app predicts whether a health insurance claim is **potentially fraudulent**
based on various features. Please fill out **all** the relevant details below.
""")

# --------------------------------------------------
# 3. Provider ID Input
# --------------------------------------------------
provider_id = st.text_input("Provider ID", value="")

# --------------------------------------------------
# 4. Collect Feature Inputs
# --------------------------------------------------
# 4.1 Claim financials
st.header("1) Claim Financials")
InscClaimAmtReimbursed = st.number_input("InscClaimAmtReimbursed", min_value=0, value=500)
DeductibleAmtPaid      = st.number_input("DeductibleAmtPaid",      min_value=0, value=50)

# 4.2 Timing features
st.header("2) Claim Timing Features")
Hospitalization_Duration = st.number_input("Hospitalization_Duration (days)", min_value=0, value=5)
Claim_Period             = st.number_input("Claim_Period (days)",           min_value=0, value=10)
ExtraClaimDays           = st.number_input("ExtraClaimDays",               min_value=0, value=0)
InOut                    = st.selectbox("Inpatient or Outpatient", ["Outpatient (0)", "Inpatient (1)"], index=0)
Inpatient_or_Outpatient_val = 1 if InOut.startswith("Inpatient") else 0

# 4.3 Coverage & renal indicator
st.header("3) Coverage & Renal")
RenalChoice = st.selectbox("RenalDiseaseIndicator", ["No (0)", "Yes (1)"], index=0)
RenalDiseaseIndicator_val = 1 if RenalChoice.startswith("Yes") else 0
NoOfMonths_PartACov = st.number_input("NoOfMonths_PartACov", min_value=0, value=10)
NoOfMonths_PartBCov = st.number_input("NoOfMonths_PartBCov", min_value=0, value=12)

# 4.4 Chronic conditions
st.header("4) Chronic Conditions")
conds = [
    'Alzheimer','Heartfailure','KidneyDisease','Cancer',
    'ObstrPulmonary','Depression','Diabetes','IschemicHeart',
    'Osteoporasis','rheumatoidarthritis','stroke'
]
cond_vals = {}
for cond in conds:
    choice = st.selectbox(f"ChronicCond_{cond}", ["No (0)", "Yes (1)"], index=0)
    cond_vals[cond] = 1 if choice.startswith("Yes") else 0

# 4.5 Demographics & Risk
st.header("5) Demographics & Risk")
Patient_Risk_Score = st.number_input("Patient_Risk_Score", min_value=0, value=3)
Patient_Age        = st.number_input("Patient_Age",         min_value=0, value=70)
dead_choice        = st.selectbox("isDead", ["No (0)", "Yes (1)"], index=0)
isDead_val         = 1 if dead_choice.startswith("Yes") else 0

# 4.6 Aggregated amounts
st.header("6) Aggregated Financial Totals")
IP_OP_TotalReimbursementAmt = st.number_input("IP_OP_TotalReimbursementAmt",   min_value=0, value=10300)
IP_OP_AnnualDeductibleAmt   = st.number_input("IP_OP_AnnualDeductibleAmt",     min_value=0, value=750)

# 4.7 One‐hot: Gender & Race
st.header("7) Gender & Race (One‐Hot)")
Gender_0 = int(st.selectbox("Gender_0 (Female)", ["0","1"], index=0))
Gender_1 = int(st.selectbox("Gender_1 (Male)",   ["0","1"], index=1))
Race_1   = int(st.selectbox("Race_1", ["0","1"], index=1))
Race_2   = int(st.selectbox("Race_2", ["0","1"], index=0))
Race_3   = int(st.selectbox("Race_3", ["0","1"], index=0))
Race_5   = int(st.selectbox("Race_5", ["0","1"], index=0))

# --------------------------------------------------
# 5. Prepare & Scale Data for Model
# --------------------------------------------------
features = [
    InscClaimAmtReimbursed,
    DeductibleAmtPaid,
    Hospitalization_Duration,
    Claim_Period,
    ExtraClaimDays,
    Inpatient_or_Outpatient_val,
    RenalDiseaseIndicator_val,
    NoOfMonths_PartACov,
    NoOfMonths_PartBCov,
] + [cond_vals[c] for c in conds] + [
    Patient_Risk_Score,
    Patient_Age,
    isDead_val,
    IP_OP_TotalReimbursementAmt,
    IP_OP_AnnualDeductibleAmt,
    Gender_0,
    Gender_1,
    Race_1,
    Race_2,
    Race_3,
    Race_5
]

# sanity check
assert len(features) == model.n_features_in_, (
    f"❌ Expected {model.n_features_in_} features but got {len(features)}"
)

input_data = np.array(features).reshape(1, -1)
input_data = scaler.transform(input_data)

# --------------------------------------------------
# 6. Predict & Display
# --------------------------------------------------
if st.button("Predict Fraud"):
    pred_class, probs = model.predict(input_data)[0], model.predict_proba(input_data)[0]
    label       = "Fraud" if pred_class == 1 else "Genuine"
    probability = probs[pred_class]

    if pred_class == 1:
        st.error(
            f"The Claim made by {provider_id} is a **Fraud** claim "
            f"with **{probability*100:.2f}%** probability."
        )
    else:
        st.success(
            f"The Claim made by {provider_id} is a **Genuine** claim "
            f"with **{probability*100:.2f}%** probability."
        )
