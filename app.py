import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")

st.title("COVID-19 Global Impact Dashboard")
st.write("Interactive analysis of demonstration COVID-19 data.")
st.warning("This project uses synthetic demonstration data, not official statistics.")

file = Path(__file__).resolve().parents[1] / "data" / "covid_demo_data.csv"
df = pd.read_csv(file)

countries = st.sidebar.multiselect(
    "Select countries",
    sorted(df["location"].unique()),
    default=sorted(df["location"].unique())
)

data = df[df["location"].isin(countries)].copy()

if data.empty:
    st.info("Select at least one country.")
    st.stop()

latest = data.sort_values("date").groupby("location").tail(1)

a, b, c = st.columns(3)
a.metric("Countries selected", len(countries))
b.metric("Reported cumulative cases", f'{latest["total_cases"].sum():,}')
c.metric("Reported cumulative deaths", f'{latest["total_deaths"].sum():,}')

st.subheader("Daily New Cases")
fig = px.line(data, x="date", y="new_cases", color="location",
              markers=True, title="Daily reported cases")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Cumulative Cases")
fig = px.line(data, x="date", y="total_cases", color="location",
              markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Daily Deaths")
fig = px.bar(data, x="date", y="new_deaths", color="location",
             barmode="group")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Vaccination Progress")
fig = px.line(data, x="date", y="people_vaccinated",
              color="location", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Data Table")
st.dataframe(data, use_container_width=True)

st.download_button(
    "Download Dataset",
    data=data.to_csv(index=False),
    file_name="covid_filtered_data.csv",
    mime="text/csv"
)
