import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load model and columns
model = joblib.load('model.pkl')
model_columns = joblib.load('model_columns.pkl')

st.set_page_config(page_title="Delivery Time Predictor", page_icon="🚚")
st.title("🚚 Delivery Time Prediction")
st.write("Enter the details below to predict how long the delivery will take.")

# --- Input fields ---
distance = st.number_input("Distance (km)", min_value=0.0, value=5.0, step=0.1)
prep_time = st.number_input("Preparation Time (minutes)", min_value=0, value=15, step=1)
experience = st.number_input("Courier Experience (years)", min_value=0.0, value=2.0, step=0.5)

weather = st.selectbox("Weather", ["Sunny", "Rainy", "Foggy", "Windy", "Cloudy"])
traffic = st.selectbox("Traffic Level", ["Low", "Medium", "High"])
time_of_day = st.selectbox("Time of Day", ["Morning", "Afternoon", "Evening", "Night"])
vehicle = st.selectbox("Vehicle Type", ["Bike", "Scooter", "Motorcycle", "Car"])

if st.button("Predict Delivery Time"):
    # Create input dataframe
    input_df = pd.DataFrame({
        'Distance_km': [distance],
        'Preparation_Time_min': [prep_time],
        'Courier_Experience_yrs': [experience],
        'Weather': [weather],
        'Traffic_Level': [traffic],
        'Time_of_Day': [time_of_day],
        'Vehicle_Type': [vehicle]
    })

    # One-hot encode
    input_encoded = pd.get_dummies(input_df)

    # Add engineered features
    input_encoded['Distance_per_Exp'] = input_encoded['Distance_km'] / (input_encoded['Courier_Experience_yrs'] + 1)
    input_encoded['Prep_plus_Distance'] = input_encoded['Preparation_Time_min'] + input_encoded['Distance_km']

    # Force the columns to match exactly what the model expects
    input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)

    # Predict
    try:
        prediction = model.predict(input_encoded)[0]
        st.success(f"**Predicted Delivery Time: {prediction:.1f} minutes**")
        st.balloons()
    except Exception as e:
        st.error("Prediction failed. Please check the category values.")
        st.write("Error details:", str(e))