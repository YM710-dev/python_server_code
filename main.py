from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/send-data', methods=['POST'])
def receive_data():
    data = request.get_json()
    print(f"Received data from ESP32: {data}")
    return jsonify({"status": "success", "message": "Data received!"})

@app.route('/get-command', methods=['GET'])
def send_command():
    # Example of sending a command to the ESP32
    return jsonify({"command": "turn_on_led"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
