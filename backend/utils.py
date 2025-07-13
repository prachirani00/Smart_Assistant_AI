import fitz  # PyMuPDF
from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import re
from transformers import pipeline
from PyPDF2 import PdfReader 
from pymongo import MongoClient
from datetime import datetime
import os

# Initialize models
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# -----------------------------
# Document Processing Functions
# -----------------------------

def extract_text_from_file(path):
    try:
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content.strip().replace("\n", " ") + " "
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def summarize_text(text):
    if not text.strip():
        return "No text to summarize."
    
    # Limit input length
    max_input_length = 1024
    input_text = text.strip().replace("\n", " ")
    input_text = input_text[:max_input_length]

    try:
        summary = summarizer(input_text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Summary generation failed: {str(e)}"

def generate_questions(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    questions = []
    for i, sentence in enumerate(sentences[:3]):
        question = f"What does the following sentence mean? '{sentence.strip()}'"
        questions.append(question)
    return questions

def answer_query(question, content):
    sentences = re.split(r'(?<=[.!?]) +', content)
    q_embed = embedder.encode([question])
    s_embed = embedder.encode(sentences)
    sims = cosine_similarity(q_embed, s_embed)[0]
    best_idx = sims.argmax()
    return sentences[best_idx], f"This is based on: '{sentences[best_idx]}'"

def evaluate_answer(question, user_answer, content):
    correct_answer, ref = answer_query(question, content)
    score = cosine_similarity(embedder.encode([user_answer]), embedder.encode([correct_answer]))[0][0]
    return score > 0.6, f"Reference: {ref}"

# -----------------------------
# MongoDB Integration Functions
# -----------------------------



def get_mongo_client():
    uri = "mongodb+srv://PrachiRani00:Priya455@cluster0.qaj8si8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    return MongoClient(uri)


def get_database():
    client = get_mongo_client()
    return client["SmartAssistent"]  # match exactly as shown in your MongoDB

def save_document(filename, content, summary):
    db = get_database()
    db.documents.insert_one({
        "filename": filename,
        "content": content,
        "summary": summary,
        "timestamp": datetime.utcnow()
    })

def get_recent_documents(limit=5):
    db = get_database()
    docs = db.documents.find().sort("timestamp", -1).limit(limit)
    return [{
        "filename": doc["filename"],
        "summary": doc["summary"],
        "timestamp": doc["timestamp"]
    } for doc in docs]
