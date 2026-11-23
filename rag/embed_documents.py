import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.vector_store import get_vector_store

def ingest_pdfs(directory="data/training_materials"):
    # Smart chunking: explicitly prefers splitting at paragraphs and sentences
    # Added 'r' before the regex separator to fix the SyntaxWarning
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, 
        chunk_overlap=100,
        separators=["\n\n", "\n", r"(?<=\. )", " ", ""]
    )
    vectordb = get_vector_store()
    all_chunks = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            filepath = os.path.join(directory, filename)
            loader = PyPDFLoader(filepath)
            docs = loader.load()
            
            # Smart Metadata Injection
            topic_name = filename.replace(".pdf", "").replace("_", " ")
            for doc in docs:
                doc.metadata["topic"] = topic_name
                doc.metadata["source_file"] = filename
                
            chunks = splitter.split_documents(docs)
            all_chunks.extend(chunks)
            
    # Batch insertion is more efficient for larger datasets
    if all_chunks:
        vectordb.add_documents(all_chunks)