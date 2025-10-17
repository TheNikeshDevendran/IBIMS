import requests
import json
API_KEY = "AIzaSyBUTtsGCIMdvJVvPYkpDmsPwuXRTzycjSw"
MODEL_NAME = "gemini-1.5-flash-latest"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
headers = {
    "Content-Type": "application/json"
}

while True:
    user_input = input("You: ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Exiting Gemini chat.")
        break
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": user_input}
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        result = response.json()
        text_output = result['candidates'][0]['content']['parts'][0]['text']
        print("🤖 Gemini:", text_output)
    else:
        print("Error:",response.status_code)
        print(response.text)
