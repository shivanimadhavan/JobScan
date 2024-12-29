from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from connection import get_groq_connection

class Chain:
    def __init__(self):
        self.llm = get_groq_connection()
    
    def extract_jobs(self, pagedata):
        prompt_extract = f"""
            ### Job description:
            {pagedata}
    
            ### INSTRUCTION:
          Your task is to:

         1. Identify and extract all the skills mentioned in the provided text, including both technical skills (e.g., programming languages, tools, domain-specific expertise) and non-technical skills (e.g., communication, problem-solving).
         2. Ignore locations, or any other irrelevant details.
         3. For any skills containing additional descriptors or phrases (e.g., "Python programming language"), extract only the core skill ("Python") and list it separately.
         4. Provide the output in JSON format under a single key called "skills" as a list, including the exact phrases as they appear in the text.
    
            ### VALID JSON (NO PREAMBLE):
            """
        res=self.llm .invoke(prompt_extract)

        try:
            json_parser = JsonOutputParser()
            json_res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return json_res if isinstance(json_res, list) else [json_res]
    
    def find_missing_skills(self, job_skills, resume_skills):
       # Extract and lowercase skills for case-insensitive comparison
       job_skills = set(skill.lower().strip() for skill in job_skills[0].get("skills", []) if isinstance(job_skills, list) and job_skills)
       resume_skills = set(skill.lower().strip() for skill in resume_skills[0].get("skills", []) if isinstance(resume_skills, list) and resume_skills)

       missing_skills = [x for x in job_skills if x not in resume_skills] #job_skills - resume_skills
       return list(missing_skills)
    
    def find_ATS_score(self, job_skills, resume_skills):         
        job_skills = set(skill.lower().strip() for skill in job_skills[0].get("skills", []) if isinstance(job_skills, list) and job_skills)
        resume_skills = set(skill.lower().strip() for skill in resume_skills[0].get("skills", []) if isinstance(resume_skills, list) and resume_skills)
       
        matches = sum(1 for skill in job_skills if skill in resume_skills)
        # Calculate percentage
        ats_score = (matches / len(job_skills)) * 100 if job_skills else 0
        return round(ats_score, 2)
    
    def generate_sentences(self, skill):
        prompt_extract = f"""
            ### Job description:
            Skill: {skill}
    
            ### INSTRUCTION:
          Your task is to generate 3 valid and professional sentences that describe the experience or proficiency with the given skill. 

          Instructions:
          1. Ensure the sentences are relevant for a professional resume.
          2. Each sentence should highlight different aspects, such as:
            - Experience using the skill in a project or job.
            - Proficiency or expertise in the skill.
            - The impact of the skill on work or outcomes.
          3. Use action verbs and concise language.

           Output:    
            ### Provide 3 sentences in a bulleted format. Do not include preambles or explanations.
            """
        res=self.llm.invoke(prompt_extract)
        return res.content
        
