from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import re

load_dotenv()

def load_pdf(pdf_path):
    try:
        loader = PyPDFLoader(pdf_path)  
        documents = loader.load()

        if not documents:
            return None

        text = " ".join(doc.page_content for doc in documents)
        text = re.sub(r"\s+", " ", text).strip()

        return text

    except Exception:
        return None
