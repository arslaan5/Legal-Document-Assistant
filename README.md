# LexiAssist (Legal Document Assistant)

Welcome to the Legal Document Assistant, a RAG-based AI chatbot designed to solve users' legal queries efficiently. It is trained on multiple PDFs to provide accurate and relevant answers to legal questions.

## Table of Contents

1. **Project Overview**
2. **Key Features**
3. **Technologies Used**
4. **Architecture**
5. **Installation Instructions**
6. **Usage**
7. **Development Details**
8. **Troubleshooting**
9. **Future Plans**
10. **Licensing**
11. **Deployment**

## 1. Project Overview

The Legal Document Assistant is an AI chatbot built to help users with legal queries. It uses Retrieval-Augmented Generation (RAG) to search through multiple PDFs and find the most relevant information. The application converts user queries into vector embeddings, searches these embeddings in the Pinecone vector database, and processes the retrieved information to provide structured responses via a language model (LLM).

## 2. Key Features

- **Secure authentication system**
- **Lightning-fast speed**
- **Sleek design**
- **Easy to use**
- **Free to use**

## 3. Technologies Used

- **Python 3.12**
- **Django 5.1**
- **Tailwind CSS**
- **Pinecone**
- **langchain**
- **langsmith**
- **Hosted PostgreSQL database**
- **Hugging Face for embedding generation (jina-embeddings-v3)**
- **Groq inference engine (llama-3.1-8b-instant)**

## 4. Architecture

The Legal Document Assistant follows this basic flow:
1. The user enters a query on the frontend.
2. The query is received by the backend and converted into vector embeddings.
3. These embeddings are then searched in the Pinecone vector database using similarity search.
4. The retrieved vector chunks are processed and sent to the LLM for a response.
5. The output from the LLM is structured and returned to the frontend for the user.

## 5. Installation Instructions

1. **Install dependencies:**
   - Ensure you have Python 3.12 and Django 5.1 installed.
   - Install the required packages listed in the `requirements.txt` file.

2. **Set up the required secrets:**
   - Configure the `.env` file with necessary environment variables (e.g., database configurations, API keys).
   
3. **Run the application:**
   - Navigate to the project directory and run `python manage.py runserver` to start the Django development server.

## 6. Usage

- After setting up the environment, simply run the Django development server as mentioned above.
- Users can interact with the application via the web interface by entering their queries.

## 7. Development Details

There are no specific guidelines for contributing to the project, nor are there scripts for automating tasks. The project is pipelined for smooth operation without additional setup.

## 8. Troubleshooting

Common issues include delayed responses due to server issues, complex legal terms, a highly professional or complex response tone, limited information due to the limited amount of PDFs uploaded to the vector database, and other minor issues. Users can contact the support email mentioned on the website for assistance.

## 9. Future Plans

- Integrate Google Auth for easier signups and logins.
- Add more legal and law-related data for better performance.
- Implement design improvements and enhance scalability.

## 10. Licensing

The Legal Document Assistant is released under the Apache 2.0 license.

## 11. Deployment

The application was hosted on AWS Beanstalk.
