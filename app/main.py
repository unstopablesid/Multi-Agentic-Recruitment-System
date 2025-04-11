from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.agents.job_summarizer import JobSummarizer
from app.agents.recruiting_agent import RecruitingAgent
from app.agents.interview_scheduler import InterviewScheduler
from app.models.database import JobDescription, Candidate, Interview, engine
from sqlalchemy.orm import sessionmaker

app = FastAPI(title="Multi-Agentic Recruitment System")
SessionLocal = sessionmaker(bind=engine)

# Pydantic models for request/response
class JobDescriptionRequest(BaseModel):
    title: str
    company: str
    description: str
    requirements: str

class CandidateRequest(BaseModel):
    name: str
    email: str
    cv_text: str
    job_id: int

class InterviewRequest(BaseModel):
    candidate_id: int
    job_id: int

# Initialize agents
job_summarizer = JobSummarizer()
recruiting_agent = RecruitingAgent()
interview_scheduler = InterviewScheduler()

@app.post("/jobs/")
async def create_job(job: JobDescriptionRequest):
    db = SessionLocal()
    try:
        # Summarize job description
        summary = job_summarizer.summarize(job.description)
        
        # Create job in database
        db_job = JobDescription(
            title=job.title,
            company=job.company,
            description=job.description,
            requirements=job.requirements,
            summary=summary["summary"]
        )
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job
    finally:
        db.close()

@app.post("/candidates/")
async def process_candidate(candidate: CandidateRequest):
    db = SessionLocal()
    try:
        # Get job description
        job = db.query(JobDescription).filter(JobDescription.id == candidate.job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Analyze match
        match_result = recruiting_agent.analyze_match(job.description, candidate.cv_text)
        
        # Create candidate in database
        db_candidate = Candidate(
            name=candidate.name,
            email=candidate.email,
            cv_text=candidate.cv_text,
            job_id=candidate.job_id,
            match_score=match_result["match_score"],
            status="pending"
        )
        db.add(db_candidate)
        db.commit()
        db.refresh(db_candidate)
        
        return {
            "candidate": db_candidate,
            "match_analysis": match_result["analysis"]
        }
    finally:
        db.close()

@app.post("/interviews/")
async def schedule_interview(interview: InterviewRequest):
    db = SessionLocal()
    try:
        # Get candidate and job
        candidate = db.query(Candidate).filter(Candidate.id == interview.candidate_id).first()
        job = db.query(JobDescription).filter(JobDescription.id == interview.job_id).first()
        
        if not candidate or not job:
            raise HTTPException(status_code=404, detail="Candidate or job not found")
        
        # Generate interview invitation
        invitation = interview_scheduler.generate_invitation_email({
            "name": candidate.name,
            "job_title": job.title,
            "company": job.company
        })
        
        # Create interview in database
        db_interview = Interview(
            candidate_id=interview.candidate_id,
            scheduled_time=f"{invitation['interview_date']} {invitation['interview_time']}",
            status="scheduled"
        )
        db.add(db_interview)
        db.commit()
        db.refresh(db_interview)
        
        return {
            "interview": db_interview,
            "email_content": invitation["email_content"]
        }
    finally:
        db.close()

@app.get("/jobs/{job_id}/candidates")
async def get_job_candidates(job_id: int):
    db = SessionLocal()
    try:
        candidates = db.query(Candidate).filter(Candidate.job_id == job_id).all()
        return candidates
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 