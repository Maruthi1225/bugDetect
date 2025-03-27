# Bug Detection System

## Overview
The Bug Detection System is an AI-powered tool designed to analyze code files, identify potential bugs, and suggest improvements. This project leverages advanced AI models to detect errors in source code, enhancing software development efficiency.

## Features
- AI-driven bug detection
- Syntax and logical error identification
- User-friendly web interface for uploading code files
- JSON-based structured output for analysis results
- Downloadable report for detected issues

## Installation
### Prerequisites
Ensure you have the following installed:
- Python (>=3.8)
- pip
- Node.js (if frontend modifications are required)
- A virtual environment (recommended)

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/bug-detection.git
   cd bug-detection
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirement.txt
   ```

## Running the Application
### Backend (Flask Server)
1. Navigate to the backend folder:
   ```sh
   cd backend
   ```
2. Start the Flask server:
   ```sh
   python app.py
   ```
3. The server should now be running at `http://127.0.0.1:5000`

### Frontend (HTML, CSS, JavaScript)
1. Open `index.html` in a web browser or use a local server:
   ```sh
   cd frontend
   python -m http.server 8000  # Run a simple HTTP server
   ```
2. Access the frontend at `http://127.0.0.1:8000`

## API Endpoints
- `POST /analyze`
  - **Description**: Uploads a code file and analyzes it for bugs.
  - **Parameters**: Code file in multipart form-data.
  - **Response**: JSON object containing detected issues and suggestions.

## Configuration
Create a `.env` file and add necessary API keys if required:
```sh
GEMINI_API_KEY=your_api_key_here
FLASK_ENV=development
```

## Troubleshooting
- **Server not starting?**
  - Ensure Python dependencies are installed properly.
  - Run `python app.py` inside the `backend/` folder.
- **Frontend not working?**
  - Check the browser console for errors.
  - Verify the backend is running and accessible at `127.0.0.1:5000`.
- **API returning errors?**
  - Ensure proper API keys are configured.
  - Check `app.py` for possible endpoint mismatches.

## Contributors
- Maruthi1225
- EshwarCharan

## License
This project is licensed under the MIT License.

