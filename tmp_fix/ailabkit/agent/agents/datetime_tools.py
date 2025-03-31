"""
Date and time tools for working with temporal data.

This agent provides tools for date calculations, formatting, and timezone conversions.
"""

import datetime
from ..core import register_tool


def date_diff(date1: str, date2: str) -> str:
    """
    Calculate the difference between two dates.
    
    Args:
        date1: First date in format YYYY-MM-DD
        date2: Second date in format YYYY-MM-DD
        
    Returns:
        str: The difference between the dates in days, months, and years
    """
    try:
        # Parse the dates
        date1_obj = datetime.datetime.strptime(date1, "%Y-%m-%d").date()
        date2_obj = datetime.datetime.strptime(date2, "%Y-%m-%d").date()
        
        # Ensure date1 is earlier than date2
        if date1_obj > date2_obj:
            date1_obj, date2_obj = date2_obj, date1_obj
            dates_swapped = True
        else:
            dates_swapped = False
        
        # Calculate difference in days
        delta = date2_obj - date1_obj
        days_diff = delta.days
        
        # Calculate difference in months and years (approximate)
        years = date2_obj.year - date1_obj.year
        months = date2_obj.month - date1_obj.month
        
        if date2_obj.day < date1_obj.day:
            months -= 1
            
        if months < 0:
            years -= 1
            months += 12
        
        # Create the result string
        if dates_swapped:
            result = "Date 2 is earlier than Date 1. Calculating difference with dates swapped.\n"
        else:
            result = ""
            
        result += f"From {date1_obj.strftime('%Y-%m-%d')} to {date2_obj.strftime('%Y-%m-%d')}:\n"
        result += f"- Days: {days_diff}\n"
        
        if years > 0 or months > 0:
            year_text = f"{years} year{'s' if years != 1 else ''}" if years > 0 else ""
            month_text = f"{months} month{'s' if months != 1 else ''}" if months > 0 else ""
            
            if years > 0 and months > 0:
                result += f"- Approximately: {year_text} and {month_text}"
            else:
                result += f"- Approximately: {year_text}{month_text}"
        
        # Add day of week information
        result += f"\n\nDay of week for {date1}: {date1_obj.strftime('%A')}"
        result += f"\nDay of week for {date2}: {date2_obj.strftime('%A')}"
        
        return result
        
    except ValueError as e:
        return f"Error: Invalid date format. Please use YYYY-MM-DD format. {str(e)}"


def format_date(date_str: str, format_code: str = "iso") -> str:
    """
    Format a date in various standard formats.
    
    Args:
        date_str: Date in format YYYY-MM-DD
        format_code: Format code (iso, us, eu, long, short, etc.)
        
    Returns:
        str: The formatted date
    """
    try:
        # Parse the date
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Define format mapping
        formats = {
            "iso": "%Y-%m-%d",                    # 2023-04-15
            "us": "%m/%d/%Y",                     # 04/15/2023
            "eu": "%d/%m/%Y",                     # 15/04/2023
            "long": "%B %d, %Y",                  # April 15, 2023
            "short": "%b %d, %Y",                 # Apr 15, 2023
            "weekday": "%A, %B %d, %Y",           # Saturday, April 15, 2023
            "weekday_short": "%a, %b %d, %Y",     # Sat, Apr 15, 2023
            "year_month": "%B %Y",                # April 2023
            "month_year": "%m-%Y",                # 04-2023
            "day_month": "%d %B",                 # 15 April
            "month_day": "%B %d",                 # April 15
        }
        
        # Check if format_code is valid
        if format_code not in formats:
            valid_formats = ", ".join(formats.keys())
            return f"Invalid format code. Valid options are: {valid_formats}"
        
        # Format the date
        formatted_date = date_obj.strftime(formats[format_code])
        
        return f"Original date: {date_str}\nFormatted date ({format_code}): {formatted_date}"
        
    except ValueError:
        return "Error: Invalid date format. Please use YYYY-MM-DD format."


def days_until(target_date: str) -> str:
    """
    Calculate the number of days until a specified date.
    
    Args:
        target_date: Target date in format YYYY-MM-DD
        
    Returns:
        str: The number of days until the target date
    """
    try:
        # Parse the target date
        target = datetime.datetime.strptime(target_date, "%Y-%m-%d").date()
        
        # Get today's date
        today = datetime.date.today()
        
        # Calculate difference
        delta = target - today
        days = delta.days
        
        # Prepare response based on whether the date is in the past, present, or future
        if days < 0:
            return f"The date {target_date} was {abs(days)} day{'s' if abs(days) != 1 else ''} ago."
        elif days == 0:
            return f"The date {target_date} is today!"
        else:
            # Calculate date components
            years = 0
            months = 0
            remaining_days = days
            
            # Rough approximation of years and months
            while remaining_days >= 365:
                years += 1
                remaining_days -= 365
                
            while remaining_days >= 30:
                months += 1
                remaining_days -= 30
            
            # Create response
            result = f"Days until {target_date}: {days} day{'s' if days != 1 else ''}"
            
            if years > 0 or months > 0:
                result += " ("
                
                if years > 0:
                    result += f"{years} year{'s' if years != 1 else ''}"
                    if months > 0:
                        result += " and "
                        
                if months > 0:
                    result += f"{months} month{'s' if months != 1 else ''}"
                    
                result += ")"
            
            # Add the day of the week
            result += f"\nThat will be a {target.strftime('%A')}."
            
            return result
            
    except ValueError:
        return "Error: Invalid date format. Please use YYYY-MM-DD format."


def register_datetime_tools():
    """Register all datetime tools with the agent."""
    register_tool(
        "date_diff",
        "Calculate the difference between two dates in format YYYY-MM-DD",
        date_diff
    )
    
    register_tool(
        "format_date",
        "Format a date (YYYY-MM-DD) using various standard formats (iso, us, eu, long, short)",
        format_date
    )
    
    register_tool(
        "days_until",
        "Calculate the number of days until a given date in format YYYY-MM-DD",
        days_until
    )