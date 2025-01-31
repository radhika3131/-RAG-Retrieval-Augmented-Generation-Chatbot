
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
