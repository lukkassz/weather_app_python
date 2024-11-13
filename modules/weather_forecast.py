from datetime import datetime
import logging

class WeatherForecast:
    @staticmethod
    def format_forecast_data(forecast_data: dict) -> str:
        """Formats forecast data into readable text"""
        if not forecast_data:
            return "No forecast data available"
        
        try:
            template = """
Forecast Title: {title}
Published: {published}

Weather Report:
{text}

Author: {author}
"""
            # Format the published date if possible
            if 'published' in forecast_data:
                try:
                    timestamp = datetime.fromisoformat(forecast_data['published'].replace('Z', '+00:00'))
                    forecast_data['published'] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                except (ValueError, AttributeError):
                    pass  # Keep original format if parsing fails
                    
            return template.format(**forecast_data)
            
        except Exception as e:
            logging.error(f"Error formatting forecast data: {e}")
            return f"Forecast formatting error: {str(e)}"
