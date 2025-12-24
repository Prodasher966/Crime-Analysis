# Crime Dashboard in Streamlit using Plotly, Matplotlib, Seaborn, and Pandas

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
from prophet import Prophet
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Set Streamlit page config
st.set_page_config(page_title="Crime Dashboard", layout="wide")

# Load and preprocess data
@st.cache_data
def load_data():
    data = pd.read_csv("Crime_Data_from_2020_to_Present.csv", parse_dates=['DATE OCC'], low_memory=False)
    data = data.dropna(subset=['LAT', 'LON', 'Vict Age'])
    data['Vict Age'] = pd.to_numeric(data['Vict Age'], errors='coerce')
    data = data.dropna(subset=['Vict Age'])
    data['Vict Age'] = data['Vict Age'].astype(int)
    return data

data = load_data()

# Sidebar filters
st.sidebar.header("Filters")

start_date = st.sidebar.date_input("Start Date", dt.date(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", dt.date.today())

area = st.sidebar.selectbox("Area", ["All"] + sorted(data['AREA NAME'].dropna().unique().tolist()))
crime_type = st.sidebar.selectbox("Crime Type", ["All"] + sorted(data['Crm Cd Desc'].dropna().unique().tolist()))
outcome = st.sidebar.selectbox("Outcome", ["All"] + sorted(data['Status Desc'].dropna().unique().tolist()))

min_age, max_age = st.sidebar.slider("Victim Age Range", 0, 100, (0, 100))

# Filter data function
def filter_data():
    filtered = data.copy()
    filtered = filtered[(filtered['DATE OCC'] >= pd.to_datetime(start_date)) & 
                        (filtered['DATE OCC'] <= pd.to_datetime(end_date))]

    if area != "All":
        filtered = filtered[filtered['AREA NAME'] == area]
    if crime_type != "All":
        filtered = filtered[filtered['Crm Cd Desc'] == crime_type]
    if outcome != "All":
        filtered = filtered[filtered['Status Desc'] == outcome]

    filtered = filtered[(filtered['Vict Age'] >= min_age) & (filtered['Vict Age'] <= max_age)]
    return filtered

filtered = filter_data()

st.title("📊 L.A. Crime Data Dashboard")

# Crime Trend
st.subheader("📈 Crime Trends Over Time")
df = filtered.groupby(filtered['DATE OCC'].dt.to_period('M')).size().reset_index(name='Crimes')
df['DATE OCC'] = df['DATE OCC'].dt.to_timestamp()
fig, ax = plt.subplots(figsize=(8, 5))
sns.lineplot(data=df, x='DATE OCC', y='Crimes', ax=ax)
ax.set_xlabel("Date")
ax.set_ylabel("Number of Crimes")
st.pyplot(fig)

# 🔮 Crime Forecast Section
st.subheader("🔮 Crime Forecast (Next 6 Months)")
forecast_df = filtered.groupby(filtered['DATE OCC'].dt.to_period('M')).size().reset_index(name='Crimes')
forecast_df['DATE OCC'] = forecast_df['DATE OCC'].dt.to_timestamp()
forecast_df.columns = ['ds', 'y']

if len(forecast_df) > 3:
    model = Prophet()
    model.fit(forecast_df)
    future = model.make_future_dataframe(periods=6, freq='M')
    forecast = model.predict(future)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(forecast_df['ds'], forecast_df['y'], label='Actual Crimes')
    ax.plot(forecast['ds'], forecast['yhat'], label='Predicted Crimes', linestyle='--')
    ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.2)
    ax.legend()
    ax.set_title("Crime Forecast for Next 6 Months")
    st.pyplot(fig)
else:
    st.info("Not enough data for forecasting. Try selecting a wider date range.")

# Top Crimes
st.subheader("🔝 Top 10 Crime Types")
df = filtered['Crm Cd Desc'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=df.values, y=df.index, ax=ax, palette='magma')
ax.set_xlabel("Number of Crimes")
ax.set_ylabel("Crime Type")
st.pyplot(fig)

# Crimes by Area
st.subheader("📍 Crime Count by Area")
df = filtered['AREA NAME'].value_counts().reset_index()
df.columns = ['Area', 'Count']
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=df, y='Area', x='Count', palette='coolwarm', ax=ax)
st.pyplot(fig)

