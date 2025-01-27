import streamlit as st # type: ignore
import pandas as pd
import numpy as np
import joblib

# Load the trained model and scaler
model_path = "fitburn_model.pkl"  # Replace with your model file path
scaler_path = "scaler.pkl"        # Replace with your scaler file path
label_encoder_path = "label_encoder.pkl"  # Replace if using a saved label encoder

regressor = joblib.load(model_path)
scaler = joblib.load(scaler_path)
le = joblib.load(label_encoder_path)

# Streamlit App Title
st.title("FitBurn Predictor")
st.write("Provide your details to predict the calories burned.")

# User Inputs
uid = st.text_input("Enter User ID (not used in prediction):")

gender = st.radio("Select your gender:", ["Male", "Female"])
if(gender=="Male"):
    gender="male"
else :
    gender="female"
age = st.number_input("Enter your age:", min_value=0, max_value=120, value=25)
height = st.number_input("Enter your height (cm):", min_value=50.0, max_value=250.0, value=170.0)
weight = st.number_input("Enter your weight (kg):", min_value=10.0, max_value=200.0, value=70.0)
duration = st.number_input("Workout duration (hours):", min_value=0.0, max_value=10.0, value=1.0)
heart_rate = st.number_input("Heart rate after workout:", min_value=30.0, max_value=200.0, value=100.0)
body_temp = st.number_input("Body temperature after workout (°C):", min_value=30.0, max_value=45.0, value=37.0)

# Prepare the input data
if st.button("Predict"):
    user_data = [gender, age, height, weight, duration, heart_rate, body_temp]
    user_df = pd.DataFrame([user_data], columns=['Gender', 'Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp'])
    
    # Process categorical and numerical data
    user_df['Gender'] = le.transform(user_df['Gender'])
    data = np.array(user_df)
    data[:, 1:-1] = scaler.transform(data[:, 1:-1])
    
    # Predict calories burned
    prediction = regressor.predict(data)
    st.write(f"The predicted calories burned is: **{prediction[0]:.2f}**")
