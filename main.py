from flask import Flask, request

app = Flask(__name__)

@app.route('/hello', methods=['POST'])
def hello():
    message = request.data.decode()  # Decode the incoming message
    print(f"ESP says: {message}")
    return "Hello " + message  # Respond with a simple message

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
