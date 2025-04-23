import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS # Needed for requests from browser (TurboWarp)
from dotenv import load_dotenv  # Import load_dotenv

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
# --- End Configuration ---

if not GEMINI_API_KEY:
    print("ERROR: Gemini API Key not set. Please set the GEMINI_API_KEY variable.")

if GEMINI_API_KEY:
     try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
     except Exception as e:
        print(f"ERROR: Could not configure Gemini client: {e}")
        # Consider exiting


app = Flask(__name__)
# Allow requests from any origin (TurboWarp). For production, restrict this!
CORS(app)

@app.route('/ask-gemini', methods=['POST'])
def ask_gemini():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "Missing 'prompt' in request data"}), 400

    if not GEMINI_API_KEY:
         print("Warning: API Key not set. Returning simulated response.")
         simulated_response = f"Simulated answer to: {prompt}"
         return jsonify({"response": simulated_response})


    # --- Actual Gemini API Call ---
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)

        gemini_response_text = response.text # Common case

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({"error": f"Failed to get response from Gemini: {e}"}), 500
    # --- End API Call ---

    return jsonify({"response": gemini_response_text})

if __name__ == '__main__':
    print("Starting server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000) # Port 5000 is common for Flask dev
