import os
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Serve the index.html file
@app.route('/', methods=['GET'])
def index():
    return send_file('index.html')

# Serve the script.js file
@app.route('/script.js', methods=['GET'])
def script():
    return send_file('script.js')

# Handle the file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        # Save the file to the 'uploaded_files' directory
        file.save(os.path.join('uploaded_files', file.filename))
        return "AAA"
        return jsonify({'message': 'File uploaded successfully.'}), 200
    else:
        return jsonify({'error': 'No file provided.'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
