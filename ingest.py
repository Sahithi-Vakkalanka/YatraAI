import os

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from utils.loader import load_documents
from utils.embeddings import get_embeddings

load_dotenv()

documents = load_documents()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=int(os.getenv("CHUNK_SIZE")),
    chunk_overlap=int(os.getenv("CHUNK_OVERLAP")),
    separators=[
        "\n## ",
        "\n### ",
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)

chunks = splitter.split_documents(documents)
for index, chunk in enumerate(chunks):

    metadata = chunk.metadata

    metadata["chunk_id"] = index

    metadata["source_type"] = "knowledge_base"

    metadata.setdefault("filename", "Unknown")

    metadata.setdefault("category", "General")

    metadata.setdefault("page", metadata.get("page", "N/A"))

embeddings = get_embeddings()

vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)

vectorstore.save_local(
    os.getenv("VECTORSTORE_PATH")
)

print("Vector database created successfully!")