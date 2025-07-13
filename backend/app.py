# backend/app.py

import os
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from backend.utils import extract_text_from_file, summarize_text, generate_questions, evaluate_answer, answer_query
from backend.utils import save_document, get_recent_documents

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QARequest(BaseModel):
    question: str
    content: str

class EvalRequest(BaseModel):
    user_answers: List[str]
    questions: List[str]
    content: str

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    temp_path = tempfile.mktemp()
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    content = extract_text_from_file(temp_path)
    summary = summarize_text(content)
    os.remove(temp_path)
    save_document(file.filename, content, summary)
    return {"content": content, "summary": summary}

@app.post("/ask")
async def ask_question(payload: QARequest):
    answer, justification = answer_query(payload.question, payload.content)
    return {"answer": answer, "justification": justification}

@app.post("/challenge")
async def challenge_me(payload: QARequest):
    questions = generate_questions(payload.content)
    return {"questions": questions}

@app.post("/evaluate")
async def evaluate(payload: EvalRequest):
    feedback = []
    for q, ans in zip(payload.questions, payload.user_answers):
        is_correct, explanation = evaluate_answer(q, ans, payload.content)
        feedback.append({
            "question": q,
            "your_answer": ans,
            "correct": bool(is_correct),
            "justification": explanation
        })
    return {"feedback": feedback}
# uvicorn backend.app:app --reload