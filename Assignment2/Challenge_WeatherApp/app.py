import requests

api_key = "2795c9397a022c14ba85da4378c89181"  

city = input("Enter city: ")

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

response = requests.get(url)

print("Status:", response.status_code)

# Convert JSON response
data = response.json()

# Check if city is found
if response.status_code == 200:
    print("\n--- Weather Report ---")
    print("City:", data["name"])
    print("Temperature:", data["main"]["temp"], "°C")
    print("Humidity:", data["main"]["humidity"], "%")
    print("Wind Speed:", data["wind"]["speed"], "m/s")
else:
    # Error output from API
    print("\nError:", data.get("message", "Something went wrong"))
