# Crime Dashboard in Streamlit using Plotly and Pandas

import streamlit as st
import pandas as pd
import plotly.express as px
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
fig = px.line(df, x='DATE OCC', y='Crimes', title='Crime Trends Over Time', markers=True)
st.plotly_chart(fig, use_container_width=True)

# Top Crimes
st.subheader("🔝 Top 10 Crime Types")
df = filtered['Crm Cd Desc'].value_counts().head(10).reset_index()
df.columns = ['Crime Type', 'Count']
fig = px.bar(df, x='Count', y='Crime Type', orientation='h', color='Count', title='Top 10 Crime Types', text='Count')
st.plotly_chart(fig, use_container_width=True)

# Crimes by Area
st.subheader("📍 Crime Count by Area")
df = filtered['AREA NAME'].value_counts().reset_index()
df.columns = ['Area', 'Count']
fig = px.bar(df, x='Count', y='Area', orientation='h', color='Count', title='Crime Count by Area', text='Count')
st.plotly_chart(fig, use_container_width=True)

# Time Heatmap
st.subheader("⏰ Crimes by Hour and Weekday")
filtered['Hour'] = filtered['TIME OCC'] // 100
filtered['Weekday'] = filtered['DATE OCC'].dt.day_name()
heatmap_data = pd.crosstab(filtered['Hour'], filtered['Weekday'])
fig = px.imshow(heatmap_data, text_auto=True, aspect="auto", title="Crimes by Hour and Weekday")
st.plotly_chart(fig, use_container_width=True)

# Outcomes
st.subheader("⚖️ Crime Outcomes")
df = filtered['Status Desc'].value_counts().reset_index()
df.columns = ['Outcome', 'Count']
fig = px.bar(df, x='Count', y='Outcome', orientation='h', color='Count', title='Crime Outcomes', text='Count')
st.plotly_chart(fig, use_container_width=True)

# Victim Demographics
st.subheader("👥 Victim Demographics")

# Victim Sex
sex_counts = filtered['Vict Sex'].value_counts().reset_index()
sex_counts.columns = ['Sex', 'Count']
fig_sex = px.bar(sex_counts, x='Sex', y='Count', color='Count', title='Victim Sex Distribution', text='Count')
st.plotly_chart(fig_sex, use_container_width=True)

# Victim Age Ranges
age_bins = pd.cut(filtered['Vict Age'], bins=[0, 18, 30, 45, 60, 100])
age_counts = age_bins.value_counts().sort_index().reset_index()
age_counts.columns = ['Age Range', 'Count']
fig_age = px.line(age_counts, x='Age Range', y='Count', markers=True, title='Victim Age Ranges')
st.plotly_chart(fig_age, use_container_width=True)

# Victim Descent
descent_counts = filtered['Vict Descent'].value_counts().head(10).reset_index()
descent_counts.columns = ['Descent', 'Count']
fig_descent = px.bar(descent_counts, x='Count', y='Descent', orientation='h', color='Count', title='Top 10 Victim Descent Groups', text='Count')
st.plotly_chart(fig_descent, use_container_width=True)

# Weapon Types
st.subheader("🔫 Top Weapon Types")
weapon_counts = filtered['Weapon Desc'].value_counts().head(10).reset_index()
weapon_counts.columns = ['Weapon', 'Count']
fig_weapon = px.bar(weapon_counts, x='Count', y='Weapon', orientation='h', color='Count', title='Top Weapon Types', text='Count')
st.plotly_chart(fig_weapon, use_container_width=True)
