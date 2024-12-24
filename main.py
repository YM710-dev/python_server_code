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
        recognizer = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except Exception as e:
        return f"Error: {e}"

@app.route('/hello', methods=['POST'])
def hello():
    message = request.data
    if message == b"EOF":
        print("Received EOF. No more data expected.")
        return "EOF received"

    print("Received audio data. Processing...")
    filename = save_audio(message)
    if isinstance(filename, str) and filename.startswith("Error"):
        print(filename)
        return filename, 500

    transcription = transcribe_audio(filename)
    print(f"Transcription: {transcription}")
    return transcription

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
