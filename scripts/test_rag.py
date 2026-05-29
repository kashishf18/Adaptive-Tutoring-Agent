import sys
import os
import io

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag import extract_text, add_documents_to_db, query_documents, clear_db

def test_rag_pipeline():
    print("Testing RAG Pipeline...")
    
    # 1. Clear existing DB
    clear_db()
    print("DB cleared")
    
    # 2. Extract text (mock file object)
    mock_txt = io.BytesIO(b"Gravity is a fundamental interaction which causes mutual attraction between all things that have mass. The equation is F = G(m1m2)/r^2.")
    text = extract_text(mock_txt, "gravity_notes.txt")
    assert "Gravity is a fundamental" in text
    print("Text extraction passed")
    
    # 3. Add to DB
    chunks_added = add_documents_to_db(text, "gravity_notes.txt")
    assert chunks_added > 0
    print(f"Added {chunks_added} chunks to DB")
    
    # 4. Query DB
    query = "What is the equation for gravity?"
    context = query_documents(query)
    assert "F = G(m1m2)/r^2" in context
    print("Query returned correct context")
    
    print("\nRAG Integration Tests Passed!")

if __name__ == "__main__":
    test_rag_pipeline()
