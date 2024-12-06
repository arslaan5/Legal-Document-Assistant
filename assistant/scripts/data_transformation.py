from langchain_text_splitters import RecursiveCharacterTextSplitter
from data_ingestion import load_pdf


def get_chunks():
    """Split documents into chunks using RecursiveCharacterTextSplitter."""
    try:
        docs = load_pdf()
        if docs:
            splitter = RecursiveCharacterTextSplitter(
                separators=['\n\n', '\n', ' '], 
                chunk_size=500, 
                chunk_overlap=50
            )
            chunks = splitter.split_documents(docs)
            for chunk in chunks:
                if not hasattr(chunk, 'metadata'):
                    chunk.metadata = {"source": "unknown"}  # Add default metadata if missing
            if not chunks:
                raise ValueError("No chunks generated from the documents.")
            return chunks
        else:
            print("No documents loaded to generate chunks.")
            return None
    except Exception as e:
        print(f"Error in text splitter: {e}")
        return None



if __name__ == "__main__":
    chunks = get_chunks()
    if chunks:
        print(f"Number of chunks generated: {len(chunks)}")
        print(f"First chunk content: {chunks[0].page_content[:100]}")  # First 100 characters of the first chunk
    else:
        print("No chunks generated.")
