from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

client_url = "http://127.0.0.1:5001/get-temperature"  # Replace <client_ip> with the client’s IP address

@app.route('/send-temperature', methods=['POST'])
def receive_temperature():
    data = request.json
    temperature = data.get('temperature')
    return jsonify({'status': 'Temperature received', 'temperature': temperature}), 200

@app.route('/request-temperature', methods=['GET'])
def request_temperature():
    response = requests.get(client_url)
    if response.status_code == 200:
        temperature = response.json().get('temperature')
        return jsonify({'status': 'Temperature fetched', 'temperature': temperature}), 200
    else:
        return jsonify({'status': 'Failed to fetch temperature from client'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
