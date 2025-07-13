
# 🧠 Smart Assistant for Research Summarization

An AI-powered research assistant that allows users to upload PDF documents, automatically summarize the content, ask contextual questions, and challenge themselves with smart MCQs — all integrated with a MongoDB database.

---

## 🚀 Features

- 📄 Upload PDF documents
- ✂️ Automatic text extraction and summarization using BART
- ❓ Contextual question-answering using sentence similarity
- 🧠 Challenge generation (logic-based and reasoning-based)
- 💾 Document storage and history retrieval via MongoDB
- ⚙️ Built using **FastAPI**, **Gradio**, **HuggingFace Transformers**, and **MongoDB Atlas**

---

## 🛠️ Tech Stack

| Technology             | Purpose                          |
|------------------------|----------------------------------|
| FastAPI                | Backend API framework            |
| Gradio                 | Frontend UI for interaction      |
| HuggingFace Transformers | Text summarization and NLP     |
| SentenceTransformers   | Semantic similarity for Q&A      |
| PyMuPDF / PyPDF2       | PDF parsing and text extraction  |
| MongoDB Atlas          | Cloud-based NoSQL database       |

---

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/smart-assistant.git
cd smart-assistant
```

### 2. Create & Activate Virtual Environment (Optional)

```bash
python -m venv venv
# Activate it
source venv/bin/activate     # On Linux/macOS
venv\Scripts\activate      # On Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Configure MongoDB Connection

Create a `.env` file inside the `backend/` directory and paste:

```
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.qaj8si8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

Replace `<PrachiRani00>` and `<Priya455>` with my MongoDB Atlas credentials.

# 5. Run the Backend Server

```bash
cd backend
uvicorn app:app --reload
```

### 6. Run the Frontend (Gradio Interface)

```bash
python frontend.py
```

---

## 🧪 Example Usage

1. Upload a `.pdf` document using the Gradio UI.
2. The assistant:
   - Extracts and summarizes the content
   - Answers your questions
   - Generates challenges to test your understanding
3. The document gets saved to MongoDB for future retrieval.

---

## 🗃️ MongoDB Schema

**Database:** `smart_assistant`  
**Collection:** `documents`

```json
{
  "filename": "example.pdf",
  "content": "Full extracted text...",
  "summary": "Short summarized text...",
  "timestamp": "2025-07-13T10:30:00Z"
}
```

---

## 📂 Folder Structure

```
smart-assistant/
├── backend/
│   ├── app.py
│   ├── utils.py
│   ├── .env
├── frontend.py
├── requirements.txt
├── README.md
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue to discuss what you would like to improve or modify.

---

## 👩‍💻 Author

- **Prachi Rani**
- GitHub: [@PrachiRani00](https://github.com/PrachiRani00)

---
