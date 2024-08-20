from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# Store the latest temperature received from the client
latest_temperature = None
last_updated = None

@app.route('/send-temperature', methods=['POST'])
def receive_temperature():
    global latest_temperature, last_updated
    data = request.json
    latest_temperature = data.get('temperature')
    last_updated = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return jsonify({'status': 'Temperature received', 'temperature': latest_temperature}), 200

@app.route('/request-temperature', methods=['GET'])
def request_temperature():
    if latest_temperature is not None:
        return jsonify({
            'status': 'Temperature fetched',
            'temperature': latest_temperature,
            'last_updated': last_updated
        }), 200
    else:
        return jsonify({'status': 'No data available'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
