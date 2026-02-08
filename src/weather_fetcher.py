import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# load env variables
load_dotenv()


def get_weather(city):
    """
    Fetches current weather data for a given city.
    """
    # get api key from the environment variable secure!
    api_key = os.getenv('WEATHER_API_KEY')

    if not api_key:
        raise ValueError('WEATHER_API_KEY not found in .env file!!!.')

    # openweathermap API endpoint
    base_url = 'http://api.openweathermap.org/data/2.5/weather'

    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # celcius we can use 'imperial' for fahrenheit
    }

    try:
        # make the api request
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # raises error if request failed

        # conert JSON response to a dict
        data = response.json()

        # extract only the data we care about

        weather_data = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
            'timestamp': datetime.now().isoformat()
        }

        return weather_data

    except requests.exceptions.RequestException as e:
        print(f'Error fetching weather: {e}')
        return None


def display_weather(weather_data):
    """
    Prints weather data in a nice format
    Seperates displaying from fetching, single responsibility principle
    """

    if not weather_data:
        print('No weather data to display.')
        return

    print(f"\n{'='*50}")
    print(f"Weather in {weather_data['city']}")
    print(f"{'='*50}")
    print(f"Temperature: {weather_data['temperature']}°C")
    print(f"Feels like: {weather_data['feels_like']}°C")
    print(f"Humidity: {weather_data['humidity']}%")
    print(f"Description: {weather_data['description']}")
    print(f"Time: {weather_data['timestamp']}")
    print(f"{'='*50}\n")
