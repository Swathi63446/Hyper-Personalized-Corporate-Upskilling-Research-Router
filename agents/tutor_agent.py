from rag.vector_store import get_vector_store

def retrieve_content(missing_skills: str) -> str:
    vectordb = get_vector_store()
    
    # Standard similarity search retrieving the top 5 chunks
    results = vectordb.similarity_search(missing_skills, k=5)
    
    # Format the output clearly with our injected Metadata so the Planner knows exactly where the info came from
    retrieved_text = "\n\n".join([
        f"Source ({doc.metadata.get('topic', 'Unknown')}): {doc.page_content}" 
        for doc in results
    ])
    
    return retrieved_text