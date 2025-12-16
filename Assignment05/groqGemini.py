import os
import requests
import json
import time

user_prompt = input("Ask anything: ")


groq_api_key = os.getenv("GROQ_API_KEY")
groq_url = "https://api.groq.com/openai/v1/chat/completions"
groq_headers = {
    "Authorization": f"Bearer {groq_api_key}",
    "Content-Type": "application/json"
}
groq_data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "user", "content": user_prompt}
    ]
}

try:
    start = time.time()
    groq_response = requests.post(
        groq_url,
        headers=groq_headers,
        data=json.dumps(groq_data)
    )
    groq_time = time.time() - start
    groq_json = groq_response.json()
    
    if "choices" in groq_json and len(groq_json["choices"]) > 0:
        groq_output = groq_json["choices"][0]["message"]["content"]
    else:
        groq_output = f"Error: 'choices' not found in Groq response.\nFull Response: {groq_json}"

except Exception as e:
    groq_output = f"Groq API call failed: {e}"
    groq_time = None


gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_model = "models/text-bison-001"

# Use API key via query parameter
gemini_url = f"https://generativelanguage.googleapis.com/v1beta/{gemini_model}:generateText?key={gemini_api_key}"
gemini_headers = {
    "Content-Type": "application/json"
}

gemini_data = {
    "prompt": {"text": user_prompt},
    "temperature": 0.7,
    "candidateCount": 1,
    "maxOutputTokens": 512
}

try:
    start = time.time()
    gemini_response = requests.post(
        gemini_url,
        headers=gemini_headers,
        data=json.dumps(gemini_data)
    )
    gemini_time = time.time() - start
    gemini_json = gemini_response.json()
    
    if "candidates" in gemini_json and len(gemini_json["candidates"]) > 0:
        gemini_output = gemini_json["candidates"][0]["content"]
    else:
        gemini_output = f"Error: 'candidates' not found in Gemini response.\nFull Response: {gemini_json}"

except Exception as e:
    gemini_output = f"Gemini API call failed: {e}"
    gemini_time = None


print("\n========== GROQ RESPONSE ==========")
print(groq_output)
if groq_time is not None:
    print(f"Groq Time: {groq_time:.2f} seconds")

print("\n========== GEMINI RESPONSE ==========")
print(gemini_output)
if gemini_time is not None:
    print(f"Gemini Time: {gemini_time:.2f} seconds")


if groq_time is not None and gemini_time is not None:
    print("\n========== SPEED RESULT ==========")
    if groq_time < gemini_time:
        print("Groq is faster 🚀")
    else:
        print("Gemini is faster 🚀")
