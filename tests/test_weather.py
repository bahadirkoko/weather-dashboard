import pytest
import os

# Import from src package
from src import weather_fetcher
from src import database

# Test database path
TEST_DB_PATH = os.path.join(os.path.dirname(__file__), 'test_weather.db')


class TestWeatherFetcher:
    """Tests for weather fetching functionality."""

    def test_get_weather_valid_city(self):
        """Test fetching weather for a valid city"""
        weather_data = weather_fetcher.get_weather('London')

        assert weather_data is not None
        assert 'city' in weather_data
        assert 'temperature' in weather_data
        assert 'humidity' in weather_data
        assert weather_data['city'] == 'London'

    def test_get_weather_invalid_city(self):
        """Test fetching weather for invalid city returns None"""
        weather_data = weather_fetcher.get_weather('InvalidCityNameXYZ123')
        assert weather_data is None

    def test_weather_data_structure(self):
        """Test that weather data has correct structure"""
        weather_data = weather_fetcher.get_weather('Paris')

        if weather_data:
            required_fields = ['city', 'temperature', 'feels_like',
                               'humidity', 'description', 'timestamp']

            for field in required_fields:
                assert field in weather_data, f"Missing field: {field}"

            assert isinstance(weather_data['temperature'], (int, float))
            assert isinstance(weather_data['humidity'], int)
            assert isinstance(weather_data['city'], str)


class TestDatabase:
    """Tests for database functionality."""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup test database"""
        database.DB_PATH = TEST_DB_PATH
        database.init_database()

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

        result = database.save_weather(test_data)
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

        database.save_weather(test_data)
        history = database.get_weather_history('TestCity', limit=1)

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
            database.save_weather(data)

        cities = database.get_all_cities()

        assert len(cities) == 2
        assert 'London' in cities
        assert 'Paris' in cities


class TestIntegration:
    """Integration tests."""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup test database"""
        database.DB_PATH = TEST_DB_PATH
        database.init_database()

        yield

        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_fetch_and_save_workflow(self):
        """Test the complete workflow: fetch weather -> save -> retrieve"""
        weather_data = weather_fetcher.get_weather('Tokyo')
        assert weather_data is not None

        result = database.save_weather(weather_data)
        assert result is True

        history = database.get_weather_history('Tokyo', limit=1)
        assert len(history) == 1
        assert history[0]['city'] == 'Tokyo'
