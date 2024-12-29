import PyPDF2
import json
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

class ResumeSkillExtractor:
    def __init__(self):
        self.llm=ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-70b-versatile",
        )
        
    def extract_pdf_text(self,pdf_file):
        text = ""
        try:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None
        
    def extract_summary_and_skills(self, text):
        prompt = f"""
        Your task is to extract all relevant information mentioned only in the *PROFESSIONAL SUMMARY* and *SKILLS* sections, including:
         - Both **technical and non-technical skills** mentioned in the text.
         - **Fields of study**, academic disciplines, or areas of expertise.
         - For any skills containing additional descriptors or phrases (e.g., "Python programming language"), extract only the core skill ("Python") and list it separately.
         - For any skills containing additional descriptors or phrases (e.g., SQL (MS-SQL, MySQL)), extract the core skill ("SQL", "MS-SQL", "MySQL") and list it separately.
         - Include everything as a unified list.

        ### INSTRUCTIONS:
        1. Normalize all skills and areas of study to a consistent format (e.g., lowercase, no additional descriptions).
        2. Provide the output in JSON format with the key `"skills"` as a list. including the exact phrases as they appear in the text.

         ### VALID JSON (NO PREAMBLE):

        Text:
        {text}
        """
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"Error extracting content with LLM: {e}")
            return None
        
    def store_resume_skills(self,uploaded_file):
        """
        Parse the resume PDF, extract the text, and store the skills into ChromaDB.
        """
        try:
            # Extract text from the resume PDF
            resume_text = self.extract_pdf_text(uploaded_file)
            if not resume_text:
                raise ValueError("No text extracted from the resume PDF.")
            
            #Extracting Professional Summary and Skills using LLM
            extracted_content = self.extract_summary_and_skills(resume_text)

            if not extracted_content:
                raise ValueError("Failed to extract content using LLM.")
            
            cleaned_content = extracted_content.strip("```json").strip("```").strip()            
            
            try:
               extracted_data = json.loads(cleaned_content)
            except json.JSONDecodeError as e:
              raise ValueError(f"Failed to parse LLM response as JSON. Error: {e}")
            return extracted_data if isinstance(extracted_data, list) else [extracted_data]
        
        except Exception as e:
            print(f"An error occurred: {e}")

