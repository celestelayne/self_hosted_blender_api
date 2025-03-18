# import flask
from flask import Flask, request, jsonify
import subprocess
import os

# create an app instance
app = Flask(__name__)

# Get Blender path from Homebrew
BLENDER_PATH = "/Applications/Blender.app/Contents/MacOS/Blender"

# create the route that handles the file logic
@app.route('/process_model', methods=['POST'])
def process_model():
    file_path = request.json.get("file_path")

    if not os.path.exists(file_path):
        return jsonify({
            "error": "File not found."
        }), 400

    output_path = "/tmp/processed_model.glb"

    # Run Blender CLI command
    command = [
        BLENDER_EXEC, "--background", "--python", "process_script.py",
        "--", file_path, output_path
    ]
    subprocess.run(command, check=True)

    return jsonify({
        "status": "success", 
        "output_file": output_path
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)