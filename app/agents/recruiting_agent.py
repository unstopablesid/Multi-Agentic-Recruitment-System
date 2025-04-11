from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from app.tools.embedding import OllamaEmbeddings
import numpy as np

class RecruitingAgent:
    def __init__(self):
        self.llm = Ollama(model="llama2")
        self.embeddings = OllamaEmbeddings()
        
        self.matching_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert recruiter. Your task is to analyze a candidate's CV and compare it with a job description.
            Focus on:
            1. Skills match
            2. Experience match
            3. Education match
            4. Overall fit
            
            Provide a detailed analysis and a match score between 0 and 100."""),
            ("human", "Job Description:\n{job_description}\n\nCandidate CV:\n{cv_text}")
        ])
        
        self.chain = self.matching_prompt | self.llm | StrOutputParser()

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts using embeddings."""
        emb1 = self.embeddings.embed_query(text1)
        emb2 = self.embeddings.embed_query(text2)
        return float(np.dot(emb1, emb2))

    def analyze_match(self, job_description: str, cv_text: str) -> Dict[str, Any]:
        """Analyze the match between a CV and job description."""
        # Get semantic similarity score
        similarity_score = self.calculate_similarity(job_description, cv_text)
        
        # Get detailed analysis from LLM
        analysis = self.chain.invoke({
            "job_description": job_description,
            "cv_text": cv_text
        })
        
        # Calculate final match score (combine semantic similarity and LLM analysis)
        # This is a simplified version - in production, you might want to use
        # a more sophisticated scoring system
        match_score = similarity_score * 100
        
        return {
            "match_score": match_score,
            "analysis": analysis,
            "similarity_score": similarity_score
        } 