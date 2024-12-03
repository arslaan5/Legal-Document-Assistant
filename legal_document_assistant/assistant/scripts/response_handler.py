from langchain_groq import ChatGroq
from langchain_core.prompts import SystemMessagePromptTemplate, ChatPromptTemplate
from dotenv import load_dotenv
import os
from .data_retriever import retrieve_relevant_chunks
from langchain_core.callbacks import StdOutCallbackHandler


load_dotenv()
groq_api = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    api_key=groq_api,
    model="llama-3.1-8b-instant",
    temperature=0.2,
    callbacks=[StdOutCallbackHandler()]
)

def generate_response(query, relevant_chunks):
    """
    Generate a response to the query using the relevant chunks.
    :param query: The user query.
    :param relevant_chunks: List of relevant chunks of text.
    :return: Generated response as a string.
    """
    print(f"Received query (response_handler.py): {query}")
    # Create a prompt using the relevant chunks

    system_template = SystemMessagePromptTemplate.from_template("""
    # Prompt for Legal Law & Rules Assistant

    ## **Clarity**
    You are a highly skilled and intelligent legal assistant specializing in analyzing and summarizing legal documents.

    ## **Specificity**
    Your task is to provide accurate and concise answers to user queries by retrieving relevant sections from the provided context of legal documents.

    ## **Context Inclusion**
    These documents contain clauses and provisions from various legal fields, such as contracts, property law, and intellectual property. Focus only on the retrieved data to craft your response.

    ## **Instruction Precision**
    Use only the information retrieved from the documents. Do not generate any information that is not directly supported by the text. Try to ignore potential grammatical errors of the user and focus on the content.

    ## **Query Relevance**
    Ensure your response is highly relevant to the user's query by prioritizing the most pertinent sections retrieved.

    ## **Output Format**
    Provide your response in a structured format using markdown language and markdown syntex where needed. Keep the response brief. Also cite relevant sections or clauses where available and required.

    ## **Length Control**
    The lenght of the response should depend on the type of user query, if the user ask for a summary then the response must be elaborative otherwise, if the user asks for an closed ended question then the response must be brief. And the overall response should remain focused and concise.

    ## **Response Tone**
    Maintain a professional and formal tone suitable for legal communication.

    ## **Error Handling**
    If no relevant information is available in the documents, respond with:
    *"No relevant information found in the provided documents."*

    ## **Irrelevant Queries**
    If the query is not related to the provided documents, respond with:
    *"The query is not related to the any legal concerns as per my knowledge base."*

    You are a legal assistant chatbot built by Arslaan Siddiqui.

    ---

    **Context:**
    {context}
    """)

    prompt = ChatPromptTemplate.from_messages([
        system_template,
        ("human", "{query}")
        ]
    )

    context = "\n\n".join([chunk['content'] for chunk in relevant_chunks])
    
    config = {
        'callbacks' : [StdOutCallbackHandler()]
    }

    chain = prompt | llm
    
    # Generate the response
    response = chain.invoke({"query":query, "context":context}, config=config)
    return response.content


if __name__ == "__main__":
    query = "What is the legal procedure for filing a family court case?"
    relevant_chunks = retrieve_relevant_chunks(query)
    result = generate_response(query, relevant_chunks)
    print(result)
