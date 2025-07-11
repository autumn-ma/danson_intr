from pydantic import BaseModel
from typing import Optional
from typing import Optional

class ContentBase(BaseModel):
    topic: str
    title: str
    grade: str
    content: str

class ContentCreate(ContentBase):
    pass

class Content(ContentBase):
    id: int

    class Config:
        orm_mode = True

class AskRequest(BaseModel):
    question: str
    persona: Optional[str] = "friendly"

class AskResponse(BaseModel):
    answer: str

class TopicResponse(BaseModel):
    topics: list[str]

class ContentFilter(BaseModel):
    topic: Optional[str] = None
    title: Optional[str] = None
    grade: Optional[str] = None
    content: Optional[str] = None

class MetricsResponse(BaseModel):
    topics_count: int
    files_uploaded: int
