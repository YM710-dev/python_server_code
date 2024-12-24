from flask import Flask, request

app = Flask(__name__)

@app.route('/receive-txt', methods=['POST'])
def receive_txt():
    try:
        # Check if a file was sent
        if 'file' not in request.files:
            return "No file part in the request", 400
        
        file = request.files['file']

        # Save the file to disk
        file_path = f"received_{file.filename}"
        file.save(file_path)
        print(f"File saved as: {file_path}")

        # Read the content of the file
        with open(file_path, "r") as f:
            content = f.read()
        print(f"File content: {content}")

        # Modify the content (append a response)
        modified_content = f"{content}\nServer: File processed successfully!"

        # Return the modified content to the ESP32
        return modified_content, 200
    except Exception as e:
        print(f"Error: {e}")
        return "Error processing the file", 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
