from flask import Flask, request
import wave
import speech_recognition as sr

app = Flask(__name__)

def save_audio(data, filename="received_audio.wav"):
    try:
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(data)
        return filename
    except Exception as e:
        return f"Error saving audio: {e}"

def transcribe_audio(filename):
    try:
        with sr.AudioFile(filename) as source:
            audio = sr.Recognizer().record(source)
        return sr.Recognizer().recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except Exception as e:
        return f"Error: {e}"

@app.route('/upload', methods=['POST'])
def upload_audio():
    audio_data = request.data
    print(f"Received {len(audio_data)} bytes of audio data")

    # Save the audio data to a file
    audio_file = save_audio(audio_data)
    transcription = transcribe_audio(audio_file) if audio_file else "Error saving audio."

    return transcription  # Return transcription result to ESP32

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
