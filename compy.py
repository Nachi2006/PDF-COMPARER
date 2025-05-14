import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from dotenv import load_dotenv

# Suppress warnings
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["LANGCHAIN_COMMUNITY_NO_PEBBLO"] = "1"

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

class PDFAgent:
    def __init__(self):
        # FIXED: Added missing closing parenthesis for text_splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_stores = {"pdf1": None, "pdf2": None}
        self.retrievers = {"pdf1": None, "pdf2": None}
        self.qa_chain = None

    async def process_pdf(self, file_path: str, pdf_id: str):
        """Process PDF and store with identifier"""
        try:
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            chunks = self.text_splitter.split_documents(pages)
            # FIXED: Added embedding parameter explicitly
            self.vector_stores[pdf_id] = FAISS.from_documents(
                chunks, 
                embedding=self.embeddings
            )
            self.retrievers[pdf_id] = self.vector_stores[pdf_id].as_retriever(search_kwargs={"k": 3})
            if all(self.vector_stores.values()):
                self._init_qa_chain()
            return {"message": f"PDF {pdf_id} processed successfully", "chunks": len(chunks)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

    def _init_qa_chain(self):
        """Initialize QA chain with multi-PDF support"""
        template = """Analyze both documents to answer the question. For comparisons:
        - Identify key similarities/differences
        - Cite source document for each point
        - Provide specific examples from both documents

        Context PDF1: {context1}
        Context PDF2: {context2}

        Question: {question}

        Answer in this format using short paragraphs and key points:
        Analysis 
        Summary
        
        """
        prompt = PromptTemplate.from_template(template)
        
        # FIXED: Properly structured QA chain
        self.qa_chain = (
            RunnableParallel({
                "context1": self.retrievers["pdf1"],
                "context2": self.retrievers["pdf2"],
                "question": RunnablePassthrough()
            })
            | prompt
            | ChatGroq(
                model_name="llama3-70b-8192",
                temperature=0.7,
                api_key=os.getenv("GROQ_API_KEY")
            )
            | StrOutputParser()
        )

    async def ask_question(self, question: str) -> str:
        if not all(self.vector_stores.values()):
            raise HTTPException(status_code=400, detail="Process both PDFs first")
        try:
            return await self.qa_chain.ainvoke(question)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

pdf_agent = PDFAgent()

@app.post("/upload/{pdf_id}")
async def upload_pdf(pdf_id: str, file: UploadFile = File(...)):
    if pdf_id not in ["pdf1", "pdf2"]:
        raise HTTPException(400, "Invalid PDF ID. Use 'pdf1' or 'pdf2'")
    
    temp_file = Path(f"temp_{pdf_id}.pdf")
    try:
        with open(temp_file, "wb") as f:
            content = await file.read()
            f.write(content)
        
        await pdf_agent.process_pdf(str(temp_file), pdf_id)
        return {"message": f"{pdf_id.upper()} uploaded and processed!"}
    except Exception as e:
        raise HTTPException(500, str(e))
    finally:
        if temp_file.exists():
            temp_file.unlink()

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    return {"answer": await pdf_agent.ask_question(request.question)}

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("frontend.html", "r", encoding="utf-8") as f:
        return f.read()
