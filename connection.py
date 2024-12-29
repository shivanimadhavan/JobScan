from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

def get_groq_connection():
    try:
      api_key = os.getenv("GROQ_API_KEY")
      if not api_key:
            raise ValueError("GROQ_API_KEY is not set in the environment.")
        
      llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-70b-versatile",
        )
    
    except Exception as e:
     raise Exception(f"GroqError: Failed to connect. Details: {e}")
    return llm