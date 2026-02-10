import streamlit as st
import pandas as pd

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
plt.figure(figsize=(10,5))
plt.plot(df['Date'], df['Inflow'], label='Inflow', color='blue')
plt.plot(df['Date'], df['Exits'], label='Exits', color='orange')
plt.title("Inflow vs Exits Over Time")
plt.xlabel("Date")
plt.ylabel("Children")
plt.legend()
plt.show()

# Control chart: Discharge Effectiveness
plt.figure(figsize=(10,5))
plt.plot(df['Date'], df['Discharge Effectiveness'], marker='o', linestyle='-', color='green')
plt.axhline(mean_discharge, color='blue', linestyle='--', label='Mean')
plt.axhline(df['Upper Limit'].iloc[0], color='red', linestyle='--', label='Upper Limit')
plt.axhline(df['Lower Limit'].iloc[0], color='red', linestyle='--', label='Lower Limit')
plt.title("Discharge Effectiveness Control Chart")
plt.xlabel("Date")
plt.ylabel("Discharge Effectiveness")
plt.legend()
plt.show()

