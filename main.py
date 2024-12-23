from flask import Flask, request, send_file
import os
from datetime import datetime

app = Flask(__name__)

# Directory to save audio files
UPLOAD_DIR = "audio_uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.route('/audio', methods=['POST'])
def upload_audio():
    # Save the audio file
    audio_data = request.data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_filename = f"{UPLOAD_DIR}/audio_{timestamp}.wav"
    
    with open(audio_filename, 'wb') as f:
        f.write(audio_data)
    
    print(f"Audio file saved: {audio_filename}")

    # TODO: Process the audio here (e.g., transcription)
    # For now, just return a placeholder response
    return "Could not understand the audio."

@app.route('/audio/<filename>', methods=['GET'])
def get_audio(filename):
    filepath = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=False)
    else:
        return "File not found.", 404

if __name__ == '__main__':
    app.run(debug=True)
