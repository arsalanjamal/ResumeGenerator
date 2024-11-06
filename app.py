# -*- coding: utf-8 -*-
"""Resume Generator .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1t4p8tdj8wojqHY_TcRBjVgT5QC5JuvqB
"""

# !pip install streamlit transformers fpdf

import streamlit as st
from transformers import pipeline
from fpdf import FPDF

# Load pre-trained resume generation model
pipe = pipeline("text2text-generation", model="nakamoto-yama/t5-resume-generation")

# Function to generate the resume
def generate_resume(name, job_role, education, skills, experience):
    input_text = f"Generate a resume for a {job_role}. The person’s name is {name}, with education in {education}. The person has the following skills: {skills}. The experience includes: {experience}."

    # Use Hugging Face pipeline for text generation
    resume = pipe(input_text)[0]['generated_text']
    return resume

# Function to export the resume to PDF
def export_to_pdf(name, job_role, resume_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Set font
    pdf.set_font("Arial", size=12)

    # Add Title
    pdf.cell(200, 10, txt=f"Resume of {name}", ln=True, align="C")
    pdf.ln(10)  # Line break

    # Add job role
    pdf.cell(200, 10, txt=f"Job Role: {job_role}", ln=True, align="L")
    pdf.ln(10)

    # Add resume content
    pdf.multi_cell(0, 10, txt=resume_text)

    # Save the PDF
    pdf_output = f"{name}_Resume.pdf"
    pdf.output(pdf_output)

    return pdf_output

# Streamlit interface
def main():
    st.title("Resume Generation App")

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
            if st.button("Export to PDF"):
                pdf_output = export_to_pdf(name, job_role, resume_text)
                st.success(f"Resume saved as {pdf_output}")
                st.download_button("Download Resume", pdf_output)
        else:
            st.error("Please fill in all fields to generate a resume.")

if __name__ == "__main__":
    main()