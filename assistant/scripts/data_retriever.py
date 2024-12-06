from pinecone import Pinecone
from .data_embedder import generate_embedding
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
pinecone_api = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone client and index
pc = Pinecone(api_key=pinecone_api)
index = pc.Index("legal-documents-embeddings")


def retrieve_relevant_chunks(query, top_k=8):
    """
    Retrieve relevant chunks from Pinecone based on a user query.
    :param query: User's query as a string.
    :param top_k: Number of top results to retrieve.
    :return: List of relevant chunks with metadata.
    """
    try:
        print(f"Received query (data_retriever.py): {repr(query)}")  # Debug log
        # Generate embedding for the query
        if len(query) < 10:
            return []
        query_embedding = generate_embedding(query)
        if query_embedding is None:
            raise ValueError("Failed to generate embedding for the query.")

        # Convert the embedding from ndarray to a list of floats
        query_embedding = query_embedding.tolist()
        
        # Query Pinecone for relevant vectors
        result = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )

        # Extract and return results
        relevant_chunks = []
        for match in result['matches']:
            metadata = match['metadata']
            score = match['score']
            relevant_chunks.append({
                "content": metadata.get("content", "Content unavailable"),
                "source": metadata.get("source", "Unknown source"),
                "score": score
            })

        return relevant_chunks

    except Exception as e:
        print(f"Error retrieving relevant chunks: {e}")
        return []


if __name__ == "__main__":
    # Example query
    query = "What is the legal procedure for filing a family court case?"
    results = retrieve_relevant_chunks(query)
    if results:
        print("Relevant Chunks:")
        for i, chunk in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"Content: {chunk['content'][:200]}...")  # Show the first 200 characters
            print(f"Source: {chunk['source']}")
            print(f"Relevance Score: {chunk['score']}")
    else:
        print("No relevant chunks found.")
