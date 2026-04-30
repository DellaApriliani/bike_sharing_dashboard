import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#menyiapkan halaman
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

st.title("Bike Sharing Dashboard 🚲")
st.markdown("Analisis Pola Peminjaman Sepeda Tahun 2011-2012")

#load data
def load_data():
    day_df = pd.read_csv("day_clear.csv")
    hour_df = pd.read_csv("hour_clear.csv")
    return day_df, hour_df

day_df, hour_df = load_data()
day_df["season"] = day_df["season"].str.lower()

season_map = {
    1: "spring",
    2: "summer",
    3: "fall",
    4: "winter"
}

hour_df["season"] = hour_df["season"].map(season_map)

#membuat sidebar filter
st.sidebar.header("Filter Dashboard")

selected_year = st.sidebar.selectbox(
    "Pilih Tahun",
    ["All", 2011, 2012]
)

selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    options=day_df["season"].unique(),
    default=day_df["season"].unique()
)

#membuat salinan day_df
filtered_day_df = day_df.copy()

#filter day_df berdasarkan tahun
if selected_year != "All":
    filtered_day_df = filtered_day_df[
        filtered_day_df["year"] == selected_year
    ]

#filter day_df berdasarkan musim
filtered_day_df = filtered_day_df[
    filtered_day_df["season"].isin(selected_season)
]

#filter hour_df berdasarkan jam
filtered_hour_df = hour_df.copy()

#filter hour_df berdasarkan tahun
if selected_year != "All":
    filtered_hour_df = filtered_hour_df[
        filtered_hour_df["year"] == selected_year
    ]

#filter hour_df berdasarkan musim
filtered_hour_df = filtered_hour_df[
    filtered_hour_df["season"].isin(selected_season)
]

#ubah nama weather
weather_map = {
    1: "Clear",
    2: "Mist",
    3: "Light Snow/Rain",
    4: "Heavy Rain/Snow"
}
filtered_day_df["weathersit"] = filtered_day_df["weathersit"].map(weather_map)

#membuat key indicator
st.subheader("Key Performance Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Rentals", value=filtered_day_df["total_rentals"].sum())

with col2:
    st.metric("Average Daily Rentals", value=round(filtered_day_df["total_rentals"].mean(), 2))

with col3:
    peak_hour = filtered_hour_df.groupby("hour")["total_rentals"].sum().idxmax()
    st.metric("Peak Hour", value=f"{peak_hour}:00")

#analisis season
st.subheader("Rentals by Season 🖼️")

season_rentals = filtered_day_df.groupby("season")["total_rentals"].mean().reset_index()

fig, ax = plt.subplots(figsize=(5,3))
sns.barplot(data=season_rentals, x="season", y="total_rentals", ax=ax)

ax.set_title("Average Rentals by Season")
ax.set_xlabel("Season")
ax.set_ylabel("Average Rentals")

st.pyplot(fig, use_container_width=False)

#analisis weather
st.subheader("Rentals by Weather Condition 🚲")

weather_rentals = filtered_day_df.groupby("weathersit")["total_rentals"].mean().reset_index()

fig, ax = plt.subplots(figsize=(5, 3))
sns.barplot(
    data=weather_rentals,
    x="weathersit",
    y="total_rentals",
    ax=ax
)

ax.set_title("Average Bike Rentals by Weather")
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Average Rentals")
plt.xticks(rotation=15)

st.pyplot(fig, use_container_width=False)

#tren bulanan
st.subheader("Monthly Rental Trend 📅")

monthly_rentals = filtered_day_df.groupby("month")["total_rentals"].mean().reset_index()

fig, ax = plt.subplots(figsize=(5, 3))
sns.lineplot(
    data=monthly_rentals,
    x="month",
    y="total_rentals",
    marker="o",
    ax=ax
)

ax.set_title("Average Rentals by Month")
ax.set_xlabel("Month")
ax.set_ylabel("Average Rentals")

st.pyplot(fig, use_container_width=False)

#tren per jam
st.subheader("Hourly Rental Trend ⏰")

hourly_rentals = filtered_hour_df.groupby("hour")["total_rentals"].mean().reset_index()

fig, ax = plt.subplots(figsize=(8,5))

sns.lineplot(
    data=hourly_rentals,
    x="hour",
    y="total_rentals",
    marker="o",
    ax=ax
)

ax.set_title("Average Rentals by Hour")
ax.set_xlabel("Hour")
ax.set_ylabel("Average Rentals")

st.pyplot(fig)

#footer
st.markdown("---")
st.caption("Dashboard by Della Apriliani | Dicoding Projek Analisis Data")