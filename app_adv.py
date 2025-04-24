import streamlit as st
import pickle
import numpy as np

# --------------------------------------------------
# 1. Load the Model and (Optionally) the Scaler
# --------------------------------------------------
# Make sure model.pkl is in the same directory, or use a full path.
model = pickle.load(open("model.pkl", "rb"))

# If you used a StandardScaler (or other scaler) during training,
# load it here. Otherwise, remove the scaler lines.
# scaler = pickle.load(open("scaler.pkl", "rb"))

# --------------------------------------------------
# 2. Title and Description
# --------------------------------------------------
st.title("Health Insurance Fraud Detection")
st.write("""
This app predicts whether a health insurance claim is **potentially fraudulent** based on various features.
Please fill out **all** the relevant details below.
""")

# --------------------------------------------------
# 3. Collect Feature Inputs from the User
# --------------------------------------------------
# NOTE: The features below are representative of those
# in your final dataset. Adjust to match your actual columns,
# especially if you have more or fewer columns.

# 3.1 Basic numeric features
st.header("1) Basic Claim Features")

InscClaimAmtReimbursed = st.number_input(
    label="InscClaimAmtReimbursed (Reimbursed amount for this claim)",
    min_value=0, max_value=1_000_000, value=500, step=1
)

DeductibleAmtPaid = st.number_input(
    label="DeductibleAmtPaid (Amount the patient paid)",
    min_value=0, max_value=1_000_000, value=50, step=1
)

IPAnnualReimbursementAmt = st.number_input(
    label="IPAnnualReimbursementAmt (Annual inpatient reimbursement)",
    min_value=0, max_value=1_000_000, value=10_000, step=100
)

OPAnnualReimbursementAmt = st.number_input(
    label="OPAnnualReimbursementAmt (Annual outpatient reimbursement)",
    min_value=0, max_value=1_000_000, value=300, step=10
)

IPAnnualDeductibleAmt = st.number_input(
    label="IPAnnualDeductibleAmt (Annual inpatient deductible)",
    min_value=0, max_value=1_000_000, value=500, step=10
)

OPAnnualDeductibleAmt = st.number_input(
    label="OPAnnualDeductibleAmt (Annual outpatient deductible)",
    min_value=0, max_value=1_000_000, value=250, step=10
)


# 3.2 Beneficiary / Patient features
st.header("2) Patient / Beneficiary Features")

NoOfMonths_PartACov = st.number_input(
    label="NoOfMonths_PartACov (Months of Part A coverage)",
    min_value=0, max_value=120, value=10, step=1
)

NoOfMonths_PartBCov = st.number_input(
    label="NoOfMonths_PartBCov (Months of Part B coverage)",
    min_value=0, max_value=120, value=12, step=1
)

Patient_Age = st.number_input(
    label="Patient_Age (in years)",
    min_value=0, max_value=120, value=70, step=1
)

Patient_Risk_Score = st.number_input(
    label="Patient_Risk_Score (sum of chronic conditions)",
    min_value=0, max_value=12, value=3, step=1
)

isDead = st.selectbox(
    label="Is the patient deceased? (isDead)",
    options=["No (0)", "Yes (1)"],
    index=0
)
isDead_val = 1 if isDead == "Yes (1)" else 0


# 3.3 Chronic conditions
st.header("3) Chronic Conditions")
ChronicCond_Alzheimer = st.selectbox("ChronicCond_Alzheimer", ["No (0)", "Yes (1)"], index=0)
ChronicCond_Heartfailure = st.selectbox("ChronicCond_Heartfailure", ["No (0)", "Yes (1)"], index=0)
ChronicCond_KidneyDisease = st.selectbox("ChronicCond_KidneyDisease", ["No (0)", "Yes (1)"], index=0)
ChronicCond_Cancer = st.selectbox("ChronicCond_Cancer", ["No (0)", "Yes (1)"], index=0)
ChronicCond_ObstrPulmonary = st.selectbox("ChronicCond_ObstrPulmonary", ["No (0)", "Yes (1)"], index=0)
ChronicCond_Depression = st.selectbox("ChronicCond_Depression", ["No (0)", "Yes (1)"], index=0)
ChronicCond_Diabetes = st.selectbox("ChronicCond_Diabetes", ["No (0)", "Yes (1)"], index=0)
ChronicCond_IschemicHeart = st.selectbox("ChronicCond_IschemicHeart", ["No (0)", "Yes (1)"], index=0)
ChronicCond_Osteoporasis = st.selectbox("ChronicCond_Osteoporasis", ["No (0)", "Yes (1)"], index=0)
ChronicCond_rheumatoidarthritis = st.selectbox("ChronicCond_rheumatoidarthritis", ["No (0)", "Yes (1)"], index=0)
ChronicCond_stroke = st.selectbox("ChronicCond_stroke", ["No (0)", "Yes (1)"], index=0)
RenalDiseaseIndicator = st.selectbox("RenalDiseaseIndicator", ["No (0)", "Yes (1)"], index=0)

