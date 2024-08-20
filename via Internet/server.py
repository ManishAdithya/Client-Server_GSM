from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/send-temperature', methods=['POST'])
def receive_temperature():
    """Endpoint to receive temperature data from the client."""
    data = request.json
    if data and 'temperature' in data:
        temperature = data['temperature']
        return jsonify({'status': 'Temperature received', 'temperature': temperature}), 200
    else:
        return jsonify({'status': 'Invalid data received'}), 400

if __name__ == '__main__':
    # The server runs on all available IP addresses of the machine and listens on port 5000
    app.run(host='0.0.0.0', port=5000)