# Time Heatmap
st.subheader("⏰ Crimes by Hour and Weekday")
filtered['Hour'] = filtered['TIME OCC'] // 100
filtered['Weekday'] = filtered['DATE OCC'].dt.day_name()
heatmap_data = pd.crosstab(filtered['Hour'], filtered['Weekday'])
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(heatmap_data, cmap="YlGnBu", ax=ax)
st.pyplot(fig)

# Outcomes
st.subheader("⚖️ Crime Outcomes")
df = filtered['Status Desc'].value_counts()
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x=df.values, y=df.index, ax=ax)
st.pyplot(fig)

# Victim Demographics
st.subheader("👥 Victim Demographics")
fig, axs = plt.subplots(1, 3, figsize=(18, 5))

# Sex
sex_counts = filtered['Vict Sex'].value_counts()
sns.barplot(x=sex_counts.index, y=sex_counts.values, ax=axs[0])
axs[0].set_title("Victim Sex Distribution")

# Age
age_bins = pd.cut(filtered['Vict Age'], bins=[0, 18, 30, 45, 60, 100])
age_counts = age_bins.value_counts().sort_index()
axs[1].plot(age_counts.index.astype(str), age_counts.values, marker='o')
axs[1].set_title("Victim Age Ranges")
axs[1].tick_params(axis='x', rotation=45)

# Descent
descent_counts = filtered['Vict Descent'].value_counts().head(10)
sns.barplot(x=descent_counts.index, y=descent_counts.values, ax=axs[2])
axs[2].set_title("Top 10 Victim Descent Groups")
axs[2].tick_params(axis='x', rotation=45)

st.pyplot(fig)

# Weapon Types
st.subheader("🔫 Top Weapon Types")
df = filtered['Weapon Desc'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=df.values, y=df.index, ax=ax, palette='viridis')
ax.set_xlabel("Occurrences")
ax.set_ylabel("Weapon")
st.pyplot(fig)

# --------------------------------------------------------
# 🧩 Predictive Model: Crime Type Prediction
# --------------------------------------------------------
@st.cache_resource
def train_crime_type_model(data):
    df = data[['Vict Age', 'Vict Sex', 'AREA NAME', 'Weapon Desc', 'Crm Cd Desc']].dropna()
    label_encoders = {}
    for col in ['Vict Sex', 'AREA NAME', 'Weapon Desc', 'Crm Cd Desc']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    X = df[['Vict Age', 'Vict Sex', 'AREA NAME', 'Weapon Desc']]
    y = df['Crm Cd Desc']

    model = RandomForestClassifier(n_estimators=120, random_state=42)
    model.fit(X, y)
    return model, label_encoders

st.subheader("🔎 Predict Crime Type")

# Prediction form
age = st.number_input("Victim Age", min_value=0, max_value=100, value=25)
sex = st.selectbox("Victim Sex", sorted(data['Vict Sex'].dropna().unique().tolist()))
area_name = st.selectbox("Area", sorted(data['AREA NAME'].dropna().unique().tolist()))
weapon = st.selectbox("Weapon Type", sorted(data['Weapon Desc'].dropna().unique().tolist()))

if st.button("Predict Crime Type"):
    model, label_encoders = train_crime_type_model(data)
    try:
        sex_enc = label_encoders['Vict Sex'].transform([sex])[0]
        area_enc = label_encoders['AREA NAME'].transform([area_name])[0]
        weapon_enc = label_encoders['Weapon Desc'].transform([weapon])[0]
    except ValueError:
        st.error("One of the selected values was not in training data.")
    else:
        X_new = np.array([[age, sex_enc, area_enc, weapon_enc]])
        pred_encoded = model.predict(X_new)[0]
        crime_pred = label_encoders['Crm Cd Desc'].inverse_transform([pred_encoded])[0]
        st.success(f"🧩 Predicted Crime Type: **{crime_pred}**")

# --------------------------------------------------------
# Footer Note
st.markdown("---")
st.caption("Developed by Kartik_Goyal for analytical and predictive exploration of Los Angeles crime data.")
