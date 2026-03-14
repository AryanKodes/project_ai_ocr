import os
import json
import re
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from utils import extract_content, chain, extract_xml

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Updated prompt to ensure the LLM returns a predictable JSON structure for the frontend
data_processing_steps = [
    "Analyse the text and write it in a clear language which is easy to understand.",
    "Extract the following fields if present: Name, Date of birth, Address, Phone, Email, Income, Employer, Education, Certifications, and all other relevant fields.",
    """Analyse the above and output the information strictly in valid JSON format inside the below xml tag.
    Do not use placeholders, actually classify the document.
    
    <json_format>
    {
        "document_type": "Classify the document here (e.g., Resume, Invoice, Bank Statement, Passport, etc.)",
        "extracted_data": {
            "name": "...",
            "email": "..."
        }
    }
    </json_format>"""
]

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            # 1. Extract text using your utils.py
            data = extract_content(file_path)["raw_text"]
            
            # 2. Run the LLM chain
            final_data = chain(data, data_processing_steps)
            
            # 3. Extract and parse the JSON
            json_string = extract_xml(final_data, "json_format")
            
            # Clean up potential markdown formatting from the LLM
            json_string = re.sub(r'```json\n?', '', json_string)
            json_string = re.sub(r'```\n?', '', json_string).strip()
            
            parsed_json = json.loads(json_string)

            # Cleanup file after processing
            os.remove(file_path)

            return jsonify(parsed_json)

        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)