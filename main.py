from flask import Flask, request
import wave
import speech_recognition as sr

app = Flask(__name__)

def save_audio(data, filename="received_audio.wav"):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(data)

def transcribe_audio(filename):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except Exception as e:
        return f"Error: {e}"

@app.route('/audio', methods=['POST'])
def audio():
    data = request.data
    if data.endswith(b"EOF"):
        data = data[:-3]  # Remove EOF marker
    save_audio(data)
    transcription = transcribe_audio("received_audio.wav")
    return transcription

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
