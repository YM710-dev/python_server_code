from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = './uploaded_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/receive-file', methods=['POST'])
def receive_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Save the file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Read the contents of the file
    with open(file_path, 'r') as f:
        content = f.read()

    # Send the content back as the response
    return jsonify({"message": "File received", "content": content})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
