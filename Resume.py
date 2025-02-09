from flask import Flask, request, send_file
from flask_cors import CORS
from fpdf import FPDF
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# Ensure profile pictures directory exists
if not os.path.exists("profile_pictures"):
    os.makedirs("profile_pictures")


def create_pdf(data, image_path=None):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, "Resume", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)

    for key, value in data.items():
        pdf.cell(200, 10, f"{key}: {value}", ln=True, align="L")
        pdf.ln(5)

    if image_path:
        pdf.image(image_path, x=10, y=pdf.get_y(), w=30)

    pdf_file = "generated_resume.pdf"
    pdf.output(pdf_file)
    return pdf_file


@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    # Retrieve form data
    data = {
        "Full Name": request.form.get("name"),
        "Job Title": request.form.get("job"),
        "Experience": request.form.get("experience"),
        "Education": request.form.get("education"),
        "Skills": request.form.get("skills"),
        "Projects": request.form.get("projects"),
        "Certifications": request.form.get("certifications"),
    }

    profile_pic = request.files.get("profile-pic")
    pic_path = None
    if profile_pic:
        pic_path = os.path.join("profile_pictures", profile_pic.filename)
        profile_pic.save(pic_path)

    # Generate the PDF
    resume_path = create_pdf(data, pic_path)

    if not os.path.exists(resume_path):
        return "Resume PDF was not created", 500

    return send_file(resume_path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
