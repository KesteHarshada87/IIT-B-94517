import requests
import json

# API URL
url = "https://jsonplaceholder.typicode.com/posts"

# Fetch the data
response = requests.get(url)
data = response.json()

# Save to a file
with open("posts.json", "w") as f:
    json.dump(data, f, indent=4)

print("Data saved to posts.json")
