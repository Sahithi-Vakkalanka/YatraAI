# import os

# from dotenv import load_dotenv
# from langchain_community.vectorstores import FAISS

# from utils.embeddings import get_embeddings

# load_dotenv()


# def get_retriever():

#     embeddings = get_embeddings()

#     vectorstore = FAISS.load_local(
#         os.getenv("VECTORSTORE_PATH"),
#         embeddings,
#         allow_dangerous_deserialization=True
#     )

#     return vectorstore.as_retriever(
#     search_type="similarity_score_threshold",
#     search_kwargs={
#         "k": int(os.getenv("TOP_K")),
#         "score_threshold": 0.35
#     }
# )

import os

from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS

from utils.embeddings import get_embeddings


load_dotenv()



def get_retriever():

    embeddings = get_embeddings()


    vectorstore = FAISS.load_local(
        os.getenv("VECTORSTORE_PATH"),
        embeddings,
        allow_dangerous_deserialization=True
    )


    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": int(os.getenv("TOP_K"))
        }
    )


    return retriever