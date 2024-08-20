from flask import Flask, request, jsonify

app = Flask(__name__)

pending_request = False

@app.route('/send-temperature', methods=['POST'])
def receive_temperature():
    """Endpoint to receive temperature data from the Arduino."""
    temperature = request.json.get('temperature')
    if temperature is not None:
        return jsonify({'status': 'Temperature received', 'temperature': temperature}), 200
    else:
        return jsonify({'status': 'No temperature data received'}), 400

@app.route('/request-temperature', methods=['POST'])
def request_temperature():
    """Endpoint to trigger the Arduino to send temperature data."""
    global pending_request
    pending_request = True
    return jsonify({'status': 'Temperature request sent'}), 200

@app.route('/get-temperature', methods=['GET'])
def get_temperature():
    """Endpoint that the Arduino checks to see if the server needs temperature data."""
    global pending_request
    if pending_request:
        pending_request = False
        return jsonify({"command": "CHECK_TEMP"}), 200
    else:
        return jsonify({"command": "NO_REQUEST"}), 200

if __name__ == '__main__':
    # The server runs on all available IP addresses of the machine and listens on port 5000
    app.run(host='0.0.0.0', port=5000)
