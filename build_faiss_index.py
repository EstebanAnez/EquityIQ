# RAG index builder
import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()

# Folder where RAG files are stored
RAG_FOLDER = "rag_files"

# Folder where FAISS index will be saved
FAISS_INDEX_PATH = "faiss_index"

documents = []

# load the files from the rag_files folder
for file_name in os.listdir(RAG_FOLDER):
    file_path = os.path.join(RAG_FOLDER, file_name)

    if file_name.endswith(".pdf"):
        print(f"Loading PDF: {file_name}")
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())

    elif file_name.endswith(".csv"):
        print(f"Loading CSV: {file_name}")
        loader = CSVLoader(file_path=file_path)
        documents.extend(loader.load())

print(f"Total documents loaded: {len(documents)}")

# split the documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)

print(f"Total chunks created: {len(chunks)}")

# create embeddings and store them in FAISS
embeddings = OpenAIEmbeddings()

vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)

# save FAISS index locally
vectorstore.save_local(FAISS_INDEX_PATH)

print("FAISS index created and saved successfully.")
