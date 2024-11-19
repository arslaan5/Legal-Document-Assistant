import os
from langchain_community.document_loaders import PyPDFDirectoryLoader


def load_pdf(path="documents"):
    """Load PDF files from the specified directory."""
    try:
        if os.path.exists(path):
            loader = PyPDFDirectoryLoader(path)
            docs = loader.load()
            if not docs:
                raise ValueError("No documents found in the directory.")
            return docs
        else:
            raise FileNotFoundError("The directory does not exist or wrong path is given.")
    except Exception as e:
        print(f"Error loading PDFs: {e}")
        return None


if __name__ == "__main__":
    doc = load_pdf()
    if doc:
        print(f"Loaded document: {doc[0].page_content[:100]}")  # Print the first 100 characters of the first doc
    else:
        print("No documents loaded.")
