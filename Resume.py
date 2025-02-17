from flask import Flask, request, send_file
from flask_cors import CORS
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
import glob

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def cleanup_old_resumes():
    """Deletes old resume files to save space."""
    files = glob.glob(os.path.join(UPLOAD_FOLDER, "*.pdf"))
    for file in files:
        os.remove(file)

@app.route("/generate_resume", methods=["POST"])
def generate_resume():
    cleanup_old_resumes()  # Delete old resumes before creating a new one

    # Retrieve form data
    name = request.form.get("name", "No Name")
    job = request.form.get("job", "No Job Title")
    experience = request.form.get("experience", "No Experience")
    education = request.form.get("education", "No Education")
    skills = request.form.get("skills", "No Skills")
    projects = request.form.get("projects", "No Projects")
    certifications = request.form.get("certifications", "No Certifications")
    template = request.form.get("template", "modern")

    # Handle profile picture upload
    profile_pic = request.files.get("profile-pic")
    pic_path = None
    if profile_pic:
        pic_path = os.path.join(UPLOAD_FOLDER, profile_pic.filename)
        profile_pic.save(pic_path)

    # Generate PDF
    pdf_path = f"{UPLOAD_FOLDER}/{name}_Resume.pdf"
    create_pdf(pdf_path, name, job, experience, education, skills, projects, certifications, template, pic_path)

    return send_file(pdf_path, as_attachment=True)

def create_pdf(pdf_path, name, job, experience, education, skills, projects, certifications, template, pic_path):
    """Creates a professional PDF resume."""
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # Add Profile Picture (if available)
    if pic_path:
        img = ImageReader(pic_path)
        c.drawImage(img, 400, height - 150, width=120, height=120)

    # Resume Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, name)
    c.setFont("Helvetica", 14)
    c.drawString(50, height - 75, job)

    # Sections
    sections = [("Experience", experience), ("Education", education), ("Skills", skills),
                ("Projects", projects), ("Certifications", certifications)]

    y_position = height - 120
    c.setFont("Helvetica", 12)

    for title, content in sections:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_position, f"{title}:")
        y_position -= 20
        c.setFont("Helvetica", 12)
        for line in content.split("\n"):
            c.drawString(50, y_position, line)
            y_position -= 15

    c.save()

if __name__ == "__main__":
    app.run(debug=True)
