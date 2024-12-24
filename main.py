from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.data  # Receive raw file content
        with open("received_file.txt", "wb") as f:
            f.write(file)
        print("File received and saved as received_file.txt")

        # Read the file content and send it back
        with open("received_file.txt", "r") as f:
            content = f.read()
        return content, 200
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
