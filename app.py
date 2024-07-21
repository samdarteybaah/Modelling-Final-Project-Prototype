

import streamlit as st
from keras.models import load_model
from tensorflow import saved_model
from sklearn.preprocessing import StandardScaler
import pickle
import pandas as pd

#loading the scaler
with open('scaler.pkl', 'rb') as scaler_file:
    loaded_scaler = pickle.load(scaler_file)

#loading the model
tuned_model = load_model('tuned_model.h5')
#load_model

# title for the model 
st.title("IMS Final Project: A Engine Failure Detection Model")

st.header("Input the following features")

Engine_rpm =st.number_input("Engine rpm", min_value=0, max_value=1500, step=1, value=0)
Lub_oil_pressure =st.number_input("Lub oil pressure (in Pound per square inch)", min_value=0.0, max_value=15.0, step=1.0, value=0.0)
Fuel_pressure =st.number_input("Fuel pressure (in Pound per square inch)", min_value=0.0, max_value=35.0, step=1.0, value=0.0)
Coolant_pressure =st.number_input("Coolant pressure (in Pound per square inch)", min_value=0.0, max_value=15.0, step=1.0, value=0.0)
lub_oil_temp =st.number_input("Lube oil temp (in Celsuis)", min_value=20.0, max_value=150.0, step=1.0, value=20.0)
Coolant_temp =st.number_input("Coolant temp (in Celsuis)", min_value=20.0, max_value=150.0, step=1.0, value=20.0)

#creating a dataframe
if st.button("Submit"): 
    user_input = pd.DataFrame({
        'Engine rpm': [Engine_rpm],
        'Lub oil pressure': [Lub_oil_pressure],
        'Fuel pressure': [Fuel_pressure],
        'Coolant pressure': [Coolant_pressure],
        'lub oil temp': [lub_oil_temp],
        'Coolant temp': [Coolant_temp]
    })

    # scaling the data input
    StandardScaler = loaded_scaler
    needed_features = ['Engine rpm', 'Lub oil pressure', 'Fuel pressure', 'Coolant pressure', 'lub oil temp', 'Coolant temp']
    user_input_scaled = StandardScaler.transform(user_input[needed_features])
    user_input_scaled_df = pd.DataFrame(user_input_scaled, columns=needed_features)

    #  using the tuned model to make predictions
    prediction = tuned_model.predict(user_input_scaled_df)

    # Displaying the prediction
    st.subheader("Prediction")
    engine_condition = "The engine is in bad condition" if prediction[0, 0] > 0.5 else "The engine is in good condition"
    confidence_score = prediction[0, 0]
    st.write(f"The predicted engine condition is: {engine_condition}")
    st.write(f"Confidence Score: {confidence_score:.2%}")
