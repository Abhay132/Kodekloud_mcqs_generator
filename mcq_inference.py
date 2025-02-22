from flask import Flask, request, jsonify
import pdfplumber
import docx
import google.generativeai as genai
import os

app = Flask(__name__)

# Load Google API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyBWPTMnCtqvmKakAbq986aCO51ciVpUszM"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro")


def extract_text(file_path):
    ext = file_path.split(".")[-1]
    if ext == "pdf":
        with pdfplumber.open(file_path) as pdf:
            text = " ".join([page.extract_text() for page in pdf.pages])
    elif ext == "docx":
        doc = docx.Document(file_path)
        text = " ".join([p.text for p in doc.paragraphs])
    return text


@app.route('/generate', methods=['POST'])
def generate_mcqs():
    file = request.files['file']
    num_questions = int(request.form['num_questions'])

    file_path = "/tmp/" + file.filename
    file.save(file_path)

    text = extract_text(file_path)
    prompt = f"Generate {num_questions} MCQs from this text:\n{text}"

    response = model.generate_content(prompt).text.strip()

    return jsonify({"mcqs": response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

