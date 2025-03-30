"""
Weather tool for checking weather conditions.
"""

from ..core import register_tool


def get_weather(location: str):
    """
    Get weather information for a location (SIMULATED).
    
    Args:
        location: Location to get weather for
        
    Returns:
        str: Weather information
    """
    # This is a simulated weather tool for educational purposes
    import random
    
    # List of possible weather conditions
    conditions = ["Sunny", "Cloudy", "Partly Cloudy", "Rainy", "Thunderstorms", "Snowy", "Windy"]
    
    # Generate random weather data
    condition = random.choice(conditions)
    temperature = random.randint(0, 35)  # Celsius
    humidity = random.randint(30, 90)
    wind_speed = random.randint(0, 30)
    
    return f"""
Weather for {location} (SIMULATED):
Condition: {condition}
Temperature: {temperature}°C
Humidity: {humidity}%
Wind Speed: {wind_speed} km/h

Note: This is simulated data for educational purposes only.
"""


def register_weather_tool():
    """Register the weather tool with the agent."""
    register_tool(
        name="weather",
        description="Get the current weather for a location (simulated). Example input: {'location': 'New York'}",
        function=get_weather
    )