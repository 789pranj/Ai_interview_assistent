from langchain_community.document_loaders import PyPDFLoader
import re
from processing.text_to_json import text_to_json

def load_pdf(pdf_path):
    try:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        if not docs:
            return None

        text = " ".join(doc.page_content for doc in docs)
        text = re.sub(r"\s+", " ", text).strip()

        return text_to_json(text, source="pdf")
    except Exception as e:
        print("PDF Error:", e)
        return None
