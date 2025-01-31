
# 🚀 Retrieval-Augmented Generation (RAG) Chatbot

## 📌 Overview
This project implements a **Retrieval-Augmented Generation (RAG) chatbot** using:
- **FAISS** for fast semantic search
- **Hugging Face Transformers** (`Flan-T5`) for text generation
- **Flask API** to serve responses
- **MySQL** to store chat history

The chatbot retrieves relevant text chunks using **vector search**, enhances responses using **an LLM (Flan-T5)**, and exposes endpoints for interaction.

---

## 📥 Installation Guide

### **1️. Clone the Repository**
```bash
git clone <YOUR_GITHUB_REPO_URL>
```

### **Create a Virtual Environment & Install Dependencies**
```
python -m venv rag_env
source rag_env/bin/activate  # On Windows: rag_env\Scripts\activate
pip install -r requirements.txt
```
### **Database Setup (MySQL)**
Start MySQL and run the following commands to set up the database:
```
CREATE DATABASE chatbot_db;
USE chatbot_db;

CREATE TABLE chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role ENUM('user', 'system'),
    content TEXT
);
```
### **Store database credentials in .env file**
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=chatbot_db
```
### **Run Each Notebook in Order**
**Open Jupyter Notebook**
```
jupyter notebook
```
Then open each notebook in order and run all cells.

**Data Preprocessing** (1_dataProcessing.ipynb)
This notebook: ✅ Loads text files
✅ Cleans and chunks them
✅ Saves processed chunks for embedding

**Generate Embeddings & Store in FAISS** (2_Embedding_Vector_Store.ipynb)
 This notebook: ✅ Loads preprocessed text
✅ Generates embeddings using sentence-transformers
✅ Stores embeddings in FAISS vector database

 **Run Retrieval-Augmented Generation** (3_Generation.ipynb)
 This notebook: ✅ Loads FAISS index
✅ Retrieves relevant text chunks
✅ Generates responses using Flan-T5

### **Run the Flask API**
After completing the notebooks, start the Flask API:
```
python app.py
```
This will start the Flask server at:
```
http://127.0.0.1:5000
```

###  **API Endpoints**
The Flask API provides the following endpoints:

1️. /chat **(POST) - Chat with the Bot**
* Purpose: Accepts a user query, retrieves relevant information, and generates a response.
* Request Format: JSON
* Response Format: JSON
   **Test Case in Postman**
1. Open Postman
2. Select POST request
3. Enter the API URL:
```
http://127.0.0.1:5000/chat
```
4. Go to the Body tab → Select raw → Choose JSON
5. Enter this JSON payload:
```
{
    "query": "How is Artificial Intelligence reshaping the workforce?"
}
```
6. Click Send
7. Expected Response:
```
{
    "answer": "Artificial Intelligence is reshaping the workforce by automating repetitive tasks, enhancing decision-making...",
    "retrieved_chunks": [
        "AI is reshaping the workforce by automating repetitive tasks...",
        "Companies are adopting AI to improve productivity..."
    ]
}
```
If you receive this kind of response, the chatbot is working correctly! 

2️. /history **(GET) - Retrieve Chat History**
* Purpose: Fetches stored chat history from MySQL.
* Request Format: No input required.
* Response Format: JSON
   **Test Case in Postman**
1. Open Postman
2. Select GET request
3. Enter the API URL:
```
http://127.0.0.1:5000/history
```
4. Click Send
5. Expected Response:
```
[
    {
        "role": "user",
        "content": "How is AI reshaping the workforce?",
        "timestamp": "2025-01-31 14:20:00"
    },
    {
        "role": "system",
        "content": "AI is reshaping the workforce by automating tasks...",
        "timestamp": "2025-01-31 14:20:05"
    }
]
```
If you receive this response, the chat history is stored correctly in MySQL!
