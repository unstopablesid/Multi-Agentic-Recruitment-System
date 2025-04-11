from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class JobDescription(Base):
    __tablename__ = "job_descriptions"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text)
    
    # Relationships
    candidates = relationship("Candidate", back_populates="job")

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    cv_text = Column(Text, nullable=False)
    job_id = Column(Integer, ForeignKey("job_descriptions.id"))
    match_score = Column(Float)
    status = Column(String(50))  # shortlisted, rejected, pending
    
    # Relationships
    job = relationship("JobDescription", back_populates="candidates")
    interviews = relationship("Interview", back_populates="candidate")

class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    scheduled_time = Column(DateTime)
    status = Column(String(50))  # scheduled, completed, cancelled
    notes = Column(Text)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="interviews")

# Create SQLite database
engine = create_engine("sqlite:///recruitment.db")
Base.metadata.create_all(engine) 