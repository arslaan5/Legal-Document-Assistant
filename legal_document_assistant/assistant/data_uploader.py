from pinecone import Pinecone
from data_transformation import get_chunks
from data_embedder import generate_embedding
from dotenv import load_dotenv
import os
from uuid import uuid4
import time


load_dotenv()
pinecone_api = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=pinecone_api)
index = pc.Index("legal-documents-embeddings")

def upload_embeddings():
    # Get chunks from the documents
    chunks = get_chunks()
    if not chunks:
        print("No chunks found. Ensure PDFs are loaded correctly.")
        return

    for chunk in chunks:
        # Extract text and metadata
        text = chunk.page_content
        metadata = chunk.metadata if hasattr(chunk, 'metadata') else {}

        if text and isinstance(text, str):
            embedding = generate_embedding(text)
            if embedding is not None:
                # Upload embedding with metadata
                try:
                    index.upsert([(str(uuid4()), embedding, metadata)], batch_size=10)
                except Exception as e:
                    print(f"Failed to upload embedding to Pinecone: {e}")
            else:
                print(f"Failed to generate embedding for chunk: {text[:50]}...")
        else:
            print(f"Invalid chunk content: {chunk}")
    print("Finished uploading embeddings and metadata.")


if __name__ == "__main__":
    print("Deleting existing index...")
    index.delete(delete_all=True)
    print("Starting upload...")
    start_time = time.process_time()
    upload_embeddings()
    end_time = time.process_time()
    print(f"Upload completed in {end_time - start_time:.4f} seconds.")