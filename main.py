import os
import webbrowser
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

from rag.embed_documents import ingest_pdfs
from api.server import app

if __name__ == "__main__":
    print("Ingesting PDFs into ChromaDB...")
    ingest_pdfs()
    
    # Get the absolute path to your dashboard.html file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dashboard_path = os.path.join(current_dir, "frontend", "dashboard.html")
    
    print("Opening dashboard in your web browser...")
    webbrowser.open(f"file:///{dashboard_path.replace(os.sep, '/')}")
        
    print("Starting Flask API Server...")
    # DEBUG MUST BE FALSE so the database doesn't trigger a server restart!
    app.run(port=5000, debug=False)