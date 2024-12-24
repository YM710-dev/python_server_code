from flask import Flask, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/receive-audio', methods=['POST'])
def receive_audio():
    try:
        file = request.files['file']
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, 'received_audio.wav')
            file.save(file_path)
            print(f"Received WAV file saved as {file_path}")
            return "Success", 200
        else:
            return "No file received", 400
    except Exception as e:
        print(f"Error: {e}")
        return "Error", 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
