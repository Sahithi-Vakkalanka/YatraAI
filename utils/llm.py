import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


def get_llm():

    llm = ChatGoogleGenerativeAI(
        model=os.getenv("MODEL_NAME"),
        temperature=float(os.getenv("TEMPERATURE")),
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    return llm
