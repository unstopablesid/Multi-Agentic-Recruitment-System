from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser

class JobSummarizer:
    def __init__(self):
        self.llm = Ollama(model="llama2")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert job description analyzer. Your task is to extract and summarize key information from job descriptions.
            Focus on:
            1. Required skills and qualifications
            2. Years of experience needed
            3. Key responsibilities
            4. Education requirements
            5. Any specific certifications or licenses needed
            
            Format your response in a clear, structured way."""),
            ("human", "{job_description}")
        ])
        self.chain = self.prompt | self.llm | StrOutputParser()

    def summarize(self, job_description: str) -> Dict[str, Any]:
        """Summarize a job description and extract key requirements."""
        summary = self.chain.invoke({"job_description": job_description})
        
        # Parse the summary into structured data
        # This is a simplified version - in production, you might want to use
        # a more sophisticated parsing approach
        return {
            "summary": summary,
            "raw_text": job_description
        } 