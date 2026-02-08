from weather_fetcher import get_weather, display_weather
from database import init_database, save_weather, get_weather_history, get_all_cities
from pipeline import fetch_all_weather  # NEW IMPORT


def main():
    init_database()

    while True:
        print("\n" + "="*50)
        print("WEATHER DASHBOARD")
        print("="*50)
        print("1. Get current weather")
        print("2. View weather history")
        print("3. View all tracked cities")
        print("4. Run data collection pipeline")  # NEW OPTION
        print("5. Exit")  # Changed from 4 to 5
        print("="*50)

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            city = input("Enter city name: ")
            weather_data = get_weather(city)
            if weather_data:
                display_weather(weather_data)
                save_weather(weather_data)

        elif choice == '2':
            city = input("Enter city name: ")
            history = get_weather_history(city, limit=5)

            if history:
                print(f"\n📊 Last 5 weather records for {city}:")
                print("-" * 70)
                for record in history:
                    print(f"{record['timestamp'][:19]} | "
                          f"Temp: {record['temperature']}°C | "
                          f"Humidity: {record['humidity']}% | "
                          f"{record['description']}")
                print("-" * 70)
            else:
                print(f"No history found for {city}")

        elif choice == '3':
            cities = get_all_cities()
            if cities:
                print(f"\n🌍 Cities tracked: {', '.join(cities)}")
            else:
                print("No cities tracked yet!")

        elif choice == '4':  # NEW OPTION
            print("\n🔄 Running data collection pipeline...")
            fetch_all_weather()

        elif choice == '5':  # Changed from 4
            print("Goodbye! 👋")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
