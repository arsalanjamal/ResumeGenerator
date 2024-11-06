import streamlit as st
from transformers import pipeline
from fpdf import FPDF
from io import BytesIO

# Load pre-trained resume generation model
pipe = pipeline("text2text-generation", model="nakamoto-yama/t5-resume-generation")

# Function to generate the resume
def generate_resume(name, job_role, education, skills, experience):
    input_text = f"Generate a professional resume for a {job_role}. The person’s name is {name}, with education in {education}. The person has the following skills: {skills}. The experience includes: {experience}."
    
    # Use Hugging Face pipeline for text generation
    resume = pipe(input_text)[0]['generated_text']
    return resume
import streamlit as st
from transformers import pipeline
from fpdf import FPDF
from io import BytesIO
import re

# Load pre-trained resume generation model
pipe = pipeline("text2text-generation", model="nakamoto-yama/t5-resume-generation")

# Function to extract keywords from the job description
def extract_keywords(job_description):
    # Basic implementation of keyword extraction (can be enhanced with NLP models)
    keywords = set(re.findall(r'\b\w+\b', job_description.lower()))
    return keywords

# Function to generate the resume
def generate_resume(name, job_role, education, skills, experience, job_description):
    # Extract keywords from the job description
    keywords = extract_keywords(job_description)
    
    # Prepare resume content with job description-based keyword focus
    input_text = f"Generate a professional, ATS-optimized resume for a {job_role}. The person’s name is {name}, with education in {education}. The person has the following skills: {skills}. The experience includes: {experience}. Focus on the following keywords from the job description: {', '.join(keywords)}."

    # Use Hugging Face pipeline for text generation
    resume = pipe(input_text)[0]['generated_text']
    return resume

# Function to export the resume to a professional PDF
def export_to_pdf(name, job_role, resume_text, education, skills, experience):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Set font for the resume
    pdf.set_font("Arial", size=16, style='B')
    
    # Add Name and Job Title (Header)
    pdf.cell(200, 10, txt=name, ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Job Role: {job_role}", ln=True, align="C")
    pdf.ln(10)
    
    # Add Professional Summary
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Professional Summary", ln=True, align="L")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=resume_text)
    pdf.ln(10)
    
    # Add Education Section
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Education", ln=True, align="L")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=education)
    pdf.ln(10)

    # Add Skills Section (ATS optimized)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Skills", ln=True, align="L")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"- {skills.replace(',', '\n- ')}")
    pdf.ln(10)

    # Add Experience Section (ATS optimized)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Experience", ln=True, align="L")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"- {experience.replace(',', '\n- ')}")
    pdf.ln(10)
    
    # Save the PDF to a BytesIO object
    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest="S").encode("latin1"))  # Output as string, then write to BytesIO
    pdf_output.seek(0)  # Move to the beginning of the BytesIO object for download

    return pdf_output

# Streamlit interface
def main():
    st.title("ATS Optimized Resume Generator")

    # Collect user information
    st.header("Enter Your Information")
    name = st.text_input("Full Name")
    job_role = st.text_input("Job Role")
    education = st.text_input("Education (e.g., BSc in Computer Science)")
    skills = st.text_area("Skills (e.g., Python, JavaScript, etc.)")
    experience = st.text_area("Experience (e.g., 2 years as Software Developer)")
    
    # Add Job Description Input
    job_description = st.text_area("Job Description (Optional)")

    # Button to generate resume
    if st.button("Generate Resume"):
        if name and job_role and education and skills and experience:
            # Generate the resume text
            resume_text = generate_resume(name, job_role, education, skills, experience, job_description)

            # Display generated resume
            st.subheader("Generated Resume")
            st.write(resume_text)

            # Export option
            pdf_output = export_to_pdf(name, job_role, resume_text, education, skills, experience)
            st.download_button("Download Resume", pdf_output, file_name=f"{name}_Resume.pdf")
        else:
            st.error("Please fill in all fields to generate a resume.")

if __name__ == "__main__":
    main()

# Function to export the resume to a professional PDF
def export_to_pdf(name, job_role, resume_text, education, skills, experience):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Set font for the resume
    pdf.set_font("Arial", size=16, style='B')
    
    # Add Name and Job Title (Header)
    pdf.cell(200, 10, txt=name, ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Job Role: {job_role}", ln=True, align="C")
    pdf.ln(10)
    
    # Add Professional Summary
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Professional Summary", ln=True, align="L")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=resume_text)
    pdf.ln(10)
    
    # Add Education Section
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Education", ln=True, align="L")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=education)
    pdf.ln(10)

    # Add Skills Section
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Skills", ln=True, align="L")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"- {skills.replace(',', '\n- ')}")
    pdf.ln(10)

    # Add Experience Section
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Experience", ln=True, align="L")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"- {experience.replace(',', '\n- ')}")
    pdf.ln(10)
    
    # Save the PDF to a BytesIO object
    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest="S").encode("latin1"))  # Output as string, then write to BytesIO
    pdf_output.seek(0)  # Move to the beginning of the BytesIO object for download

    return pdf_output

# Streamlit interface
def main():
    st.title("Professional Resume Generation App")

    # Collect user information
    st.header("Enter Your Information")
    name = st.text_input("Full Name")
    job_role = st.text_input("Job Role")
    education = st.text_input("Education (e.g., BSc in Computer Science)")
    skills = st.text_area("Skills (e.g., Python, JavaScript, etc.)")
    experience = st.text_area("Experience (e.g., 2 years as Software Developer)")

    # Button to generate resume
    if st.button("Generate Resume"):
        if name and job_role and education and skills and experience:
            # Generate the resume text
            resume_text = generate_resume(name, job_role, education, skills, experience)

            # Display generated resume
            st.subheader("Generated Resume")
            st.write(resume_text)

            # Export option
            pdf_output = export_to_pdf(name, job_role, resume_text, education, skills, experience)
            st.download_button("Download Resume", pdf_output, file_name=f"{name}_Resume.pdf")
        else:
            st.error("Please fill in all fields to generate a resume.")

if __name__ == "__main__":
    main()
