# Crime Analysis Dashboards

This repository contains a comprehensive set of crime analysis dashboards developed in Python to analyze and visualize large-scale crime data. The dashboards are designed to uncover meaningful patterns in crime occurrence, geographic distribution, victim demographics, crime outcomes, and time-based trends through interactive and filter-driven visualizations.

The project demonstrates end-to-end data analytics capabilities, including data ingestion and preprocessing, exploratory data analysis (EDA), feature filtering, and the development of interactive dashboards for analytical reporting. Multiple visualization libraries and frameworks are used to present insights in both static and highly interactive formats.

In addition to descriptive analytics, the project incorporates predictive components such as time-series crime forecasting and supervised machine learning–based crime type prediction. These extensions illustrate how traditional dashboards can be enhanced with predictive intelligence to support forward-looking analysis and decision-making.

Multiple dashboard implementations are included to showcase different approaches to user interaction, visualization design, and analytical presentation across desktop-based and web-based environments.

## 📊 Dashboards Included

### 1️⃣ Crime_Analysis.py (Tkinter Desktop Dashboard)
A desktop-based interactive dashboard built using **Tkinter**, **Matplotlib**, and **Seaborn**.

**Key Features:**
- Date range filtering
- Area, crime type, and outcome filtering
- Victim age range selection
- Visualizations:
  - Crime trends over time
  - Top crime types
  - Crimes by area
  - Time-based heatmap (hour vs weekday)
  - Crime outcomes
  - Victim demographics
  - Weapon usage analysis

**Use Case:**  
Demonstrates traditional desktop-based data visualization and UI controls.

### 2️⃣ crime_dashboard.py (Streamlit – Static Visual Analytics)
A web-based dashboard built using **Streamlit**, **Matplotlib**, and **Seaborn**.

**Key Features:**
- Sidebar filters for date, area, crime type, outcome, and age
- Clean layout with multiple analytical sections
- Focused on exploratory visual analysis

**Use Case:**  
Shows migration from desktop UI to web-based analytics using Streamlit.

### 3️⃣ Crime_Dashboard_2.py (Streamlit + Plotly)
An enhanced Streamlit dashboard using **Plotly** for interactive visualizations.

**Key Features:**
- Interactive charts with hover and zoom
- Plotly-based line charts, bar charts, and heatmaps
- Improved user experience compared to static charts

**Use Case:**  
Demonstrates improved interactivity and modern visualization techniques.

### 4️⃣ Crime_Dashboard_With_ML.py (Analytics + ML Extension)
An advanced version of the dashboard integrating **forecasting and prediction**.

**Additional Features:**
- Time-series crime forecasting using **Facebook Prophet**
- Crime type prediction using **Random Forest Classifier**
- User input–based crime prediction
- Combines EDA, forecasting, and supervised ML

**Use Case:**  
Explores how analytics dashboards can be extended with predictive capabilities.

## 🗂 Dataset
- Public crime dataset sourced from **Kaggle**
- Large CSV file (~243 MB)
- Dataset is **not included** in the repository due to size constraints
- The dataset is available on request—please contact me if you need access to it for development or testing purposes.

**Dataset Name**
Crime_Data_from_2020_to_Present.csv
