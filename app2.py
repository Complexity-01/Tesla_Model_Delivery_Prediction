import streamlit as st
import pickle
import pandas as pd


# page configuration

st.set_page_config(page_title= "Tesla Model Predictor", layout = 'centered')


st.title("Tesla Model Estimate Delivery Indicator")
st.markdown("Enter Details for the prediction")

# loading preprocessor
with open(r'preprocessor2.pkl' , 'rb') as f:
    preprocessor = pickle.load(f)

# loading model
with open(r"model2.pkl" , 'rb') as f:
    model = pickle.load(f)


# input form

with st.form("prediction_form"):
    st.subheader("Details")


    col1, col2 = st.columns(2)

    with col1:
        years=list(range(2015,2026))
        Year = st.selectbox("Year",years)
        st.write("selected Year:",Year)
        
        month=list(range(1,13))
        Month = st.selectbox("Month",month)
        st.write("Selected month:", Month)


        Region = st.selectbox("Region",
                                options= ["Europe", "Asia","North America","Middle East"
                                                    ])

        Model = st.selectbox("Model",
                              options= ["Model S", "Model X","Model 3","Cybertruck","Model Y"])

        Production_Units = st.number_input("Production Units (50-30000)", min_value= 50, max_value= 30000, value= 70)
        

        Avg_Price_USD = st.number_input("Average Price in USD (50000-120000)", min_value=50000, max_value=120000, value=70000)
 

    with col2:

        Battery_Capacity_kWh = st.number_input("Battery Capacity in KWH (60-120)", min_value=60, max_value=120, value=70)

        Range_km = st.number_input("Range in KM (300-800)", min_value=300, max_value=800, value=700)

        CO2_Saved_tons = st.number_input("CO2 Saved Tons (0-2600)", min_value=0, max_value=2600, value=70)

        Source_Type = st.selectbox("Source Type",
                              options= ["Interpolated (Month)", "Official (Quarter)","Estimated (Region)"]) 

        Charging_Stations = st.number_input("Charging stations (3000-15000)", min_value=3000, max_value=15000, value=7000)                  



   
    submit_btn = st.form_submit_button("Predict Estimated Deliveries", type= 'primary')


# prediction logic

if submit_btn:
    # prepare dataframe
    input_data = pd.DataFrame({
    'Year': [Year],
    'Month': [Month],
    'Region': [Region],
    'Model': [Model],
    'Production_Units': [Production_Units],
    'Avg_Price_USD': [Avg_Price_USD],
    'Battery_Capacity_kWh': [Battery_Capacity_kWh],
    'Range_km': [Range_km],
    'CO2_Saved_tons': [CO2_Saved_tons],
    'Source_Type': [Source_Type],
    'Charging_Stations': [Charging_Stations],
})


    # preprocessing data
    data_scaled = preprocessor.transform(input_data)

    # predict

    prediction = model.predict(data_scaled)

    # display result


    st.success("Estimated Deliveries Status: **{:.2f}**".format(prediction[0]))




