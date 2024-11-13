from utils.api_handler import BuienradarAPI
from datetime import datetime
import logging

class CurrentWeather:
    @staticmethod
    def format_station_data(station_data: dict) -> str:
        """Formats weather station data into readable text"""
        if not station_data:
            return "No data available"
        
        try:
            # Check if all required fields exist and handle potential None values
            template = """
Station: {stationname}
Region: {regio}
Temperature: {temperature:.1f}°C
Ground Temperature: {groundtemperature:.1f}°C
Wind Speed: {windspeed:.1f} Bft
Wind Direction: {winddirection}
Air Pressure: {airpressure}
Precipitation: {precipitation:.1f} mm
Weather Description: {weatherdescription}
Measured at: {timestamp}
"""
            # Handle potential None or missing values
            safe_data = {
                'stationname': station_data.get('stationname', 'N/A'),
                'regio': station_data.get('regio', 'N/A'),
                'temperature': station_data.get('temperature', 0.0) or 0.0,
                'groundtemperature': station_data.get('groundtemperature', 0.0) or 0.0,
                'windspeed': station_data.get('windspeed', 0.0) or 0.0,
                'winddirection': station_data.get('winddirection', 'N/A'),
                'airpressure': station_data.get('airpressure', 'N/A'),  # Remove formatting for airpressure
                'precipitation': station_data.get('precipitation', 0.0) or 0.0,
                'weatherdescription': station_data.get('weatherdescription', 'N/A'),
                'timestamp': station_data.get('timestamp', 'N/A')
            }

            # Format timestamp if it exists
            if safe_data['timestamp'] != 'N/A':
                try:
                    timestamp = datetime.fromisoformat(safe_data['timestamp'].replace('Z', '+00:00'))
                    safe_data['timestamp'] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                except (ValueError, AttributeError):
                    safe_data['timestamp'] = 'N/A'

            return template.format(**safe_data)
            
        except Exception as e:
            logging.error(f"Error formatting station data: {e}")
            return f"Data formatting error: {str(e)}"
