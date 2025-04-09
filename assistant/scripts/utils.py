from .data_retriever import retrieve_relevant_chunks
from markdown import markdown
from django.http import JsonResponse
from langchain_core.callbacks import StdOutCallbackHandler
import uuid
import logging

logger = logging.getLogger(__name__)

def initialize_conversation(session):
    """Initialize conversation history in the session if it doesn't exist."""
    if "conversation" not in session:
        session["conversation"] = []

    if not session.session_key:
        session.save()  # Ensures a session ID is generated


def get_config():
    return { 
        "callbacks": [StdOutCallbackHandler()]
    }


def validate_query(user_query):
    """Validate the user's query."""
    if not user_query or len(user_query.strip()) < 2:
        return False, "Query too short. Please ask a question or provide more context."
    return True, None


def generate_assistant_response(request, user_query, session_id=None):
    """Generate a response using LangChain and relevant chunks from Pinecone."""
    from .response_handler import generate_response
    relevant_chunks = retrieve_relevant_chunks(user_query)
    if not relevant_chunks:
        return "Sorry, I could only answer your legal queries."

    response = generate_response(user_query, relevant_chunks, session_id=session_id)

    # Handle string responses
    if isinstance(response, str):
        response_content = response
    elif hasattr(response, "content"):
        response_content = response.content
    else:
        response_content = str(response)

    return markdown(response_content)


def handle_ajax_request(user_query, response_html):
    """Handle AJAX requests by returning a JSON response."""
    return JsonResponse({
        "user_message": {"role": "user", "content": user_query},
        "assistant_message": {"role": "assistant", "content": response_html},
    })

