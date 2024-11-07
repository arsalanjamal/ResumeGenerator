import streamlit as st
from transformers import pipeline
from fpdf import FPDF
from io import BytesIO
import re

# Load pre-trained model for resume generation
pipe_resume = pipeline("text2text-generation", model="nakamoto-yama/t5-resume-generation")

# Function to extract keywords from the job description
def extract_keywords(job_description):
    keywords = set(re.findall(r'\b\w+\b', job_description.lower()))
    return keywords

# Function to generate each section of the resume
def generate_resume_sections(name, job_role, education, skills, experience, job_description):
    keywords = extract_keywords(job_description)

    # Generate Professional Summary
    summary_prompt = f"Generate a professional summary for a {job_role} named {name} with skills in {skills}. Focus on relevant keywords: {', '.join(keywords)}."
    summary_text = pipe_resume(summary_prompt)[0]['generated_text']

    # Generate Skills Section
    skills_prompt = f"Generate a list of key skills for a {job_role} with experience in {skills}. Include skills matching the job description keywords: {', '.join(keywords)}."
    skills_text = pipe_resume(skills_prompt)[0]['generated_text']

    # Generate Experience Section
    experience_prompt = f"Generate detailed work experience for a {job_role} with past experience in {experience}. Emphasize accomplishments and responsibilities."
    experience_text = pipe_resume(experience_prompt)[0]['generated_text']

    # Generate Education Section
    education_prompt = f"Generate an education section for someone with a background in {education}."
    education_text = pipe_resume(education_prompt)[0]['generated_text']

    return {
        "summary": summary_text,
        "skills": skills_text,
        "experience": experience_text,
        "education": education_text,
    }

# Function to export the resume to PDF with a background color
def export_to_pdf(name, job_role, sections, phone, email, linkedin, address, background_color="white"):
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

    # Add Professional Summary
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="PROFESSIONAL SUMMARY", ln=True, align="L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=sections["summary"])
    pdf.ln(10)

    # Add Skills Section
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="SKILLS", ln=True, align="L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=sections["skills"])
    pdf.ln(10)

    # Add Experience Section
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="EXPERIENCE", ln=True, align="L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=sections["experience"])
    pdf.ln(10)

    # Add Education Section
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="EDUCATION", ln=True, align="L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=sections["education"])
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
    job_role = st.text_input("Job Role", key="job_role")
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
            # Generate each resume section
            sections = generate_resume_sections(name, job_role, education, skills, experience, job_description)

            st.subheader("Generated Resume")
            for section, content in sections.items():
                st.subheader(section.capitalize())
                st.write(content)

            # Export and download PDF
            pdf_output = export_to_pdf(name, job_role, sections, phone, email, linkedin, address, background_color)
            st.download_button("Download Resume", pdf_output, file_name=f"{name}_Resume.pdf")
        else:
            st.error("Please fill in all fields to generate a resume.")

if __name__ == "__main__":
    main()
