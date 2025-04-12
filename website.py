import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load Saved Model
with open('vehicle_price_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Load Transmission Encoder
with open('transmission_encoder.pkl', 'rb') as f:
    transmission_encoder = pickle.load(f)

# Title
st.title("Vehicle Price Prediction App")

# Input Fields
age = st.number_input("Vehicle Age (years)", min_value=0, max_value=50, value=5)
mileage = st.number_input("Mileage (in km)", min_value=0, value=50000)
cylinders = st.number_input("Number of Cylinders", min_value=2, max_value=16, value=4)
doors = st.number_input("Number of Doors", min_value=2, max_value=6, value=4)

fuel = st.selectbox("Fuel Type", ['Gasoline', 'Diesel', 'Electric', 'Hybrid', 'Unknown','PHEV Hybrid Fuel'])
body = st.selectbox("Body Type", ['SUV', 'Sedan', 'Hatchback', 'Pickup Truck', 'Coupe', 'Unknown', 'Passenger Van'])
transmission = st.selectbox("Transmission", transmission_encoder.classes_)
drivetrain = st.selectbox("Drivetrain", ['FWD', 'RWD', 'AWD', '4WD', 'Unknown'])
engine = st.text_input("Engine Type", "Unknown")
trim = st.text_input("Trim Level", "Unknown")
make_model = st.text_input("Make & Model", "Unknown")
exterior_color = st.text_input("Exterior Color", "Unknown")

# Convert transmission to encoded value
transmission_encoded = transmission_encoder.transform([transmission])[0]

# Create Input DataFrame
input_data = pd.DataFrame([[age, mileage, cylinders, doors, fuel, body, transmission_encoded, drivetrain, engine, trim, make_model, exterior_color]],
                          columns=['age', 'mileage', 'cylinders', 'doors', 'fuel', 'body', 'transmission', 'drivetrain', 'engine', 'trim', 'make_model', 'exterior_color'])

# Ensure Data Types are Correct
for col in ['fuel', 'body', 'drivetrain', 'engine', 'trim', 'make_model', 'exterior_color']:
    input_data[col] = input_data[col].astype(str)

# Fill Missing Values
input_data.fillna("Unknown", inplace=True)

# Predict
if st.button("Predict Price"):
    prediction = model.predict(input_data)
    st.success(f"Estimated Vehicle Price: ${prediction[0]:,.2f}")
