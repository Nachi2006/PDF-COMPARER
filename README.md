# PDF Comparison Chat

A conversational web app to compare and analyze the content of two PDF documents using AI.  
Upload two PDFs, ask a question, and get a comparative answer in a chat-style interface.

---

## 🚀 Features

- **FastAPI backend** for robust file handling and API endpoints
- **Modern chat-style frontend** (dark theme, Roboto font)
- **PDF upload and processing**: Handles two PDFs per session
- **AI-powered question answering**: Uses Llama 3 70B via Groq for comparative analysis
- **No data stored**: PDFs are processed in-memory and deleted after use

---

## 🖥️ Demo

![screenshot](screenshot.png) <!-- Add a screenshot if you have one -->

---

## 📦 Project Structure

.
├── compy.py # FastAPI backend
├── frontend.html # Chat-style web frontend
├── requirements.txt # Python dependencies
├── .env.example # Example environment config (no secrets)
└── README.md # This file

text

---

## ⚡ Quickstart

1. **Clone the repository**
    ```
    git clone https://github.com/yourusername/pdf-comparison-chat.git
    cd pdf-comparison-chat
    ```

2. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```

3. **Set up environment variables**
    - Copy `.env.example` to `.env` and add your [Groq API key](https://console.groq.com/keys):
      ```
      GROQ_API_KEY=your_groq_api_key_here
      ```

4. **Run the app**
    ```
    uvicorn compy:app --reload
    ```

5. **Open in browser**
    - Visit [http://localhost:8000](http://localhost:8000)

---

## 📝 Usage

1. **Upload two PDF documents** using the upload section.
2. **Ask any question** about their similarities, differences, or content.
3. **View the answer** in the chat interface.

---

## 🛠️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) (Python backend)
- [LangChain](https://www.langchain.com/) for PDF parsing and retrieval
- [HuggingFace Embeddings](https://huggingface.co/) for semantic search
- [Groq Llama 3 70B](https://groq.com/) for large language model answers
- Pure HTML/CSS/JS frontend (no frameworks, chat UI)

---

## 📄 Example `.env.example`

GROQ_API_KEY=your_groq_api_key_here

text

---

## 🙈 .gitignore

pycache/
*.pyc
*.env
venv/
.DS_Store

text

---

## 📋 Requirements

See `requirements.txt` for full list.  
Key packages:
- fastapi
- uvicorn
- python-dotenv
- langchain-huggingface
- langchain-community
- langchain-groq

---

## 🤝 Contributing

Pull requests are welcome!  
Please open an issue first to discuss major changes.

---

## 📄 License

MIT License

---

## ✨ Credits

- Inspired by [FastAPI](https://fastapi.tiangolo.com/) and [LangChain](https://www.langchain.com/)
- LLM powered by [Groq](https://groq.com/)

---

> _“Compare, analyze, and converse with your PDFs-instantly.”_

Instructions and structure are based on best practices for open source FastAPI projects
