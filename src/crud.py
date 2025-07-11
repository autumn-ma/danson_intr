from sqlalchemy.orm import Session
from . import models, schemas

def create_content(db: Session, content: schemas.ContentCreate):
    db_content = models.Content(**content.dict())
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

def get_content(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Content).offset(skip).limit(limit).all()

def get_contents_filtered(db: Session, content_filter: schemas.ContentFilter, skip: int = 0, limit: int = 100):
    query = db.query(models.Content)
    if content_filter.topic:
        query = query.filter(models.Content.topic.ilike(f"%{content_filter.topic}%"))
    if content_filter.title:
        query = query.filter(models.Content.title.ilike(f"%{content_filter.title}%"))
    if content_filter.grade:
        query = query.filter(models.Content.grade.ilike(f"%{content_filter.grade}%"))
    if content_filter.content:
        query = query.filter(models.Content.content.ilike(f"%{content_filter.content}%"))
    return query.offset(skip).limit(limit).all()

def get_topics(db: Session, grade: str = None):
    if grade:
        return db.query(models.Content.topic).filter(models.Content.grade == grade).distinct().all()
    return db.query(models.Content.topic).distinct().all()

def get_metrics(db: Session):
    topics_count = db.query(models.Content.topic).distinct().count()
    files_uploaded = db.query(models.Content).count()
    return {"topics_count": topics_count, "files_uploaded": files_uploaded}
