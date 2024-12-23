from flask import Flask, request
import wave
import io
import pyaudio

app = Flask(__name__)

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    try:
        # Get audio file from the request
        audio_data = request.data
        print(f"Received audio of size: {len(audio_data)} bytes")

        # Save the received audio data to a file
        with open('received_audio.wav', 'wb') as f:
            f.write(audio_data)
        print("Audio file saved as 'received_audio.wav'.")

        # Play the received audio
        play_audio('received_audio.wav')

        return "Audio received and played", 200
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}", 500

def play_audio(filename):
    """Play the received audio file."""
    try:
        wf = wave.open(filename, 'rb')
        p = pyaudio.PyAudio()
        
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        print("Playing audio...")

        chunk_size = 1024
        data = wf.readframes(chunk_size)
        while data:
            stream.write(data)
            data = wf.readframes(chunk_size)

        stream.stop_stream()
        stream.close()
        p.terminate()

        print("Audio playback finished.")
    except Exception as e:
        print(f"Error playing audio: {e}")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
