from flask import Flask, request
import wave
import io
import base64
import speech_recognition as sr

app = Flask(__name__)

# Save audio data into an in-memory file-like object
def save_audio_in_memory(data):
    try:
        audio_buffer = io.BytesIO()
        with wave.open(audio_buffer, "wb") as wf:
            wf.setnchannels(1)  # Mono channel
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(16000)  # Sample rate
            wf.writeframes(data)
        audio_buffer.seek(0)  # Reset the pointer to the start of the file
        return audio_buffer
    except Exception as e:
        print(f"Error saving audio: {e}")
        return None

# Transcribe the audio from the in-memory file-like object
def transcribe_audio(audio_buffer):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_buffer) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except Exception as e:
        return f"Error: {e}"

@app.route('/hello', methods=['POST'])
def hello():
    try:
        # Get Base64-encoded audio data from the request
        base64_audio = request.data.decode('utf-8')

        if base64_audio == "EOF":
            return "End of audio received."

        if base64_audio:
            # Decode Base64 to raw binary data
            audio_data = base64.b64decode(base64_audio)

            # Save the audio data in memory
            audio_buffer = save_audio_in_memory(audio_data)
            if audio_buffer:
                transcription = transcribe_audio(audio_buffer)
            else:
                transcription = "Error saving audio."
        else:
            transcription = "No audio data received."

        return transcription  # Return the transcription as the response
    except Exception as e:
        return f"Server error: {e}"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
