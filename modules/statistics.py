from utils.data_processor import KNMIDataProcessor
from datetime import datetime
import logging

class WeatherStatistics:
    def __init__(self):
        self.processor = KNMIDataProcessor()

    def process_period(self, file_path: str, start_date: str, end_date: str) -> tuple:
        """Processes weather data for given period and returns statistics"""
        try:
            # Read data
            df = self.processor.read_knmi_file(file_path)
            if df is None:
                return None, "Failed to read KNMI data file"

            # Calculate statistics
            stats = self.processor.calculate_statistics(df, start_date, end_date)
            if stats is None:
                return None, "Failed to calculate statistics"

            # Save results
            output_file = self.processor.save_statistics(stats, start_date, end_date)
            if output_file is None:
                return None, "Failed to save statistics"

            return stats, output_file
        except Exception as e:
            logging.error(f"Error processing weather statistics: {e}")
            return None, str(e)
