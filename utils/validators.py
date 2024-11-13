from datetime import datetime
import re

class DateValidator:
    DATE_FORMAT = "%Y-%m-%d"
    DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')

    @staticmethod
    def validate_date_format(date_string: str) -> tuple[bool, str]:
        """
        Validates if the date string matches YYYY-MM-DD format
        Returns (is_valid, error_message)
        """
        if not date_string:
            return False, "Date cannot be empty"
            
        if not DateValidator.DATE_PATTERN.match(date_string):
            return False, "Date must be in YYYY-MM-DD format"
            
        try:
            datetime.strptime(date_string, DateValidator.DATE_FORMAT)
            return True, ""
        except ValueError:
            return False, "Invalid date value"
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> tuple[bool, str]:
        """
        Validates if the date range is valid
        Returns (is_valid, error_message)
        """
        # First validate both dates format
        start_valid, start_error = DateValidator.validate_date_format(start_date)
        if not start_valid:
            return False, f"Start date error: {start_error}"
            
        end_valid, end_error = DateValidator.validate_date_format(end_date)
        if not end_valid:
            return False, f"End date error: {end_error}"
            
        # Convert strings to datetime objects
        start_dt = datetime.strptime(start_date, DateValidator.DATE_FORMAT)
        end_dt = datetime.strptime(end_date, DateValidator.DATE_FORMAT)
        
        # Check if end date is not before start date
        if end_dt < start_dt:
            return False, "End date cannot be before start date"
            
        # Check if date range is not in the future
        today = datetime.now()
        if start_dt > today or end_dt > today:
            return False, "Dates cannot be in the future"
            
        return True, ""
