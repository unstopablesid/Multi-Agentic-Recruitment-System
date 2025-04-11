from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from datetime import datetime, timedelta
import random

class InterviewScheduler:
    def __init__(self):
        self.llm = Ollama(model="llama2")
        self.email_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an HR professional writing interview invitation emails.
            Write a professional and personalized email inviting the candidate for an interview.
            Include:
            1. A brief mention of their application
            2. The interview date and time
            3. Interview format (e.g., virtual, in-person)
            4. Any preparation materials needed
            5. Contact information for questions
            
            Keep the tone professional but friendly."""),
            ("human", """Candidate Name: {candidate_name}
            Job Title: {job_title}
            Company: {company}
            Interview Date: {interview_date}
            Interview Time: {interview_time}
            Interview Format: {interview_format}""")
        ])
        self.chain = self.email_prompt | self.llm | StrOutputParser()

    def generate_time_slots(self, num_slots: int = 3) -> list:
        """Generate available interview time slots."""
        # This is a simplified version - in production, you might want to
        # integrate with a calendar system
        base_date = datetime.now() + timedelta(days=2)
        slots = []
        for i in range(num_slots):
            slot_date = base_date + timedelta(days=i)
            slot_time = f"{random.randint(9, 16)}:00"  # Random hour between 9 AM and 4 PM
            slots.append({
                "date": slot_date.strftime("%Y-%m-%d"),
                "time": slot_time
            })
        return slots

    def generate_invitation_email(self, candidate_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an interview invitation email."""
        time_slots = self.generate_time_slots()
        selected_slot = time_slots[0]  # In production, let the candidate choose
        
        email_content = self.chain.invoke({
            "candidate_name": candidate_info["name"],
            "job_title": candidate_info["job_title"],
            "company": candidate_info["company"],
            "interview_date": selected_slot["date"],
            "interview_time": selected_slot["time"],
            "interview_format": "Virtual (Zoom)"
        })
        
        return {
            "email_content": email_content,
            "interview_date": selected_slot["date"],
            "interview_time": selected_slot["time"],
            "time_slots": time_slots
        } 