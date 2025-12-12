from app import get_weather

API_KEY = "2795c9397a022c14ba85da4378c89181"

def main():
    city = input("Enter city name: ")

    result = get_weather(city, API_KEY)

    if result is None:
        print("City not found or error in API!")
    else:
        print(f"Temperature: {result['temperature']} °C")
        print(f"Humidity: {result['humidity']} %")
        print(f"Wind Speed: {result['wind_speed']} m/s")

if __name__ == "__main__":
    main()

