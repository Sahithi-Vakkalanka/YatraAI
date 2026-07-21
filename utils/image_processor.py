import base64

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os


load_dotenv()


def process_image(image_path):

    llm = ChatGoogleGenerativeAI(
        model=os.getenv("MODEL_NAME"),
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )


    with open(image_path, "rb") as image_file:

        image_bytes = image_file.read()


    image_base64 = base64.b64encode(
        image_bytes
    ).decode("utf-8")


    message = [
        {
            "type": "text",
            "text": """
You are YatraAI.

Analyze this travel image.

Extract:
- Place name if visible
- Landmarks
- Location clues
- Text present in image
- Travel relevance

If unsure, clearly say unknown.
"""
        },
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_base64}"
            }
        }
    ]


    response = llm.invoke(
        [
            {
                "role": "user",
                "content": message
            }
        ]
    )


    return response.content