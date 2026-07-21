from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader


def load_documents():
    loader = DirectoryLoader(
        "data",
        glob="**/*.txt",
        loader_cls=TextLoader,
    )

    documents = loader.load()

    for doc in documents:
        path = Path(doc.metadata["source"])

        doc.metadata.update(
            {
                "source": path.as_posix(),
                "filename": path.name,
                "category": path.parent.name,
            }
        )

    return documents
