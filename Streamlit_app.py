import streamlit as st
import pandas as pd

# Load your processed data
df = pd.read_csv("UAC_processed.csv")

st.title("Care Transition Efficiency & Placement Outcome Analytics")

# Show KPIs
st.metric("Transfer Efficiency Ratio", round(df['Transfer Efficiency'].mean(), 2))
st.metric("Discharge Effectiveness Index", round(df['Discharge Effectiveness'].mean(), 2))
st.metric("Pipeline Throughput", round(df['Pipeline Throughput'].mean(), 2))
st.metric("Backlog Accumulation Rate", round(df['Inflow'].mean() - df['Exits'].mean(), 2))

# Simple chart example
st.line_chart(df[['Inflow','Exits']])
