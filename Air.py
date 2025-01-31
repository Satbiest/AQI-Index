import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import numpy as np

# Membaca dataset
try:
    df = pd.read_csv("C:/Users/resia/Downloads/airrdataa.csv", encoding="utf-8")
except Exception as e:
    st.error(f"Error reading CSV file: {e}")
    st.stop()

# Menghapus spasi dari nama kolom (jika ada)
df.columns = df.columns.str.strip()

# Menampilkan judul dashboard
st.title('Air Quality Data Dashboard')

# Membuat filter untuk memilih 'station' dan 'year'
stations = df['station'].unique()
years = df['year'].unique()

selected_station = st.selectbox('Select Station', stations)
selected_year = st.selectbox('Select Year', years)

# Filter data berdasarkan inputan user
filtered_df = df[(df['station'] == selected_station) & (df['year'] == selected_year)].dropna()

# Jika tidak ada data setelah filter, tampilkan pesan
if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# Menampilkan statistik dasar untuk data yang difilter
st.subheader('Basic Statistics of Selected Data')
st.write(filtered_df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN']].describe())

# Bar chart untuk membandingkan polutan utama
st.subheader('Comparison of Pollutants')
fig, ax = plt.subplots()
filtered_df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean().plot(kind='bar', ax=ax, color=['red', 'orange', 'yellow', 'green', 'blue', 'purple'])
ax.set_ylabel('Average Concentration')
ax.set_title('Comparison of Pollutants')
st.pyplot(fig)

# Perhitungan AQI sederhana
st.subheader("Air Quality Index (AQI)")
AQI = filtered_df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean().max()
st.metric(label="Estimated AQI Index", value=round(AQI, 2))

# Gauge Chart untuk AQI
st.subheader("Air Quality Gauge Indicator")
gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=AQI,
    title={'text': "AQI Level"},
    gauge={'axis': {'range': [None, 500]}, 'bar': {'color': "purple"}}
))
st.plotly_chart(gauge)

# Menambahkan kolom bulan jika tidak ada kolom 'date'
if 'month' not in filtered_df.columns:
    filtered_df['month'] = pd.to_datetime(filtered_df[['year', 'month', 'day']]).dt.month

# Time series AQI per bulan
st.subheader("AQI Trend per Month")
monthly_aqi = filtered_df.groupby('month')[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean().max(axis=1)
fig, ax = plt.subplots()
ax.plot(monthly_aqi.index, monthly_aqi.values, marker='o', linestyle='-', color='purple', label='AQI')
ax.set_xlabel('Month')
ax.set_ylabel('AQI Level')
ax.set_title(f'AQI Trend for {selected_station} in {selected_year}')
ax.legend()
st.pyplot(fig)

# Wind Rose Chart
st.subheader("Wind Rose Chart")
wind_data = filtered_df.groupby('wd')['WSPM'].mean()
fig, ax = plt.subplots()
wind_data.plot(kind='bar', ax=ax, color='skyblue')
ax.set_ylabel('Average Wind Speed')
ax.set_title('Wind Speed Distribution by Wind Direction')
st.pyplot(fig)

# Heatmap Korelasi Polutan
st.subheader("Heatmap: Correlation Between Pollutants")
corr = filtered_df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Scatter Plot 2 Variabel (TEMP vs PM2.5)
st.subheader("Scatter Plot: Temperature vs PM2.5")
fig, ax = plt.subplots()
ax.scatter(filtered_df['TEMP'], filtered_df['PM2.5'], alpha=0.5, color='red')
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('PM2.5 Level')
ax.set_title('Temperature vs PM2.5')
st.pyplot(fig)

# Scatter Plot Hubungan Suhu, Tekanan, Kelembapan, dan Polusi
st.subheader("Scatter Plot: Temperature, Pressure, and PM2.5")
fig, ax = plt.subplots()
sc = ax.scatter(filtered_df['TEMP'], filtered_df['PRES'], c=filtered_df['PM2.5'], cmap='coolwarm', alpha=0.7)
plt.colorbar(sc, label='PM2.5 Level')
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Pressure (hPa)')
ax.set_title('Relationship Between Temperature, Pressure, and PM2.5')
st.pyplot(fig)
