# 🌍 YatraAI
## AI Travel Copilot powered by RAG
YatraAI is an intelligent travel assistant that helps users discover destinations,
plan trips, analyze travel documents, and understand travel images.
Built using LangChain, Gemini, FAISS, and Chainlit.

# ✨ Features
## 🗺️ 1. Travel Assistance
- Destination recommendations
- Travel questions
- Trip planning
- Food recommendations
- Travel tips
## 📄 2. Document Question Answering
Users can upload:
- PDF
- DOCX
- TXT
and ask questions based on uploaded documents.
## 📚 3. Multiple Document Support
Supports:
- Multiple uploads
- Document comparison
- Summarization
- Information extraction
## 🖼️ 4. Travel Image Understanding
Upload travel images and get:
- Place description
- Tourist information
- Travel suggestions
## 🧠 5. RAG Architecture
Uses Retrieval Augmented Generation:
- FAISS vector database
- Sentence Transformer embeddings
- Gemini LLM

# 🏗️ Architecture
             USER
               │
          Chainlit UI
               │
            app.py
     ┌─────────┼─────────┐
     │         │         │
  Image     Documents    Text
     │         │         │

Gemini Vision FAISS RAG Knowledge Base
└─────────┼─────────┘
Gemini LLM
│
Final Response

# 🛠️ Tech Stack
## Backend
- Python
## AI Framework
- LangChain
## LLM
- Google Gemini
## Vector Database
- FAISS
## Embeddings
- Sentence Transformers
## Interface
- Chainlit



