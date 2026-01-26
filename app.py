import streamlit as st
import pandas as pd
import pickle

# Load trained pipeline
with open("churn_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="Customer Churn Predictor", layout="centered")

st.title("📊 Customer Churn Prediction")
st.write("Enter customer details to predict churn")

# ---------------- INPUTS ----------------

state = st.selectbox(
    "State",
    [
        'KS','OH','NJ','OK','AL','MA','MO','LA','WV','IN','RI','IA','MT','NY',
        'ID','VT','VA','TX','FL','CO','AZ','SC','NE','WY','HI','IL','NH','GA',
        'AK','MD','AR','WI','OR','MI','DE','UT','CA','MN','SD','NC','WA','NM',
        'NV','DC','KY','ME','MS','TN','PA','CT','ND'
    ]
)

# ✅ KEEP AS STRING (VERY IMPORTANT)
area_code = st.selectbox("Area Code", ["408", "415", "510"])

account_length = st.number_input("Account Length", min_value=1, value=250)

voice_plan = st.selectbox("Voice Plan", ["yes", "no"])
voice_messages = st.number_input("Voice Messages", min_value=0, value=60)

intl_plan = st.selectbox("International Plan", ["yes", "no"])
intl_mins = st.number_input("International Minutes", value=40.0)
intl_calls = st.number_input("International Calls", value=20)
intl_charge = st.number_input("International Charge", value=20.0)

day_mins = st.number_input("Day Minutes", value=300.0)
day_calls = st.number_input("Day Calls", value=150)
day_charge = st.number_input("Day Charge", value=30.0)

eve_mins = st.number_input("Evening Minutes", value=200.0)
eve_calls = st.number_input("Evening Calls", value=150)
eve_charge = st.number_input("Evening Charge", value=30.0)

night_mins = st.number_input("Night Minutes", value=150.0)
night_calls = st.number_input("Night Calls", value=150)
night_charge = st.number_input("Night Charge", value=30.0)

customer_calls = st.number_input(
    "Customer Service Calls", min_value=0, max_value=10, value=1
)

# ---------------- DATAFRAME ----------------

input_df = pd.DataFrame([{
    "state": state,
    "area.code": area_code,   # STRING — MATCH TRAINING
    "account.length": account_length,
    "voice.plan": voice_plan,
    "voice.messages": voice_messages,
    "intl.plan": intl_plan,
    "intl.mins": intl_mins,
    "intl.calls": intl_calls,
    "intl.charge": intl_charge,
    "day.mins": day_mins,
    "day.calls": day_calls,
    "day.charge": day_charge,
    "eve.mins": eve_mins,
    "eve.calls": eve_calls,
    "eve.charge": eve_charge,
    "night.mins": night_mins,
    "night.calls": night_calls,
    "night.charge": night_charge,
    "customer.calls": customer_calls
}])

# ---------------- PREDICTION ----------------

if st.button("Predict Churn"):
    prob = model.predict_proba(input_df)[0][1]

    if prob >= 0.5:
        st.error(f"❌ Customer WILL churn (Probability: {prob:.2f})")
    else:
        st.success(f"✅ Customer will NOT churn (Probability: {prob:.2f})")
