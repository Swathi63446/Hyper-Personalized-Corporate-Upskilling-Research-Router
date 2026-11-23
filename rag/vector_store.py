from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def get_vector_store():
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma(persist_directory="./chroma_db", embedding_function=embedding_model)