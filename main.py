from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def message():
    data = request.get_json()
    if data and 'message' in data:
        print(f"Message received: {data['message']}")
        return jsonify({'response': 'Hello from Server'})
    return jsonify({'error': 'Invalid message'}), 400

app.run(host='0.0.0.0', port=80)