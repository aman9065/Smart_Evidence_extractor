from flask import Flask, render_template, request, jsonify, session, send_file
import io
import os
import cv2
import pytesseract
from dotenv import load_dotenv
from pdf2image import convert_from_path
from openai import OpenAI
from docx import Document

load_dotenv()  
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
print("API Key loaded:", api_key is not None)

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY", "fallback_secret")

TEMP_FOLDER = "temp"
os.makedirs(TEMP_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'docx','txt'}

# POPPLER PATH IN OUR SYSTEM
POPPLER_PATH = r"C:\Users\amank\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clear_old_images():
    for file in os.listdir(TEMP_FOLDER):
        file_path = os.path.join(TEMP_FOLDER, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def summarize_with_openai(keywords):
    """Summarize extracted text based on multiple keywords using OpenAI"""
    output_path = os.path.join(TEMP_FOLDER, "output.txt")

    if not os.path.exists(output_path):
        return "No text file found. Please upload a file first."

    with open(output_path, "r", encoding="utf-8") as f:
        text = f.read()

    if not text.strip():
        return "No text found to summarize."

    # Convert to list if string is passed
    if isinstance(keywords, str):
        keywords = [kw.strip() for kw in keywords.split(",") if kw.strip()]

    if not keywords:
        return "No keywords provided."

    found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
    if not found_keywords:
        return f"None of the keywords {keywords} were found in the document."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Extract and summarize only the parts of this text related to the following keywords: {', '.join(found_keywords)}.\n\nText:\n{text}"}
            ],
            max_tokens=400
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        return f"Error generating summary: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])

def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file uploaded."})

        file = request.files['file']
        if file.filename == '':
            return jsonify({"status": "error", "message": "No file selected."})

        if not allowed_file(file.filename):
            return jsonify({"status": "error", "message": "Unsupported file type."})

        clear_old_images()
        
        filename = file.filename
        file_ext = filename.rsplit('.', 1)[1].lower()
        temp_path = os.path.join(TEMP_FOLDER, f"temp_upload.{file_ext}")
        file.save(temp_path)

        extracted_text = ""

        if file_ext == "pdf":
            pages = convert_from_path(temp_path, dpi=300, poppler_path=POPPLER_PATH)
            for i, page in enumerate(pages):
                temp_img_path = os.path.join(TEMP_FOLDER, f"page_{i+1}.png")
                page.save(temp_img_path, "PNG")
                image = cv2.imread(temp_img_path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                text = pytesseract.image_to_string(gray, lang="eng")
                extracted_text += f"\n--- Page {i+1} ---\n\n{text}"

        elif file_ext in ["png", "jpg", "jpeg",]:
            image = cv2.imread(temp_path)
            if image is None:
                return jsonify({"status": "error", "message": "Could not load image."})
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            extracted_text = pytesseract.image_to_string(gray, lang="eng")

        elif file_ext == "txt":
            with open(temp_path, "r", encoding="utf-8") as f:
                extracted_text = f.read()
        elif file_ext == "docx":
                   from docx import Document
                   doc = Document(temp_path)
                   extracted_text = "\n".join([para.text for para in doc.paragraphs])

        else:
            return jsonify({"status": "error", "message": f"Unsupported file type for OCR: {file_ext}"})

        session["extracted_text"] = extracted_text
        output_path = os.path.join(TEMP_FOLDER, "output.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        return jsonify({"status": "success", "message": "File uploaded successfully", "text": extracted_text})

    except Exception as e:
        import traceback; traceback.print_exc()  # log the actual error
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"})


@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json(silent=True) or {}
    keywords = data.get("keywords")

    if not keywords:
        keywords = request.form.get("keywords")

    if not keywords or not str(keywords).strip():
        return jsonify({"status": "error", "message": "No keywords provided."})

    summary = summarize_with_openai(keywords)
    session["last_summary"] = summary
    return jsonify({"status": "success", "summary": summary})

@app.route("/download_summary")
def download_summary():
    summary = session.get("last_summary")
    if not summary:
        return "No summary is available. Please generate a summary first."

    buffer = io.BytesIO()
    buffer.write(summary.encode("utf-8"))
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="summary.txt",
        mimetype="text/plain"
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
 







