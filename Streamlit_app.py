import streamlit as st
import pandas as pd
import streamlit as st

st.title("Care Transition Efficiency & Placement Outcome Analytics")
st.write("✅ Streamlit app is running successfully!")

# Example chart
st.line_chart({"Inflow":[10,20,30], "Exits":[5,15,25]})


# -------------------------------
# Step 1: Load and Clean the Data
# -------------------------------
df = pd.read_csv("HHS_Unaccompanied_Alien_Children_Program.csv")

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Remove commas and convert numeric columns to integers
numeric_cols = [
    "Children apprehended and placed in CBP custody*",
    "Children in CBP custody",
    "Children transferred out of CBP custody",
    "Children in HHS Care",
    "Children discharged from HHS Care"
]
for col in numeric_cols:
    df[col] = df[col].astype(str).str.replace(",", "").replace("nan", "0").astype(float)

# -------------------------------
# Step 2: Calculate Metrics
# -------------------------------
df['Transfer Efficiency'] = df['Children transferred out of CBP custody'] / df['Children in CBP custody']
df['Discharge Effectiveness'] = df['Children discharged from HHS Care'] / df['Children in HHS Care']
df['Pipeline Throughput'] = (
    (df['Children transferred out of CBP custody'] + df['Children discharged from HHS Care']) /
    (df['Children apprehended and placed in CBP custody*'] + df['Children in CBP custody'])
)

# Inflow vs Exits for backlog analysis
df['Inflow'] = df['Children apprehended and placed in CBP custody*'] + df['Children in CBP custody']
df['Exits'] = df['Children transferred out of CBP custody'] + df['Children discharged from HHS Care']

# -------------------------------
# Step 3: Temporal Analysis
# -------------------------------
df['Weekday'] = df['Date'].dt.day_name()
df['Month'] = df['Date'].dt.to_period('M')

# Rolling averages for backlog detection
df['Inflow_Rolling'] = df['Inflow'].rolling(7).mean()
df['Exits_Rolling'] = df['Exits'].rolling(7).mean()

# -------------------------------
# Step 4: Outcome Stability
# -------------------------------
mean_discharge = df['Discharge Effectiveness'].mean()
std_discharge = df['Discharge Effectiveness'].std()
df['Upper Limit'] = mean_discharge + 2 * std_discharge
df['Lower Limit'] = mean_discharge - 2 * std_discharge

# -------------------------------
# Step 5: Export Processed Data
# -------------------------------
df.to_csv("UAC_processed.csv", index=False)

# -------------------------------
# Step 6: Example Visualizations
# -------------------------------
# Line chart: Inflow vs Exits

# Control chart: Discharge Effectiveness


