import os
import json
import re
import requests
import zipfile
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables (for Google API Key)
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed text-based file extensions
ALLOWED_EXTENSIONS = {
    ".py", ".js", ".java", ".cpp", ".c", ".cs", ".kt", ".xml", ".json",
    ".yaml", ".yml", ".env", ".properties", ".sh", ".bat", ".gradle",
    ".md", ".html", ".css", ".ts", ".jsx", ".tsx", ".ini", ".toml",
    ".cfg", ".sql", ".pl", ".ipynb", ".dockerfile", ".txt", ".graphql", ".proto"
}

# Helper: Check if a file is valid
def is_allowed_file(filename):
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

# Extract and read contents of ZIP or single file
def extract_files(file_path):
    contents = []
    if file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if is_allowed_file(file):
                    with zip_ref.open(file) as f:
                        contents.append({"name": file, "content": f.read().decode('utf-8', errors='ignore')})
    else:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            contents.append({"name": os.path.basename(file_path), "content": f.read()})
    return contents

# Helper: Extract JSON content from Gemini response
def extract_json_from_response(response_text):
    try:
        # Regex to find JSON content inside ```json ... ```
        match = re.search(r'```json\s*(.*?)\s*```', response_text, re.S)
        if match:
            return match.group(1)
        return response_text
    except Exception as e:
        print(f"Error extracting JSON: {e}")
        return '{}'

# Analyze with Gemini 1.5 Pro API
def analyze_with_gemini(code_context):
    try:
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"You are an expert code reviewer and bug detector. Analyze the following code and return errors and misconfigurations in structured JSON:\n\n{code_context}"
                        }
                    ]
                }
            ]
        }

        # Call Gemini API with API key from environment
        response = requests.post(api_url, headers=headers, json=payload, params={"key": os.getenv("GOOGLE_API_KEY")})
        response.raise_for_status()

        # Extract and return the Gemini output
        gemini_response = response.json()
        print("Gemini API Response Status:", response.status_code)
        print("Gemini API Response:", json.dumps(gemini_response, indent=2))

        return gemini_response["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        print("Error during Gemini API call:", e)
        return json.dumps({"error": "Failed to analyze code"})

# Home route (Serve frontend)
@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

# Serve static files (CSS, JS, images)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('../frontend', filename)

# API route: Analyze uploaded file
@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    # Save and process the file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    try:
        # Extract contents for analysis
        files_content = extract_files(file_path)
        if not files_content:
            return jsonify({"error": "No valid code files found!"}), 400

        # Merge code for analysis
        code_context = "\n\n".join(f"File: {f['name']}\n{f['content']}" for f in files_content)

        # Analyze with Gemini
        analysis_result = analyze_with_gemini(code_context)

        # Extract JSON from Gemini response
        cleaned_json = extract_json_from_response(analysis_result)

        # Convert cleaned JSON string to Python dictionary
        return jsonify(json.loads(cleaned_json))

    except Exception as e:
        print("Error during file analysis:", e)
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        # Clean up uploaded file
        os.remove(file_path)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
