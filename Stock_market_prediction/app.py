import streamlit as st
import pandas as pd
from predictiom import predict_next

st.title("📈 TSLA Stock Price Predictor")

price = predict_next()
st.success(f"Predicted TSLA Closing Price: ${price:.2f}")

st.header("📅 Prediction Log")
log = pd.read_csv("prediction_log.csv")
st.dataframe(log)

if 'Actual_Price' in log.columns:
    st.header("📉 Predicted vs Actual Prices")
    st.line_chart(log[['Predicted_Price', 'Actual_Price']])
