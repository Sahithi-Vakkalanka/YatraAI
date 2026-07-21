import os

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS

from utils.embeddings import get_embeddings


load_dotenv()


embeddings = get_embeddings()


vectorstore = FAISS.load_local(
    os.getenv("VECTORSTORE_PATH"),
    embeddings,
    allow_dangerous_deserialization=True
)


results = vectorstore.similarity_search_with_score(
    "Tell me about Munnar",
    k=5
)


for i, (doc, score) in enumerate(results):

    print("\n======================")
    print("RESULT:", i+1)
    print("SCORE:", score)

    print("METADATA:")
    print(doc.metadata)

    print("\nCONTENT:")
    print(doc.page_content[:500])