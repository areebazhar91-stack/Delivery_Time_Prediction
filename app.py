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

# Input fields
distance = st.number_input("Distance (km)", min_value=0.0, value=5.0, step=0.1)
prep_time = st.number_input("Preparation Time (minutes)", min_value=0, value=15, step=1)
experience = st.number_input("Courier Experience (years)", min_value=0.0, value=2.0, step=0.5)

weather = st.selectbox("Weather", ["Windy", "Clear", "Foggy", "Rainy", "Snowy"])
traffic = st.selectbox("Traffic Level", ["Low", "Medium", "High"])
time_of_day = st.selectbox("Time of Day", ["Afternoon", "Evening", "Night", "Morning"])
vehicle = st.selectbox("Vehicle Type", ["Scooter", "Bike", "Car"])

if st.button("Predict Delivery Time"):

    # Create a dictionary with ALL expected columns set to 0
    data = {col: 0 for col in model_columns}

    # Fill the numeric columns
    data['Distance_km'] = distance
    data['Preparation_Time_min'] = prep_time
    data['Courier_Experience_yrs'] = experience
    data['Distance_per_Exp'] = distance / (experience + 1)
    data['Prep_plus_Distance'] = prep_time + distance

    # Set the correct dummy columns to 1
    if weather == "Foggy":
        data['Weather_Foggy'] = 1
    elif weather == "Rainy":
        data['Weather_Rainy'] = 1
    elif weather == "Snowy":
        data['Weather_Snowy'] = 1
    elif weather == "Windy":
        data['Weather_Windy'] = 1
    # "Clear" stays 0 (it was the dropped category)

    if traffic == "Low":
        data['Traffic_Level_Low'] = 1
    elif traffic == "Medium":
        data['Traffic_Level_Medium'] = 1
    # "High" stays 0

    if time_of_day == "Evening":
        data['Time_of_Day_Evening'] = 1
    elif time_of_day == "Morning":
        data['Time_of_Day_Morning'] = 1
    elif time_of_day == "Night":
        data['Time_of_Day_Night'] = 1
    # "Afternoon" stays 0

    if vehicle == "Car":
        data['Vehicle_Type_Car'] = 1
    elif vehicle == "Scooter":
        data['Vehicle_Type_Scooter'] = 1
    # "Bike" stays 0

    # Create dataframe in the exact column order
    input_encoded = pd.DataFrame([data], columns=model_columns)

    # Predict
    prediction = model.predict(input_encoded)[0]
    st.success(f"**Predicted Delivery Time: {prediction:.1f} minutes**")
    st.balloons()