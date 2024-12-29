import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from chain import Chain
from resume import ResumeSkillExtractor 
import logging
     
def create_streamlit_app():
    st.title("🔍 Job Scanner")
    descriptions_input = st.text_area("Enter the Requirements:", value="")
    uploaded_file = st.file_uploader("Upload your resume/document", type=["pdf", "docx", "txt"])
    submit_button = st.button("Submit")
    clear_button=st.button("Clear")
    
    # Use session state to persist data across interactions
    if "missing_skills" not in st.session_state:
        st.session_state.missing_skills = []  # Initialize missing skills
    
    if clear_button:
        try:
           streamlit_js_eval(js_expressions="parent.window.location.reload()")
        except Exception as e:
           st.error(f"An Error Occurred: {e}")
    
    if submit_button: 
        try:   
            description_loader=chain.extract_jobs(descriptions_input) 
            resume_loader=resume.store_resume_skills(uploaded_file)
            missing_skills=chain.find_missing_skills(description_loader, resume_loader)
            st.session_state.missing_skills = missing_skills  # Save missing skills
            ats_score=chain.find_ATS_score(description_loader, resume_loader)
            st.write("ATS Score",ats_score, "%")
            st.write("### Skills Missing from Your Resume:")
        except Exception as e:
           logging.error("An error occurred:", exc_info=e)
           st.error(f"An Error Occurred: {e}")
           
    # Handle skill button clicks
    for i, skill in enumerate(st.session_state.missing_skills):
        if st.button(skill, key=f"clicked_skill_{i}"):  # Use a unique key for this button too
            try:
                st.write(f"### Generated Sentences for the Skill: {skill}")
                sentences = chain.generate_sentences(skill)
                 # Ensure sentences are properly processed
                if isinstance(sentences, str):
                # If sentences are returned as a single string, split them into a list
                   sentences = sentences.strip().split('\n')
                for sentence in sentences:
                    if isinstance(sentence, str):
                      st.markdown(f"{sentence}")
                    else:
                      st.error(f"Unexpected non-string sentence: {sentence}")
            except Exception as e:
                logging.error("An error occurred:", exc_info=e)
                st.error(f"An Error Occurred: {e}")
            
if __name__=='__main__':
    st.set_page_config(layout="wide", page_title="Job Sanner", page_icon="🔍")
    chain=Chain()
    resume=ResumeSkillExtractor()
    create_streamlit_app()
    