from sentence_transformers import SentenceTransformer

# Load the embedding model
try:
    model = SentenceTransformer("jinaai/jina-embeddings-v3", trust_remote_code=True)
except Exception as e:
    print(f"Error loading the embedding model: {e}")
    model = None


def generate_embedding(text):
    """Generate an embedding for the provided text."""
    try:
        if not model:
            raise RuntimeError("Embedding model is not loaded.")
        if not text or not isinstance(text, str):
            raise ValueError("Invalid text input for embedding generation.")
        result = model.encode(text, show_progress_bar=True)
        return result
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None


if __name__ == "__main__":
    result = generate_embedding("Hello, how are you?")
    if result:
        print(f"Embedding length: {len(result)}")
        print(f"Embedding type: {type(result)}")
        print(result[:10])  # Print the first 10 elements of the embedding
    else:
        print("Embedding generation failed.")
