from flask import Flask, request
import speech_recognition as sr
import os

app = Flask(__name__)

@app.route('/receive-audio', methods=['POST'])
def receive_audio():
    try:
        # Save the received WAV file
        wav_file = "received_audio.wav"
        with open(wav_file, "wb") as f:
            f.write(request.data)
        print(f"Received WAV file saved as {wav_file}")

        # Transcribe the WAV file
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file) as source:
            audio_data = recognizer.record(source)
        transcription = recognizer.recognize_google(audio_data)
        print(f"Transcription: {transcription}")

        # Clean up the file
        os.remove(wav_file)

        return transcription, 200
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
