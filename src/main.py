import json
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .utils import decode_metadata_text
from . import crud, models, schemas
from .schemas import ContentFilter
from .database import SessionLocal, engine, get_db
from config.config import settings

from .vector_store import get_vector_store
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from dotenv import load_dotenv

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload-content/", response_class=HTMLResponse)
async def upload_content(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "text/plain":
        raise HTTPException(status_code=400, detail="Invalid file type. Only .txt files are allowed.")
    
    try:
        contents = file.file.read().decode("utf-8")
        decoded = decode_metadata_text(contents)

        content_data = schemas.ContentCreate(
            topic=decoded.get("topic"),
            title=decoded.get("title"),
            grade=decoded.get("grade"),
            content=decoded.get("content"),
        )
        db_content = crud.create_content(db=db, content=content_data)
        vector_store = get_vector_store()
        vector_store.add_texts([db_content.content], metadatas=[{"source": db_content.title}])
        return templates.TemplateResponse("index.html", {"request": request, "response": "success"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")

@app.post("/ask/", response_class=HTMLResponse)
async def ask(
    request: Request,
    question: str = Form(...),
    persona: str  = Form(...),
    db: Session   = Depends(get_db)
):
    retriever = get_vector_store().as_retriever()
    llm = ChatOpenAI(
        model_name="gpt-4.1",
        temperature=0.7,
        openai_api_key=settings.OPENAI_API_KEY,
    )

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", f"You are an educational tutor. Your persona is {persona}. Answer **only** in Markdown, with code fences as needed."),
            (
                "human",
                "Context: {context}\nQuestion: {question}"
            ),
        ]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": chat_prompt},
    )

    result = qa_chain({"query": question})

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "markdown": result["result"]},
    )

@app.get("/topics/", response_class=HTMLResponse)
async def get_topics(
    request: Request,
    topic: str | None = None,
    title: str | None = None,
    grade: str | None = None,
    content: str | None = None,
    db: Session = Depends(get_db)
):
    content_filter = ContentFilter(topic=topic, title=title, grade=grade, content=content)
    topics = crud.get_contents_filtered(db=db, content_filter=content_filter)
    return templates.TemplateResponse("index.html", {"request": request, "response": {"topics": [topic.topic for topic in topics]}})

@app.get("/metrics/", response_class=HTMLResponse)
async def get_metrics(request: Request, db: Session = Depends(get_db)):
    metrics = crud.get_metrics(db=db)
    return templates.TemplateResponse("index.html", {"request": request, "response": metrics})
