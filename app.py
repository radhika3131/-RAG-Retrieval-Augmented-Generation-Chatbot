from flask import Flask, request, jsonify
import mysql.connector
import faiss
import pickle
from datetime import datetime
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from dotenv import load_dotenv
import os

app = Flask(__name__)

#  Load FAISS index and text chunks
index = faiss.read_index("faiss_index.idx")
with open("retrieved_text_chunks.pkl", "rb") as file:
    text_chunks = pickle.load(file)

#  Load Embedding Model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

#  Load Local LLM Model
generator = pipeline("text2text-generation", model="google/flan-t5-large")





# Load environment variables
load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor()


def retrieve_top_k(query, k=7):  # Increase k from 5 to 7
    """Retrieve top-k relevant text chunks from FAISS"""
    query_embedding = embedder.encode([query])
    distances, indices = index.search(query_embedding, k)
    return [text_chunks[i] for i in indices[0]]



def generate_response_local(query):
    """Generate AI response using retrieved context and local model"""
    retrieved_texts = retrieve_top_k(query, k=5)  # Retrieve more context
    context = "\n\n".join(retrieved_texts)  # Better readability

    # 🔹 Debugging Output: Print retrieved chunks before using them in the LLM
    print("\n🔹 Retrieved Context for Debugging:\n", context)

    prompt = f"""
You are an expert AI assistant. Answer the question based ONLY on the given context.

Context:
{context}

User Question: {query}

Provide a structured, detailed, and coherent response. Make sure the answer is complete and does NOT repeat phrases:
"""

    response = generator(prompt, max_new_tokens=150, num_return_sequences=1)

    return response[0]["generated_text"], retrieved_texts




def save_chat(role, content):
    """Save chat message to MySQL"""
    cursor.execute("INSERT INTO chat_history (role, content) VALUES (%s, %s)", (role, content))
    db.commit()


@app.route('/chat', methods=['POST'])
def chat():
    """POST endpoint to handle chat"""
    data = request.json
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    # Save user query
    save_chat("user", query)

    # Generate response
    answer, retrieved_texts = generate_response_local(query)

    # Save chatbot response
    save_chat("system", answer)

    return jsonify({
        "answer": answer,
        "retrieved_chunks": retrieved_texts  # Optional: Debugging info
    })


@app.route('/history', methods=['GET'])
def history():
    """GET endpoint to retrieve chat history"""
    cursor.execute("SELECT role, content, timestamp FROM chat_history ORDER BY timestamp DESC")
    chats = cursor.fetchall()

    return jsonify([
        {"role": row[0], "content": row[1], "timestamp": row[2].strftime("%Y-%m-%d %H:%M:%S")}
        for row in chats
    ])


if __name__ == '__main__':
    app.run(debug=True)
