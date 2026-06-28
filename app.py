import os
import warnings
from contextlib import asynccontextmanager

# Silenciar advertencias de librerías obsoletas y metadatos internos de PDFs
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Importaciones de LangChain adaptadas a las versiones modernas
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings  # Versión actualizada y recomendada
import requests

# Configuración de Rutas y Constantes
DOCS_DIR = "documentos"
DB_DIR = "chroma_db"
OLLAMA_API_URL = "http://localhost:11434/api/generate"
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3:8b"  # Cambia por el modelo local que uses (ej: llama3, mistral, etc.)

# Variables globales para persistir el RAG en memoria activa
vector_store = None
retriever = None

# 1. Configuración del Ciclo de Vida (Lifespan) reemplazando los viejos eventos "on_event"
@asynccontextmanager
async def lifespan(app: FastAPI):
    global vector_store, retriever
    print("\n🧠 [StarMind RAG] Iniciando sistema de extracción documental...")
    
    # Crear carpeta de documentos si no existe
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
        print(f"📁 Se creó la carpeta '{DOCS_DIR}'. Agrega tus archivos .pdf allí.")
        
    try:
        print("🤖 Cargando base de datos del RAG y vectorizando documentos...")
        embeddings = OllamaEmbeddings(model=EMBED_MODEL)
        
        # Cargar PDFs desde la carpeta local
        loader = PyPDFDirectoryLoader(DOCS_DIR)
        documents = loader.load()
        
        if documents:
            # Segmentar el texto en fragmentos óptimos para el contexto
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(documents)
            
            # Inicializar e indexar en la base de datos vectorial Chroma
            vector_store = Chroma.from_documents(chunks, embeddings, persist_directory=DB_DIR)
            retriever = vector_store.as_retriever(search_kwargs={"k": 4})
            print(f"✅ Repositorio RAG listo de forma local ({len(documents)} PDFs indexados con éxito).")
        else:
            print("⚠️ No se encontraron archivos .pdf dentro de la carpeta 'documentos/'.")
            # Inicializar un vector store vacío o persistido para evitar excepciones
            vector_store = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
            retriever = vector_store.as_retriever(search_kwargs={"k": 4})
            
    except Exception as e:
        print(f"❌ Error crítico durante la inicialización del RAG: {e}")
        print("💡 Asegúrate de tener Ollama corriendo y el modelo de embeddings instalado (`ollama run nomic-embed-text`).")

    yield
    print("🛑 [StarMind RAG] Apagando el ecosistema local de forma segura.\n")

# Inicialización de FastAPI con el nuevo manejador de ciclo de vida
app = FastAPI(title="StarMind RAG Backend", lifespan=lifespan)

# Configuración de CORS para comunicarse sin restricciones con el index.html
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estructuras de datos de Pydantic para validar peticiones del Frontend
class QueryRequest(BaseModel):
    query: str

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage]

# Endpoint para el Estado del Sistema del Banner Superior
@app.get("/api/system-status")
async def get_system_status():
    return {
        "weather": "Base de datos local sincronizada y lista.",
        "tip": "StarMind extrae conocimientos directamente de tus documentos locales cifrados."
    }

# Endpoint Principal de Búsqueda RAG Avanzada (Tarjetas de Análisis)
@app.post("/api/search")
async def search_rag(payload: QueryRequest):
    global retriever
    if not retriever:
        raise HTTPException(status_code=503, detail="El motor RAG no está inicializado o no hay documentos.")
        
    query = payload.query
    try:
        # Recuperar fragmentos de documentos relevantes
        relevant_docs = retriever.invoke(query)
        
        context_text = ""
        sources = []
        
        for idx, doc in enumerate(relevant_docs):
            source_name = doc.metadata.get("source", f"Documento_{idx+1}").split(os.sep)[-1]
            page_num = doc.metadata.get("page", 0) + 1
            snippet = doc.page_content
            
            context_text += f"\n--- [Fuente: {source_name} (Pág. {page_num})] ---\n{snippet}\n"
            
            # Formatear la fuente para que el mapa conceptual del frontend la pinte con diseño de tarjeta
            sources.append({
                "title": f"{source_name}",
                "snippet": snippet[:180] + "...",
                "priority": 95 - (idx * 10),  # Prioridad simulada según el orden de relevancia
                "hint": f"Página {page_num}",
                "thumbnail": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=120&auto=format&fit=crop" # Fondo abstracto estético
            })
            
        # Construir el Prompt del Sistema RAG
        prompt = (
            f"Eres StarMind, un analizador documental de nivel experto de inteligencia artificial.\n"
            f"Utiliza ÚNICAMENTE los siguientes fragmentos de contexto recuperados para responder de forma profunda, analítica y técnica al usuario.\n"
            f"Si el contexto no contiene la información para responder la duda, indícalo de forma elegante.\n\n"
            f"CONTEXTO RECUPERADO:\n{context_text}\n\n"
            f"PREGUNTA DEL USUARIO: {query}\n\n"
            f"RESPUESTA EXTRACTIVA Y EXPLICATIVA:"
        )
        
        # Llamar al modelo de Ollama
        response = requests.post(OLLAMA_API_URL, json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False
        })
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error en la respuesta del modelo Ollama.")
            
        answer_text = response.json().get("response", "No se pudo generar un análisis.")
        
        return {
            "answer": answer_text,
            "sources": sources
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para el Chat Inteligente Conversacional Alternativo
@app.post("/api/chat")
async def chat_interaction(payload: ChatRequest):
    try:
        # Reconstruir el hilo histórico para mantener la memoria conversacional local
        conversation_context = "Eres StarMind, el módulo conversacional inteligente de la plataforma. Responde de forma concisa, útil y futurista.\n\n"
        for msg in payload.history:
            speaker = "Usuario" if msg.role == "user" else "StarMind"
            conversation_context += f"{speaker}: {msg.content}\n"
            
        conversation_context += f"Usuario: {payload.message}\nStarMind:"
        
        response = requests.post(OLLAMA_API_URL, json={
            "model": LLM_MODEL,
            "prompt": conversation_context,
            "stream": False
        })
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error de procesamiento en Ollama Chat.")
            
        reply = response.json().get("response", "Disculpa, tengo problemas para procesar esa idea.")
        return {"reply": reply}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.py:app", host="127.0.0.1", port=8001, reload=True)
