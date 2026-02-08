from weather_fetcher import get_weather
from database import init_database, save_weather
import time
from datetime import datetime

# Cities we want to track
TRACKED_CITIES = ['London', 'New York', 'Tokyo', 'Paris', 'Sydney']


def fetch_all_weather():
    """
    Fetches weather for all tracked cities.

    Why: This is our data collection pipeline.
    In production, this would run on a schedule (hourly, daily, etc.)
    """
    print(f"\n{'='*60}")
    print(
        f"🔄 PIPELINE RUN STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    success_count = 0
    fail_count = 0

    for city in TRACKED_CITIES:
        print(f"Fetching weather for {city}...", end=" ")

        weather_data = get_weather(city)

        if weather_data:
            save_weather(weather_data)
            print(f"✓ Success ({weather_data['temperature']}°C)")
            success_count += 1
        else:
            print(f"✗ Failed")
            fail_count += 1

        # Be nice to the API - wait 1 second between requests
        time.sleep(1)

    print(f"\n{'='*60}")
    print(f"📊 Pipeline Summary:")
    print(f"   ✓ Successful: {success_count}")
    print(f"   ✗ Failed: {fail_count}")
    print(f"{'='*60}\n")


def run_continuous_pipeline(interval_minutes=60):
    """
    Runs the pipeline continuously at specified intervals.

    Args:
        interval_minutes: How often to fetch data (default 60 minutes)

    Why: Simulates a real production data pipeline.
    In AWS, we'd use CloudWatch Events or Lambda scheduled functions.
    """
    print(f"🚀 Starting continuous pipeline (every {interval_minutes} minutes)")
    print("Press Ctrl+C to stop\n")

    init_database()

    try:
        while True:
            fetch_all_weather()

            next_run = datetime.now()
            next_run = next_run.replace(second=0, microsecond=0)

            print(f"💤 Sleeping for {interval_minutes} minutes...")
            print(f"Next run at: {next_run.strftime('%H:%M')}\n")

            time.sleep(interval_minutes * 60)

    except KeyboardInterrupt:
        print("\n\n👋 Pipeline stopped by user")


if __name__ == "__main__":
    # For testing: run once
    init_database()
    fetch_all_weather()

    # Uncomment below to run continuously every 60 minutes
    # run_continuous_pipeline(interval_minutes=60)
