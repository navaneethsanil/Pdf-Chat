# PDF Chat System using LangChain

This repository contains a project to build a PDF chat system that enables users to interact with PDF documents. By leveraging a Retrieval-Augmented Generation (RAG) pipeline, users can ask questions related to the content of a document, and the system retrieves relevant information to respond intelligently. 

Key components of this project:
- **LangChain** as the framework to manage the RAG pipeline.
- **Pinecone** for vector database management.
- **Mistral large latest model** as the language model (LLM) for generating answers.
- **all-mpnet-base-v2** as the embedding model for document and query embeddings.
- **LangChain Hub** for retrieval QA chat prompts.
- **Streamlit** for the frontend application.

## Table of Contents

- [Features](#features)
- [Installation](#installation)

## Features

- Upload and process PDFs for conversational question-answering.
- Retrieval-Augmented Generation (RAG) using LangChain.
- Embedding-based similarity search using Pinecone.
- Integration with Mistral's LLM for high-quality responses.
- Customizable prompts from LangChain Hub.
- User-friendly interface with **Streamlit**.

## Installation

### Prerequisites

- Python 3.8 or higher
- [Pinecone](https://www.pinecone.io/) account for vector database storage
- [MISTRAL AI](https://mistral.ai/) account for LLM model
- [Streamlit](https://streamlit.io/) for the frontend interface

### Install Dependencies

1. Clone this repository:

   ```bash
   git clone https://github.com/navaneethsanil/Pdf-Chat.git
   cd Pdf-Chat
   python -m venv env
   source env/scripts/activate
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file to store API keys and configuration settings:

   ```bash
   PINECONE_API_KEY=your_pinecone_api_key
   MISTRAL_API_KEY=your_mistral_api_key
   LANGSMITH_API_KEY=your_langsmith_api_key
   INDEX_NAME=your_index_name
   ```

### Running the Application

1. Start the Streamlit frontend application:

   ```bash
   streamlit run app.py
   ```

2. Open the provided URL in your browser to access the PDF Chat interface.

   - Upload your PDF document.
   - Ask questions related to the document's content.

## Contribution

Feel free to submit issues or pull requests for enhancements or bug fixes.
