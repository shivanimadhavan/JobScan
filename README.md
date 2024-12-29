Purpose: The application is a Job Scanner that helps users evaluate their resumes against job descriptions to identify missing skills and calculate an ATS (Applicant Tracking System) compatibility score.

User Interaction:
Users input job requirements and upload their resumes.
The app processes the resume to extract skills and other relevant information.
It compares the extracted skills with the job requirements to identify any missing skills.

Backend Process:
Resume Processing: The resume.py file uses a combination of PDF reading and a language model (ChatGroq) to extract a structured list of skills and professional summary details from the uploaded resume.
Skill Matching: The chain.py logic identifies gaps between job requirements and resume content, highlighting missing skills and generating tailored suggestions or sentences for improvement.
ATS Score Calculation: The compatibility between the resume and the job description is quantified as a percentage score.

Interface:
The app is built with Streamlit, providing a simple web-based interface for user interaction.
The missing skills are presented interactively, and users can click to view improvement suggestions.

Deployment:
The application is containerized using Docker for consistent deployment.
