import streamlit as st
from transformers import pipeline
from fpdf import FPDF
from io import BytesIO
import re

# Load pre-trained model for resume generation
pipe_resume = pipeline("text2text-generation", model="nakamoto-yama/t5-resume-generation")

# Function to generate the resume
def generate_resume(name, job_role, education, skills, experience, job_description):
    # Construct a detailed input prompt for the model
    input_text = f"Generate a detailed, ATS-optimized professional summary for an individual applying for the role of {job_role}. The candidate’s name is {name}. The candidate has {education} and {experience}. The candidate possesses skills in {skills}. The job description includes tasks like {job_description}. Generate a concise and impactful professional summary that highlights the candidate’s experience, accomplishments, and qualifications. Focus on the candidate's personal contributions, not a team-based perspective."
    
    # Use the model to generate the professional summary
    resume = pipe_resume(input_text)[0]['generated_text']
    return resume

# Function to export the resume to PDF with a background color
def export_to_pdf(name, job_role, resume_text, education, skills, experience, phone, email, linkedin, address, background_color="white"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_fill_color(255, 255, 255)  # Default white

    # Set background color based on selection
    if background_color == "light grey":
        pdf.set_fill_color(240, 240, 240)
    elif background_color == "blue":
        pdf.set_fill_color(230, 240, 255)

    pdf.rect(0, 0, 210, 297, 'F')  # Apply background color

    # Set font for the resume
    pdf.set_font("Arial", size=16, style='B')
    
    # Add Title (capitalized)
    pdf.cell(200, 10, txt=name.upper(), ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Job Role: {job_role.upper()}", ln=True, align="C")
    pdf.ln(10)

    # Add Contact Info
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Phone: {phone} | Email: {email} | LinkedIn: {linkedin} | Address: {address}", ln=True, align="C")
    pdf.ln(10)

    # Add Professional Summary Section
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="PROFESSIONAL SUMMARY", ln=True, align="L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=resume_text)
    pdf.ln(10)

    # Add Education Section
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="EDUCATION", ln=True, align="L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=education)
    pdf.ln(10)

    # Add Skills Section
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="SKILLS", ln=True, align="L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"- {skills.replace(',', '\n- ')}")
    pdf.ln(10)

    # Add Experience Section
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="EXPERIENCE", ln=True, align="L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"- {experience.replace(',', '\n- ')}")
    pdf.ln(10)

    # Save the PDF to a BytesIO object
    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest="S").encode("latin1"))
    pdf_output.seek(0)

    return pdf_output

# Streamlit interface
def main():
    st.title("ATS OPTIMIZED RESUME GENERATOR")

    # Collect user information
    st.header("Enter Your Information")
    name = st.text_input("Full Name", key="name")
    
    # Job role selection dropdown
    job_roles = [
        "Software Engineer", "Data Scientist", "Web Developer", "Cybersecurity Analyst", 
        "Database Administrator", "Network Engineer", "UX/UI Designer", "DevOps Engineer", 
        "Machine Learning Engineer", "Cloud Architect", 
        "Physician", "Registered Nurse", "Pharmacist", "Medical Assistant", "Physical Therapist", 
        "Occupational Therapist", "Medical Coder", "Medical Biller", "Radiology Technician", 
        "Healthcare Administrator", 
        "Financial Analyst", "Accountant", "Actuary", "Investment Banker", "Stockbroker", 
        "Underwriter", "Compliance Officer", "Risk Manager", "Auditor", "Financial Advisor", 
        "Production Manager", "Quality Control Inspector", "Manufacturing Engineer", 
        "Industrial Engineer", "Maintenance Technician", "Supply Chain Manager", "Production Line Worker", 
        "Robotics Technician", "Logistics Coordinator", "Quality Assurance Manager", 
        "Teacher", "Professor", "School Counselor", "Principal", "Superintendent", 
        "Special Education Teacher", "Librarian", "Curriculum Developer", "Educational Psychologist", 
        "Early Childhood Educator"
    ]
    job_role = st.selectbox("Job Role", job_roles, key="job_role")
    
    education = st.text_input("Education (e.g., BSc in Computer Science)", key="education")
    skills = st.text_area("Skills (e.g., Python, JavaScript, etc.)", key="skills")
    experience = st.text_area("Experience (e.g., 2 years as Software Developer)", key="experience")
    
    # Add contact details inputs
    phone = st.text_input("Phone Number", key="phone")
    email = st.text_input("Your Email Address", key="email")
    linkedin = st.text_input("LinkedIn Profile", key="linkedin")
    address = st.text_input("Home Address", key="address")
    
    # Add Job Description Input (Optional)
    job_description = st.text_area("Job Description (Optional)", key="job_description")
    
    # Background color selection
    background_color = st.selectbox("Select Resume Background Color", ["white", "light grey", "blue"], key="background_color")

    # Button to generate resume
    if st.button("Generate Resume", key="generate_resume"):
        if name and job_role and education and skills and experience and phone and email and linkedin and address:
            resume_text = generate_resume(name, job_role, education, skills, experience, job_description)

            st.subheader("Generated Resume")
            st.write(resume_text)

            # Export and download PDF
            pdf_output = export_to_pdf(name, job_role, resume_text, education, skills, experience, phone, email, linkedin, address, background_color)
            st.download_button("Download Resume", pdf_output, file_name=f"{name}_Resume.pdf")
        else:
            st.error("Please fill in all fields to generate a resume.")

if __name__ == "__main__":
    main()
