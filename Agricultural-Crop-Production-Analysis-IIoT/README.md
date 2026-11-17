# Agricultural Crop Production Analysis using IIoT

Python + Streamlit data analytics dashboard.

## Features
- Load included CSV or upload another agricultural CSV.
- Filter by crop and date.
- Calculate production and environmental summaries.
- Show crop-wise bar chart, rainfall scatter plot and environmental trends.
- Download filtered data.

## Important data note
The included CSV is **synthetic sample data** for practice. It is not real farm data and is not collected from live IIoT sensors. This version does not connect to physical sensors, a cloud service, or an irrigation controller.

In a real IIoT deployment, sensors could send soil moisture, temperature and humidity readings to a database/cloud. This dashboard could analyze that verified data after export.

## Run in VS Code (Windows)
1. Extract this ZIP and open the project folder in VS Code.
2. Open Terminal > New Terminal.
3. Create a virtual environment:
   `python -m venv .venv`
4. Activate in PowerShell:
   `.venv\\Scripts\\Activate.ps1`
   If blocked, use Command Prompt and run:
   `.venv\\Scripts\\activate.bat`
5. Install dependencies:
   `python -m pip install -r requirements.txt`
6. Run:
   `python -m streamlit run app.py`
7. Open the local URL shown in the terminal, usually `http://localhost:8501`.

## CSV columns required
`Date, Crop, Area_Hectares, Production_Tonnes, Rainfall_mm, Temperature_C, Humidity_Percent, Soil_Moisture_Percent`

## Project structure
- `app.py` - dashboard and analysis code
- `data/crop_production.csv` - synthetic practice dataset
- `requirements.txt` - Python libraries

## Viva explanation
"My project is a software-based agricultural data analytics dashboard. It reads crop and field-condition data from a CSV using Pandas, calculates production summaries, and displays charts using Matplotlib and Streamlit. The environmental columns represent readings that could be collected by IIoT sensors. The current version uses sample data, not live sensor readings."

## Limitations
- Synthetic sample dataset.
- No trained machine-learning yield prediction.
- No live sensor connection or automatic irrigation.
