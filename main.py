import os
import wave
import speech_recognition as sr
from flask import Flask, request, jsonify

app = Flask(__name__)

# Save received audio
def save_audio(data, filename="received_audio.wav"):
    try:
        with open(filename, "wb") as f:
            f.write(data)
        return filename
    except Exception as e:
        print(f"Error saving audio: {e}")
        return None

# Transcribe audio using SpeechRecognition
def transcribe_audio(filename):
    try:
        with sr.AudioFile(filename) as source:
            audio = sr.Recognizer().record(source)
        return sr.Recognizer().recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except Exception as e:
        return f"Error: {e}"

# Play received audio (for testing)
def play_audio(filename):
    os.system(f"aplay {filename}")  # Linux command to play audio, adjust for your OS

@app.route('/upload', methods=['POST'])
def upload_audio():
    if request.method == 'POST':
        print("Receiving audio file...")
        audio_data = request.data  # Get the binary data of the audio
        if audio_data:
            filename = save_audio(audio_data)
            if filename:
                print(f"Audio saved to {filename}")
                transcription = transcribe_audio(filename)
                print(f"Transcription: {transcription}")

                # Play the received audio (Optional)
                play_audio(filename)

                return jsonify({"transcription": transcription}), 200
            else:
                return jsonify({"error": "Error saving audio."}), 400
        else:
            return jsonify({"error": "No audio data received."}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
