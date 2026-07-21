from utils.retriever import get_retriever


retriever = get_retriever()


docs = retriever.invoke(
    "summer destinations in India"
)


print("\nNUMBER OF DOCUMENTS:")
print(len(docs))


for doc in docs:

    print("\nSOURCE:")
    print(
        doc.metadata
    )

    print("\nCONTENT:")
    print(
        doc.page_content[:300]
    )