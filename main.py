from flask import Flask, request

app = Flask(__name__)

@app.route('/receive-file', methods=['POST'])
def receive_file():
    try:
        if 'file' not in request.files:
            return "No file part", 400

        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400

        file_content = file.read().decode('utf-8')
        print(f"Received file content: {file_content}")

        return file_content, 200
    except Exception as e:
        print(f"Error: {e}")
        return "Error processing file", 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
