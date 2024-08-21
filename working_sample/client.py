import requests
import random
import time
from flask import Flask, jsonify

app = Flask(__name__)

SERVER_URL_POST = "http://127.0.0.1:5000/send-temperature"  # Replace <server_ip> with your server's IP or domain

def generate_temperature():
    return round(random.uniform(20.0, 30.0), 2)

def send_temperature():
    temperature = generate_temperature()
    data = {'temperature': temperature}
    try:
        response = requests.post(SERVER_URL_POST, json=data)
        print(f"Sent temperature: {temperature}C, Server Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send temperature: {e}")

@app.route('/get-temperature', methods=['GET'])
def get_temperature():
    temperature = generate_temperature()
    return jsonify({'temperature': temperature}), 200

if __name__ == "__main__":
    # Run the Flask server to listen for manual requests from the server
    from threading import Thread

    def run_flask():
        app.run(host='0.0.0.0', port=5001)

    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Send temperature data every 20 seconds
    while True:
        send_temperature()
        time.sleep(10)

# End of client.py