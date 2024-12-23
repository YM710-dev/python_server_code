from flask import Flask, request
import wave
import speech_recognition as sr

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Save the received audio data
    try:
        data = request.data
        with open("received_audio.wav", "wb") as audio_file:
            audio_file.write(data)
    except Exception as e:
        print(f"Error saving audio: {e}")
        return "Error saving audio", 500

    # Convert the audio to text
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile("received_audio.wav") as source:
            audio = recognizer.record(source)
        transcription = recognizer.recognize_google(audio)
        print(f"Transcription: {transcription}")
        return transcription
    except sr.UnknownValueError:
        return "Could not understand audio"
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return "Error transcribing audio", 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
