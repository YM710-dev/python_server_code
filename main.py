from flask import Flask, request
import wave
import os
import speech_recognition as sr

app = Flask(__name__)

@app.route('/receive-audio', methods=['POST'])
def receive_audio():
    try:
        # Save the received audio file
        audio_file = "received_audio.raw"
        with open(audio_file, "wb") as f:
            f.write(request.data)
        print(f"Received audio file saved as {audio_file}")

        # Convert RAW to WAV
        wav_file = "received_audio.wav"
        with wave.open(wav_file, "wb") as wav:
            wav.setnchannels(1)  # Mono
            wav.setsampwidth(2)  # 16-bit audio
            wav.setframerate(16000)  # Sample rate
            with open(audio_file, "rb") as raw:
                wav.writeframes(raw.read())
        print(f"Converted RAW file to WAV: {wav_file}")

        # Transcribe the WAV file
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file) as source:
            audio_data = recognizer.record(source)
        transcription = recognizer.recognize_google(audio_data)
        print(f"Transcription: {transcription}")

        # Clean up files
        os.remove(audio_file)
        os.remove(wav_file)

        return transcription, 200
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
