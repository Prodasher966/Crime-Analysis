# Crime Dashboard in Streamlit using Plotly, Matplotlib, Seaborn, and Pandas

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt

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

#To Run this Code: Run this in terminal
#streamlit run crime_dashboard.py
