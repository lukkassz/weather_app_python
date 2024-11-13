import pandas as pd
import os
from datetime import datetime
import logging

class WeatherStatistics:
    def __init__(self):
        self.output_dir = "data/output"
        os.makedirs(self.output_dir, exist_ok=True)

    def process_period(self, file_path: str, start_date: str, end_date: str) -> tuple:
        """Process weather data for the given period"""
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            
            # Convert dates to datetime for comparison
            df['DATE'] = pd.to_datetime(df['DATE'])
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            
            # Filter data for the specified period
            mask = (df['DATE'] >= start) & (df['DATE'] <= end)
            period_data = df.loc[mask]
            
            if period_data.empty:
                return None, "No data found for the specified period"
            
            # Calculate statistics
            stats = {
                'max_temp': float(period_data['TEMP'].max()),
                'min_temp': float(period_data['TEMP'].min()),
                'avg_temp': float(period_data['TEMP'].mean()),
                'total_precipitation': float(period_data['PRECIPITATION'].sum())
            }
            
            # Create output filename
            filename = f"weerstatistieken-{start_date}-{end_date}.txt"
            output_path = os.path.join(self.output_dir, filename)
            
            # Save results
            self._save_results(output_path, stats, start_date, end_date)
            
            return stats, output_path
            
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            return None, "The specified file was not found"
        except pd.errors.EmptyDataError:
            logging.error("Empty data file")
            return None, "The data file is empty"
        except Exception as e:
            logging.error(f"Error processing weather statistics: {e}")
            return None, f"Error processing data: {str(e)}"

    def _save_results(self, filepath: str, stats: dict, start_date: str, end_date: str):
        """Save statistics results to a file"""
        content = f"""Weather Statistics
Period: {start_date} to {end_date}

Maximum Temperature: {stats['max_temp']:.1f}°C
Minimum Temperature: {stats['min_temp']:.1f}°C
Average Temperature: {stats['avg_temp']:.1f}°C
Total Precipitation: {stats['total_precipitation']:.1f}mm
"""
        with open(filepath, 'w') as f:
            f.write(content) 