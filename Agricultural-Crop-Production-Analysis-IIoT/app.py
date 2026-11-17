import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Crop Production Analysis", page_icon="🌾", layout="wide")
st.title("🌾 Agricultural Crop Production Analysis using IIoT")
st.caption("Python data analytics dashboard | CSV-based demonstration")

DATA_FILE = Path(__file__).parent / "data" / "crop_production.csv"
REQUIRED = ["Date","Crop","Area_Hectares","Production_Tonnes","Rainfall_mm","Temperature_C","Humidity_Percent","Soil_Moisture_Percent"]

with st.sidebar:
    st.header("Data")
    upload = st.file_uploader("Upload agricultural CSV", type=["csv"])
    st.info("Included data is synthetic sample data, not live sensor readings.")

try:
    df = pd.read_csv(upload) if upload else pd.read_csv(DATA_FILE)
except Exception as e:
    st.error(f"Could not read CSV: {e}")
    st.stop()

missing = [c for c in REQUIRED if c not in df.columns]
if missing:
    st.error("Missing required columns: " + ", ".join(missing))
    st.stop()

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
for c in REQUIRED:
    if c not in ["Date","Crop"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
df = df.dropna(subset=["Date","Crop","Production_Tonnes"])
if df.empty:
    st.error("No valid data rows found.")
    st.stop()

with st.sidebar:
    crop_options = sorted(df["Crop"].astype(str).unique())
    chosen = st.multiselect("Choose crops", crop_options, default=crop_options)
    filtered = df[df["Crop"].isin(chosen)]
    date_range = st.date_input("Date range", value=(df.Date.min().date(), df.Date.max().date()))

# Apply the selected date range when two dates are selected.
if isinstance(date_range, tuple) and len(date_range) == 2:
    filtered = filtered[(filtered.Date.dt.date >= date_range[0]) & (filtered.Date.dt.date <= date_range[1])]
elif date_range:
    filtered = filtered[filtered.Date.dt.date == date_range]

if filtered.empty:
    st.warning("No records match the filters.")
    st.stop()

tot = filtered.Production_Tonnes.sum()
avg = filtered.Production_Tonnes.mean()
top = filtered.groupby("Crop").Production_Tonnes.sum().idxmax()
k1,k2,k3,k4 = st.columns(4)
k1.metric("Total production", f"{tot:,.1f} tonnes")
k2.metric("Average production", f"{avg:,.1f} tonnes")
k3.metric("Average rainfall", f"{filtered.Rainfall_mm.mean():.1f} mm")
k4.metric("Highest production crop", top)

st.subheader("Dataset preview")
st.dataframe(filtered, use_container_width=True, hide_index=True)

left,right = st.columns(2)
with left:
    st.subheader("Crop-wise production")
    totals=filtered.groupby("Crop").Production_Tonnes.sum().sort_values(ascending=False)
    fig,ax=plt.subplots()
    totals.plot(kind="bar",ax=ax)
    ax.set_xlabel("Crop"); ax.set_ylabel("Production (tonnes)")
    ax.set_title("Total production by crop")
    plt.xticks(rotation=30); fig.tight_layout()
    st.pyplot(fig); plt.close(fig)
with right:
    st.subheader("Rainfall vs production")
    fig,ax=plt.subplots()
    ax.scatter(filtered.Rainfall_mm,filtered.Production_Tonnes)
    ax.set_xlabel("Rainfall (mm)"); ax.set_ylabel("Production (tonnes)")
    ax.set_title("Rainfall and production")
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)

st.subheader("Environmental readings")
measure=st.selectbox("Select measurement",["Temperature_C","Humidity_Percent","Soil_Moisture_Percent","Rainfall_mm"])
fig,ax=plt.subplots()
ax.plot(filtered.Date,filtered[measure],marker="o")
ax.set_xlabel("Date"); ax.set_ylabel(measure); ax.set_title(measure+" over time")
fig.autofmt_xdate(); fig.tight_layout()
st.pyplot(fig); plt.close(fig)

st.subheader("Crop summary")
summary=filtered.groupby("Crop").agg(
    Total_Production=("Production_Tonnes","sum"),
    Average_Production=("Production_Tonnes","mean"),
    Average_Rainfall=("Rainfall_mm","mean"),
    Average_Temperature=("Temperature_C","mean")
).round(2).sort_values("Total_Production",ascending=False)
st.dataframe(summary,use_container_width=True)

st.subheader("Analysis")
st.write(f"Highest total production in the selected data: **{top}**.")
st.write(f"Average soil moisture: **{filtered.Soil_Moisture_Percent.mean():.1f}%**.")
st.write("Compare environmental readings with production to explore patterns.")
st.warning("Patterns do not prove cause and effect. Use verified local data for real farming decisions.")

st.download_button("Download filtered CSV",filtered.to_csv(index=False).encode("utf-8"),"filtered_crop_data.csv","text/csv")
st.subheader("How IIoT fits")
st.write("In a real deployment, sensors can measure soil moisture, temperature and humidity and send readings to a database/cloud. This version analyzes a CSV sample; it does not connect to physical sensors or control irrigation.")
