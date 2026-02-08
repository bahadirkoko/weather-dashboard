import sqlite3
import src.database as db
import src.weather_fetcher as weather
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class TestWeatherFetcher:

    def test_get_weather_valid_city(self):
        """Test fetching weather for a valid city"""
        weather_data = weather.get_weather('London')  # Changed!

        assert weather_data is not None
        assert 'city' in weather_data
        assert 'temperature' in weather_data
        assert 'humidity' in weather_data
        assert weather_data['city'] == 'London'

    def test_get_weather_invalid_city(self):
        """Test fetching weather for invalid city returns None"""
        weather_data = weather.get_weather('InvalidCityNameXYZ123')  # Changed!
        assert weather_data is None

    def test_weather_data_structure(self):
        """Test that weather data has correct structure"""
        weather_data = weather.get_weather('Paris')  # Changed!

        if weather_data:
            required_fields = ['city', 'temperature', 'feels_like',
                               'humidity', 'description', 'timestamp']

            for field in required_fields:
                assert field in weather_data, f"Missing field: {field}"

            assert isinstance(weather_data['temperature'], (int, float))
            assert isinstance(weather_data['humidity'], int)
            assert isinstance(weather_data['city'], str)


class TestDatabase:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup test database"""
        TEST_DB_PATH = os.path.join(
            os.path.dirname(__file__), 'test_weather.db')
        db.DB_PATH = TEST_DB_PATH  # Changed!
        db.init_database()  # Changed!

        yield

        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_save_weather(self):
        """Test saving weather data to database"""
        test_data = {
            'city': 'TestCity',
            'temperature': 20.5,
            'feels_like': 19.0,
            'humidity': 65,
            'description': 'clear sky',
            'timestamp': '2024-01-01T12:00:00'
        }

        result = db.save_weather(test_data)  # Changed!
        assert result is True

    def test_get_weather_history(self):
        """Test retrieving weather history"""
        test_data = {
            'city': 'TestCity',
            'temperature': 20.5,
            'feels_like': 19.0,
            'humidity': 65,
            'description': 'clear sky',
            'timestamp': '2024-01-01T12:00:00'
        }

        db.save_weather(test_data)  # Changed!
        history = db.get_weather_history('TestCity', limit=1)  # Changed!

        assert len(history) == 1
        assert history[0]['city'] == 'TestCity'
        assert history[0]['temperature'] == 20.5

    def test_get_all_cities(self):
        """Test getting list of all cities"""
        cities_data = [
            {'city': 'London', 'temperature': 15, 'feels_like': 14,
             'humidity': 70, 'description': 'cloudy', 'timestamp': '2024-01-01T12:00:00'},
            {'city': 'Paris', 'temperature': 18, 'feels_like': 17,
             'humidity': 65, 'description': 'sunny', 'timestamp': '2024-01-01T12:00:00'}
        ]

        for data in cities_data:
            db.save_weather(data)  # Changed!

        cities = db.get_all_cities()  # Changed!

        assert len(cities) == 2
        assert 'London' in cities
        assert 'Paris' in cities


class TestIntegration:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup test database"""
        TEST_DB_PATH = os.path.join(
            os.path.dirname(__file__), 'test_weather.db')
        db.DB_PATH = TEST_DB_PATH  # Changed!
        db.init_database()  # Changed!

        yield

        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_fetch_and_save_workflow(self):
        """Test the complete workflow: fetch weather -> save -> retrieve"""
        # Fetch weather
        weather_data = weather.get_weather('Tokyo')  # Changed!
        assert weather_data is not None

        # Save to database
        result = db.save_weather(weather_data)  # Changed!
        assert result is True

        # Retrieve from database
        history = db.get_weather_history('Tokyo', limit=1)  # Changed!
        assert len(history) == 1
        assert history[0]['city'] == 'Tokyo'
