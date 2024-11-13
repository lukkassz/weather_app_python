import requests
from typing import Dict, Optional
import logging

class BuienradarAPI:
    BASE_URL = "https://data.buienradar.nl/2.0/feed/json"
    
    @staticmethod
    def get_weather_data() -> Optional[Dict]:
        """Fetches weather data from Buienradar API"""
        try:
            response = requests.get(BuienradarAPI.BASE_URL)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Error fetching weather data: {e}")
            return None
    
    @staticmethod
    def get_stations() -> list:
        """Retrieves list of available weather stations"""
        data = BuienradarAPI.get_weather_data()
        if not data:
            return []
        
        try:
            stations = data['actual']['stationmeasurements']
            return [(station['stationname'], station['regio']) 
                   for station in stations]
        except KeyError as e:
            logging.error(f"Error parsing stations data: {e}")
            return []
    
    @staticmethod
    def get_station_data(station_name: str) -> Optional[Dict]:
        """Retrieves data for a specific station"""
        data = BuienradarAPI.get_weather_data()
        if not data:
            return None
        
        try:
            stations = data['actual']['stationmeasurements']
            for station in stations:
                if station['stationname'].lower() == station_name.lower():
                    return station
            logging.warning(f"Station {station_name} not found")
            return None
        except KeyError as e:
            logging.error(f"Error parsing station data: {e}")
            return None
    
    @staticmethod
    def get_forecast() -> Optional[Dict]:
        """Retrieves weather forecast from Buienradar API"""
        try:
            data = BuienradarAPI.get_weather_data()
            if not data:
                return None
            
            forecast = data.get('forecast', {}).get('weatherreport', {})
            if not forecast:
                return None
            
            return {
                'title': forecast.get('title', 'No title available'),
                'published': forecast.get('published', 'No date available'),
                'text': forecast.get('text', 'No forecast available'),
                'author': forecast.get('author', 'Unknown')
            }
        except Exception as e:
            logging.error(f"Error fetching forecast: {e}")
            return None
