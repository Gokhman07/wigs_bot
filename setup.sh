#!/bin/bash

# Update the system
sudo yum update -y

# Install Python and pip
sudo yum install python3 -y

# Install Flask and requests for the microservice
sudo pip3 install flask requests

# Install Rasa
sudo pip3 install rasa





# Create the Flask microservice script
cat <<EOF > telegram_rasa_service.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"
TELEGRAM_API_URL = "https://api.telegram.org/bot<YOUR_TELEGRAM_BOT_TOKEN>/sendMessage"

@app.route('/webhook', methods=['POST'])
def receive_message():
    data = request.json

    message = data['message']['text']
    chat_id = data['message']['chat']['id']

    rasa_response = requests.post(
        RASA_SERVER_URL,
        json={"sender": str(chat_id), "message": message}
    )

    rasa_responses = rasa_response.json()
    for response in rasa_responses:
        if "text" in response:
            requests.post(
                TELEGRAM_API_URL.replace("<YOUR_TELEGRAM_BOT_TOKEN>", "7335977975:AAEghYDIinBOEDwxTgzfiTo9XQDrsbVD4bI"),
                json={"chat_id": chat_id, "text": response["text"]}
            )

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
EOF

# Run Rasa in the background
nohup rasa run --enable-api --cors "*" &

# Run the Flask microservice in the background
nohup python3 telegram_rasa_service.py &
