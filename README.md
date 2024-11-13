# Weather Application

A Python application for displaying weather information from the Netherlands using the Buienradar API and KNMI data.

## Features

- Current weather display for Dutch weather stations
- Weather forecast
- Historical weather statistics calculation from KNMI data files

## Requirements

- Python 3.x
- Required packages:
  - requests
  - pandas
  - tkinter (usually comes with Python)

## Installation

1. Clone the repository: 
```

## Usage

Run the application:
```

### Current Weather
- Select a weather station from the dropdown
- Click "Refresh Data" to see current weather information

### Forecast
- Click "Get Forecast" to see the latest weather forecast

### Statistics
- Select a KNMI data file (.csv format)
- Enter date range
- Click "Calculate Statistics" to see weather statistics for the selected period

## Data Format

For statistics calculation, the KNMI data file should be in CSV format with the following columns:
- DATE: Date in YYYY-MM-DD format
- TEMP: Temperature in Celsius
- PRECIPITATION: Precipitation in mm
- AIRPRESSURE: Air pressure in hPa

## License

This project is licensed under the MIT License - see the LICENSE file for details.