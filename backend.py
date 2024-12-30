import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_mistralai import ChatMistralAI
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from pinecone.grpc import PineconeGRPC as Pinecone
from typing import Dict, List


from dotenv import load_dotenv
load_dotenv()

# Embedding model setup
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


def upload_document(doc_path: str):
  '''
  This function is used to upload a document to the Pinecone vector database.
  
  Args:
    doc_path: The path to the document to be uploaded.
  '''

  # Delete existing Pinecone namespace
  pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
  index = pc.Index(host=os.environ.get("INDEX_HOST"))

  # Initializing namespace
  index.upsert(
    vectors=[
        {
            "id": "1",
            "values": [1.0] * 768,
        },
    ],
    namespace="document_namespace",
  )

  # Delete existing Pinecone namespace
  index.delete(delete_all=True, namespace="document_namespace")
  
  # Load the document
  loader = PyPDFLoader(doc_path)

  pages = []
  for page in loader.lazy_load():
    pages.append(page)

  # Splitting text into text_chunks
  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    add_start_index=True
  )

  text_chunks = text_splitter.split_documents(pages)

  # Pinecone setup (Ingesting data into pinecone vector database)
  PineconeVectorStore.from_documents(
    text_chunks,
    embedding_model,
    index_name=os.getenv('INDEX_NAME'),
    namespace="document_namespace"
  )


def query_document(query: str, chat_history: List[Dict[str, str]] = []):
  '''
  This function is used to query the Pinecone vector database.
  
  Args:
    query: The query to be used to query the Pinecone vector database.
  '''
  llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
    max_retries=2
  )

  vectorstore = PineconeVectorStore(index_name=os.getenv("INDEX_NAME"), embedding=embedding_model, namespace="document_namespace")

  rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

  retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
  combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)

  history_aware_retriever = create_history_aware_retriever(
    llm=llm, retriever=vectorstore.as_retriever(), prompt=rephrase_prompt
  )

  retrival_chain = create_retrieval_chain(
    retriever=history_aware_retriever, combine_docs_chain=combine_docs_chain
  )

  result = retrival_chain.invoke(input={"input": query, "chat_history": chat_history})
  return result["answer"]