# Market Lens — Automated Stock Analysis Pipeline

An end-to-end automated stock analysis pipeline that reads tickers from Google Sheets, fetches market data, performs advanced technical analysis, and writes predictions back to the sheet.

Built for traders, analysts, and automation workflows who want fast, repeatable insights without manual charting.

Helps identify key price levels and potential breakout zones without manual chart analysis.

---
## Features
### Google Sheets Integration
- Import stock tickers automatically
- Export results directly back to your sheet
- Enables fully automated workflows

### Market Data Collection
- Fetches historical OHLC data
- Configurable timeframes and intervals
- Reliable data retrieval with retry logic

### Support & Resistance Detection
- Uses Kernel Density Estimation (KDE)
- Identifies high-probability price zones
- Filters noise to produce clean levels

### Trend Line Forecasting
- Detects trend channels (uptrend/downtrend)
- Applies regression on price structure
- Projects future price ranges and breakout zones

---
## Visualization
The pipeline automatically generates:

- Candlestick charts
- Trend lines & projections
- Turning points (peaks & troughs)
- Support/resistance zones

Charts are saved locally for further analysis or reporting.

---
## Screenshots
![Chart Example](Line_chart.jpg)
![screenshot_2](Candle_chart.jpg)
![screenshot_3](Support_resistance.jpg)

---
## How It Works
```
Google Sheets → Fetch Tickers
        ↓
Yahoo Finance → Download OHLC Data
        ↓
Data Processing → Clean & Prepare
        ↓
Analysis:
   • KDE (Support/Resistance)
   • Trend Detection
   • Regression Forecast
        ↓
Visualization → Charts
        ↓
Write Results → Google Sheets
```

---
## Installation
### Clone the repository:
```bash
git clone https://github.com/alexkanav/Market-Lens-python
cd Market-Lens-python
```
### Create and activate a virtual environment
```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Install Python dependencies
```bash
pip install -r requirements.txt
```

---
### Google Sheets Setup
- Enable Google Sheets API
- Create a service account
- Download credentials JSON
- Place it in the project root

---
## Run the script:
```bash
python main.py
```

---
## License
This project is licensed under the MIT License.