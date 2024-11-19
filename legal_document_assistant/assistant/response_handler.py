from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from data_retriever import retrieve_relevant_chunks
from pprint import pformat


load_dotenv()
groq_api = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    api_key=groq_api,
    model="llama-3.1-8b-instant",
    temperature=0.2
)

def generate_response(query, relevant_chunks):
    """
    Generate a response to the query using the relevant chunks.
    :param query: The user query.
    :param relevant_chunks: List of relevant chunks of text.
    :return: Generated response as a string.
    """
    # Create a prompt using the relevant chunks
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="Use the following context to answer the question:\n{context}\n\nQuestion: {question}"
    )
    
    context = "\n\n".join([chunk['content'] for chunk in relevant_chunks])
    prompt = prompt_template.format(context=context, question=query)
    
    # Generate the response
    response = llm.invoke(prompt)
    return response


if __name__ == "__main__":
    query = "What is the legal procedure for filing a family court case?"
    relevant_chunks = retrieve_relevant_chunks(query, top_k=10)
    result = generate_response(query, relevant_chunks)
    print(result.content)