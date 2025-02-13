from flask import Flask, render_template, request, jsonify
import os
from model import calculate_similarity
import chardet
from PyPDF2 import PdfReader  # Add this for PDF support

app = Flask(__name__)

# Ensure the upload folders exist
UPLOAD_FOLDER = 'data/resumes'
JOB_DESC_FOLDER = 'data/job_descriptions'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(JOB_DESC_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files or 'job_description' not in request.files:
        return "No file uploaded", 400
    
    resume = request.files['resume']
    job_description = request.files['job_description']
    
    # Save files
    resume_path = os.path.join(UPLOAD_FOLDER, resume.filename)
    job_desc_path = os.path.join(JOB_DESC_FOLDER, job_description.filename)
    resume.save(resume_path)
    job_description.save(job_desc_path)
    
    # Extract text based on file type
    if resume.filename.endswith('.pdf'):
        resume_text = extract_text_from_pdf(resume_path)
    else:
        resume_encoding = detect_encoding(resume_path)
        with open(resume_path, 'r', encoding=resume_encoding) as f:
            resume_text = f.read()
    
    if job_description.filename.endswith('.pdf'):
        job_desc_text = extract_text_from_pdf(job_desc_path)
    else:
        job_desc_encoding = detect_encoding(job_desc_path)
        with open(job_desc_path, 'r', encoding=job_desc_encoding) as f:
            job_desc_text = f.read()
    
    # Calculate similarity
    similarity_score = calculate_similarity(resume_text, job_desc_text)
    
    # Determine eligibility
    threshold = 0.4
    if similarity_score >= threshold:
        eligibility = "Qualified for next round"
    else:
        eligibility = "Does not meet requirements"
    
    # Determine category
    if similarity_score >= 0.8:
        category = "Excellent"
    elif similarity_score >= 0.6:
        category = "High"
    elif similarity_score >= 0.3:
        category = "Medium"
    else:
        category = "Low"
    
    return render_template('result.html', 
                         score=similarity_score,
                         category=category,
                         eligibility=eligibility)
if __name__ == '__main__':
    app.run(debug=True)