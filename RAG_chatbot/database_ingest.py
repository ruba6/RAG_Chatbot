from langchain_community.document_loaders import PyPDFDirectoryLoader #loads all PDFs from a directory and returns LangChain Document objects
from langchain_text_splitters import RecursiveCharacterTextSplitter  #splits large text into smaller chunks
from langchain_chroma import Chroma  #vector DB wrapper to store embeddings.
from dotenv import load_dotenv
from uuid import uuid4  #to create unique IDs for each chunk.
import os
from langchain_huggingface import HuggingFaceEmbeddings

#pdf data path
DATA_PATH = r"data"
#script creates chromadb when it is executed to store chunks
CHROMA_PATH = r"chroma_db" 

# Creates an embeddings object using the small, fast Sentence-Transformer model (good for local use).
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


# semantic db that stores chunks of the file 
# Instantiates Chroma vector store that will store vectors under chroma_db.
vector_store = Chroma(
    collection_name="example_collections",
    embedding_function=embeddings_model,
    persist_directory=CHROMA_PATH,
)


def ingest_single_file(file_path):
    from langchain_community.document_loaders import PyPDFLoader
    print("Loading documents...")

    loader = PyPDFLoader(file_path)
    documents = loader.load()
    print("Documents loaded:", len(documents))
    if not documents:
        print("No PDFs found in data folder!")
        exit()



    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)
    print("Chunks created:", len(chunks))


    ids = [str(uuid4()) for _ in range(len(chunks))]

    vector_store.add_documents(documents=chunks, ids=ids)
    print("Data successfully indexed into ChromaDB")
