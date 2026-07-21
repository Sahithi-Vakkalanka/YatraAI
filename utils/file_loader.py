from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS

from utils.embeddings import get_embeddings

import os



def create_uploaded_vectorstore(files):


    all_docs = []



    for file in files:


        file_path = file["path"]

        filename = file["name"]


        suffix = file_path.split(".")[-1].lower()



        if suffix == "pdf":

            loader = PyPDFLoader(
                file_path
            )


        elif suffix == "docx":

            loader = Docx2txtLoader(
                file_path
            )


        elif suffix == "txt":

            loader = TextLoader(
                file_path,
                encoding="utf-8"
            )


        else:

            continue



        docs = loader.load()



        # ADD FILENAME METADATA HERE

        for doc in docs:

            doc.metadata["filename"] = filename

            doc.metadata["source_type"] = "uploaded"



        all_docs.extend(
            docs
        )




    splitter = RecursiveCharacterTextSplitter(

        chunk_size=900,

        chunk_overlap=180,

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




    chunks = splitter.split_documents(
        all_docs
    )



    for index, chunk in enumerate(chunks):


        metadata = chunk.metadata


        metadata["chunk_id"] = index


        metadata["source_type"] = "uploaded"



        metadata.setdefault(
            "filename",
            "uploaded_document"
        )



        metadata.setdefault(
            "page",
            metadata.get(
                "page",
                "N/A"
            )
        )



    embeddings = get_embeddings()



    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )



    return vectorstore