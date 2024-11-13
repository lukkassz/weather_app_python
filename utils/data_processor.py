import pandas as pd
import os
from datetime import datetime
import logging

class KNMIDataProcessor:
    @staticmethod
    def read_knmi_file(file_path: str) -> pd.DataFrame:
        """Reads KNMI data file and returns a pandas DataFrame"""
        try:
            # Read KNMI data file (you might need to adjust the format based on actual file)
            df = pd.read_csv(file_path, delimiter=',')
            return df
        except Exception as e:
            logging.error(f"Error reading KNMI file: {e}")
            return None

    @staticmethod
    def calculate_statistics(df: pd.DataFrame, start_date: str, end_date: str) -> dict:
        """Calculates weather statistics for given period"""
        try:
            # Filter data for the given period
            mask = (df['DATE'] >= start_date) & (df['DATE'] <= end_date)
            period_data = df.loc[mask]

            # Calculate statistics
            stats = {
                'max_temp': period_data['TEMP'].max(),
                'min_temp': period_data['TEMP'].min(),
                'avg_temp': period_data['TEMP'].mean(),
                'total_precipitation': period_data['PRECIPITATION'].sum()
            }
            return stats
        except Exception as e:
            logging.error(f"Error calculating statistics: {e}")
            return None

    @staticmethod
    def save_statistics(stats: dict, start_date: str, end_date: str) -> str:
        """Saves statistics to a file"""
        try:
            # Create output directory if it doesn't exist
            output_dir = "data/output"
            os.makedirs(output_dir, exist_ok=True)

            # Create filename
            filename = f"weerstatistieken-{start_date}-{end_date}.txt"
            filepath = os.path.join(output_dir, filename)

            # Format statistics
            content = f"""Weather Statistics ({start_date} to {end_date})
            
Maximum Temperature: {stats['max_temp']:.1f}°C
Minimum Temperature: {stats['min_temp']:.1f}°C
Average Temperature: {stats['avg_temp']:.1f}°C
Total Precipitation: {stats['total_precipitation']:.1f}mm
"""
            # Save to file
            with open(filepath, 'w') as f:
                f.write(content)

            return filepath
        except Exception as e:
            logging.error(f"Error saving statistics: {e}")
            return None
