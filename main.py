from flask import Flask, request

app = Flask(__name__)

@app.route('/receive-file', methods=['POST'])
def receive_file():
    try:
        # Receive file
        file = request.files['file']
        file_content = file.read().decode('utf-8')
        
        # Print the file content received from ESP32
        print(f"Received file content: {file_content}")

        # Send the content back to ESP32 as the response
        return file_content, 200
    except Exception as e:
        print(f"Error: {e}")
        return "Error processing file", 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
