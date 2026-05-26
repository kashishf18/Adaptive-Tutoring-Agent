import os
import PyPDF2
import chromadb
from chromadb.utils import embedding_functions

DB_PATH = os.path.join(os.getcwd(), "data", "vector_db")
COLLECTION_NAME = "knowledge_base"

# Using the default sentence-transformers model that chromadb ships with
# all-MiniLM-L6-v2 is lightweight and works well locally.
default_ef = embedding_functions.DefaultEmbeddingFunction()

def get_chroma_client():
    os.makedirs(DB_PATH, exist_ok=True)
    return chromadb.PersistentClient(path=DB_PATH)

def get_chroma_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=default_ef)

def extract_text(file_obj, filename: str) -> str:
    """Extract text from a file-like object."""
    text = ""
    if filename.lower().endswith(".pdf"):
        reader = PyPDF2.PdfReader(file_obj)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    elif filename.lower().endswith(".txt"):
        text = file_obj.read().decode("utf-8")
    return text

def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list:
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - chunk_overlap
    return chunks

def add_documents_to_db(text: str, source_name: str) -> int:
    """Process text, chunk it, and add to ChromaDB."""
    if not text.strip():
        return 0
        
    collection = get_chroma_collection()
    chunks = chunk_text(text)
    
    # Generate unique IDs for the chunks
    # Simple hash or count based on source
    existing_count = collection.count()
    ids = [f"{source_name}_chunk_{existing_count + i}" for i in range(len(chunks))]
    metadatas = [{"source": source_name} for _ in chunks]
    
    collection.add(
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )
    return len(chunks)

def query_documents(query: str, n_results: int = 3) -> str:
    """Query ChromaDB and return a single concatenated context string."""
    collection = get_chroma_collection()
    if collection.count() == 0:
        return ""
        
    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count())
    )
    
    if results and "documents" in results and results["documents"]:
        # results["documents"] is a list of lists of documents
        docs = results["documents"][0]
        context = "\n\n---\n\n".join(docs)
        return context
    return ""

def clear_db():
    """Wipe the collection."""
    client = get_chroma_client()
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass # Collection might not exist
