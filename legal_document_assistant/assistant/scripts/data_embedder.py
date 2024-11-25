from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# Load the embedding model
try:
    model = SentenceTransformer("jinaai/jina-embeddings-v3", revision="c445d96389595a6e93b1b63baa69a116a8b4af68", trust_remote_code=True)
except Exception as e:
    print(f"Error loading the embedding model: {e}")
    model = None


def generate_embedding(text):
    """Generate an embedding for the provided text."""
    try:
        print("Recieved text (data_embedder.py): ", text)
        if not isinstance(text, str):
            raise ValueError("Input must be a string.")
        if not text:
            raise ValueError("Input cannot be None or empty.")
        if text.strip() == "":
            raise ValueError("Input cannot be whitespace only.")
        if len(text) < 10:
            raise ValueError("Input must be at least 10 characters long.")
        
        try:
            result = model.encode(text, show_progress_bar=True)
        except Exception as e:
            raise RuntimeError(f"An error occurred during embedding generation: {e}")
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
