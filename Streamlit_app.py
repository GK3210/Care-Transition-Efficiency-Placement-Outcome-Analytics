import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your processed data
df = pd.read_csv("UAC_processed.csv")

st.title("Care Transition Efficiency & Placement Outcome Analytics")
st.write("This dashboard analyzes the child care pipeline using KPIs and visualizations.")

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Transfer Efficiency", round(df['Transfer Efficiency'].mean(), 2))
col2.metric("Discharge Effectiveness", round(df['Discharge Effectiveness'].mean(), 2))
col3.metric("Pipeline Throughput", round(df['Pipeline Throughput'].mean(), 2))
col4.metric("Backlog Rate", round((df['Inflow'].mean() - df['Exits'].mean()), 2))

# Line Chart: Inflow vs Exits
st.subheader("Inflow vs Exits Over Time")
st.line_chart(df[['Inflow', 'Exits']])

# Control Chart: Discharge Effectiveness
st.subheader("Discharge Effectiveness Control Chart")
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(df['Date'], df['Discharge Effectiveness'], marker='o', linestyle='-', color='green')
ax.axhline(df['Discharge Effectiveness'].mean(), color='blue', linestyle='--', label='Mean')
ax.axhline(df['Upper Limit'].iloc[0], color='red', linestyle='--', label='Upper Limit')
ax.axhline(df['Lower Limit'].iloc[0], color='red', linestyle='--', label='Lower Limit')
ax.set_xlabel("Date")
ax.set_ylabel("Discharge Effectiveness")
ax.legend()
st.pyplot(fig)
