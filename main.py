from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

# Directory to save audio files
AUDIO_SAVE_PATH = "./audio_files"
os.makedirs(AUDIO_SAVE_PATH, exist_ok=True)

@app.route('/audio', methods=['POST'])
def receive_audio():
    try:
        # Save the incoming audio file
        audio_file_path = os.path.join(AUDIO_SAVE_PATH, "recorded_audio.wav")

        with open(audio_file_path, "wb") as f:
            f.write(request.data)

        print(f"Audio file saved at: {audio_file_path}")

        # Return response for debugging
        return jsonify({"message": "Audio received", "file_path": audio_file_path})

    except Exception as e:
        print(f"Error receiving audio: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/audio/play', methods=['GET'])
def play_audio():
    audio_file_path = os.path.join(AUDIO_SAVE_PATH, "recorded_audio.wav")
    if os.path.exists(audio_file_path):
        return send_file(audio_file_path, as_attachment=True)
    else:
        return jsonify({"error": "Audio file not found"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