# Convert these selects to numeric 0/1
ChronicCond_Alzheimer_val = 1 if ChronicCond_Alzheimer == "Yes (1)" else 0
ChronicCond_Heartfailure_val = 1 if ChronicCond_Heartfailure == "Yes (1)" else 0
ChronicCond_KidneyDisease_val = 1 if ChronicCond_KidneyDisease == "Yes (1)" else 0
ChronicCond_Cancer_val = 1 if ChronicCond_Cancer == "Yes (1)" else 0
ChronicCond_ObstrPulmonary_val = 1 if ChronicCond_ObstrPulmonary == "Yes (1)" else 0
ChronicCond_Depression_val = 1 if ChronicCond_Depression == "Yes (1)" else 0
ChronicCond_Diabetes_val = 1 if ChronicCond_Diabetes == "Yes (1)" else 0
ChronicCond_IschemicHeart_val = 1 if ChronicCond_IschemicHeart == "Yes (1)" else 0
ChronicCond_Osteoporasis_val = 1 if ChronicCond_Osteoporasis == "Yes (1)" else 0
ChronicCond_rheumatoidarthritis_val = 1 if ChronicCond_rheumatoidarthritis == "Yes (1)" else 0
ChronicCond_stroke_val = 1 if ChronicCond_stroke == "Yes (1)" else 0
RenalDiseaseIndicator_val = 1 if RenalDiseaseIndicator == "Yes (1)" else 0


# 3.4 Inpatient/Outpatient Timings
st.header("4) Claim Timings")
Hospitalization_Duration = st.number_input(
    label="Hospitalization_Duration (days)",
    min_value=0, max_value=365, value=5, step=1
)

Claim_Period = st.number_input(
    label="Claim_Period (days from ClaimStartDt to ClaimEndDt)",
    min_value=0, max_value=365, value=10, step=1
)

ExtraClaimDays = st.number_input(
    label="ExtraClaimDays (Claim_Period - Hospitalization_Duration if > 0)",
    min_value=0, max_value=365, value=0, step=1
)


# 3.5 Gender / Race (One-Hot Encoded)
st.header("5) Gender & Race (One-Hot Encoded)")
Gender_0 = st.selectbox("Gender_0 (Female=0)", ["0", "1"], index=0)
Gender_1 = st.selectbox("Gender_1 (Male=1)", ["0", "1"], index=1)

# Race can have multiple columns if one-hot encoded (Race_1, Race_2, Race_3, Race_5, etc.).
Race_1 = st.selectbox("Race_1", ["0", "1"], index=1)
Race_2 = st.selectbox("Race_2", ["0", "1"], index=0)
Race_3 = st.selectbox("Race_3", ["0", "1"], index=0)
Race_5 = st.selectbox("Race_5", ["0", "1"], index=0)

# Convert to int
Gender_0_val = int(Gender_0)
Gender_1_val = int(Gender_1)
Race_1_val = int(Race_1)
Race_2_val = int(Race_2)
Race_3_val = int(Race_3)
Race_5_val = int(Race_5)

# 3.6 Additional aggregated columns (if any)
# Because your code does many group-by transformations, you might have additional columns
# like: PerProvider_mean_InscClaimAmtReimbursed, PerBeneID_mean_..., etc.
# For demonstration, let's show how you'd do one or two:
st.header("6) Grouped/Aggregated Features (Example)")

PerProvider_mean_InscClaimAmtReimbursed = st.number_input(
    label="PerProvider_mean_InscClaimAmtReimbursed",
    min_value=0.0, max_value=1_000_000.0, value=600.0, step=50.0
)

PerBeneID_mean_InscClaimAmtReimbursed = st.number_input(
    label="PerBeneID_mean_InscClaimAmtReimbursed",
    min_value=0.0, max_value=1_000_000.0, value=700.0, step=50.0
)

# Add more if your model needs them...

# --------------------------------------------------
# 4. Prepare Data for Model
# --------------------------------------------------
# Build a list/array of features in EXACTLY the same order
# the model expects. If you have ~100+ features, keep them
# in the same order as in your final training code.

features = [
    InscClaimAmtReimbursed,
    DeductibleAmtPaid,
    IPAnnualReimbursementAmt,
    IPAnnualDeductibleAmt,
    OPAnnualReimbursementAmt,
    OPAnnualDeductibleAmt,
    NoOfMonths_PartACov,
    NoOfMonths_PartBCov,
    Patient_Age,
    Patient_Risk_Score,
    isDead_val,
    ChronicCond_Alzheimer_val,
    ChronicCond_Heartfailure_val,
    ChronicCond_KidneyDisease_val,
    ChronicCond_Cancer_val,
    ChronicCond_ObstrPulmonary_val,
    ChronicCond_Depression_val,
    ChronicCond_Diabetes_val,
    ChronicCond_IschemicHeart_val,
    ChronicCond_Osteoporasis_val,
    ChronicCond_rheumatoidarthritis_val,
    ChronicCond_stroke_val,
    RenalDiseaseIndicator_val,
    Hospitalization_Duration,
    Claim_Period,
    ExtraClaimDays,
    Gender_0_val,
    Gender_1_val,
    Race_1_val,
    Race_2_val,
    Race_3_val,
    Race_5_val,
    PerProvider_mean_InscClaimAmtReimbursed,
    PerBeneID_mean_InscClaimAmtReimbursed
    # ... If your model has more aggregator columns,
    # add them here in the right order ...
]

# Convert to numpy array and reshape for model
input_data = np.array(features).reshape(1, -1)

# If a scaler was used, apply it:
# input_data = scaler.transform(input_data)

# --------------------------------------------------
# 5. Predict with Model
# --------------------------------------------------
if st.button("Predict Fraud"):
    prediction = model.predict(input_data)
    
    # Usually, 1 = Fraud, 0 = Not Fraud.
    if prediction[0] == 1:
        st.error("**The claim is predicted to be Fraudulent.**")
    else:
        st.success("**The claim is predicted to be Non-Fraudulent.**")
