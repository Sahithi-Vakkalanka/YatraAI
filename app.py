import os
import uuid
import chainlit as cl

from utils.rag_chain import generate_response
from utils.file_loader import create_uploaded_vectorstore
from utils.image_processor import process_image


@cl.on_chat_start
async def start():

    cl.user_session.set(
        "session_id",
        str(uuid.uuid4())
    )

    cl.user_session.set(
        "uploaded_vectorstore",
        None
    )

    cl.user_session.set(
        "uploaded_files",
        []
    )

    cl.user_session.set(
        "uploaded_image_path",
        None
    )

    await cl.Message(
        content="""
# 🌍 Welcome to **YatraAI**

### Your AI Travel Copilot ✈️

I can help you with:

🗺️ Destination recommendations

🧳 Personalized trip planning

🏨 Hotels & attractions

🍜 Local food suggestions

📄 Travel document analysis

🖼️ Landmark & destination recognition

💰 Budget travel suggestions

🎒 Packing advice

---

### Supported uploads

📄 PDF

📝 DOCX

📃 TXT

🖼️ JPG / PNG / JPEG

---

Just ask your travel question or upload your travel files!
"""
    ).send()

    await cl.Message(
        content="""
### 💡 Try asking:

• Plan a 5-day Kerala trip

• Compare Rajasthan and Gujarat

• Tell me about Munnar

• Suggest hill stations under ₹20,000

• Identify this monument

• Upload a travel brochure and summarize it
"""
    ).send()


@cl.on_message
async def main(message: cl.Message):

    uploaded_vectorstore = cl.user_session.get(
        "uploaded_vectorstore"
    )

    uploaded_image_path = cl.user_session.get(
        "uploaded_image_path"
    )


    # -----------------------------
    # CLEAR UPLOADED DOCUMENTS
    # -----------------------------

    if message.content.lower().strip() in [
        "clear documents",
        "reset uploads"
    ]:

        cl.user_session.set(
            "uploaded_files",
            []
        )

        cl.user_session.set(
            "uploaded_vectorstore",
            None
        )

        cl.user_session.set(
            "uploaded_image_path",
            None
        )

        await cl.Message(
            content="""
🗑️ Uploaded documents cleared.

🖼️ Uploaded image cleared.

YatraAI will now use its built-in travel knowledge base.

You can upload new files anytime.
"""
        ).send()

        return


    # -----------------------------
    # HANDLE NEW FILE UPLOAD
    # -----------------------------

    if message.elements:

        image_files = []

        document_files = []


        for file in message.elements:

            extension = os.path.splitext(
                file.name
            )[1].lower()


            if extension in [
                ".png",
                ".jpg",
                ".jpeg"
            ]:

                image_files.append(file)


            elif extension in [
                ".pdf",
                ".txt",
                ".docx"
            ]:

                document_files.append(file)


        # -----------------------------
        # HANDLE IMAGE
        # -----------------------------

        if image_files:

            image_file = image_files[0]

            cl.user_session.set(
                "uploaded_image_path",
                image_file.path
            )

            uploaded_image_path = image_file.path

            await cl.Message(
                content=f"""
🖼️ Image uploaded successfully.

**{image_file.name}**

Try asking:

• What place is this?

• Describe this destination

• Is this worth visiting?

• Suggest nearby attractions
"""
            ).send()


        # -----------------------------
        # HANDLE DOCUMENT MEMORY
        # -----------------------------

        if document_files:

            uploaded_files = cl.user_session.get(
                "uploaded_files"
            )

            uploaded_files.extend(
                [
                    {
                        "path": file.path,
                        "name": file.name
                    }
                    for file in document_files
                ]
            )

            cl.user_session.set(
                "uploaded_files",
                uploaded_files
            )


            vectorstore = create_uploaded_vectorstore(
                uploaded_files
            )

            cl.user_session.set(
                "uploaded_vectorstore",
                vectorstore
            )

            uploaded_vectorstore = vectorstore


            uploaded_names = "\n".join(
                f"• {file['name']}"
                for file in uploaded_files
            )


            await cl.Message(
                content=f"""
## 📄 Documents Ready

Successfully indexed **{len(uploaded_files)} document(s)**

{uploaded_names}

You can now ask questions using these documents.
"""
            ).send()

    # -----------------------------
    # PROCESS IMAGE ONLY WHEN USER ASKS
    # -----------------------------

    image_context = None

    if uploaded_image_path:

        image_context = process_image(
            uploaded_image_path
        )


    # -----------------------------
    # CHECK DOCUMENT COMMANDS
    # -----------------------------

    document_queries = [
        "compare documents",
        "compare uploads",
        "list uploaded docs",
        "list documents",
        "summarize uploads",
        "summarize documents"
    ]


    if any(
        query in message.content.lower()
        for query in document_queries
    ):

        if uploaded_vectorstore is None:

            await cl.Message(
                content="""
📂 No uploaded documents found.

Upload one or more travel documents first.
"""
            ).send()

            return


    # -----------------------------
    # GENERATE RESPONSE
    # -----------------------------

    thinking = cl.Message(
        content="✈️ Planning your trip..."
    )

    await thinking.send()


    try:

        result = generate_response(
            message.content,
            cl.user_session.get("session_id"),
            uploaded_vectorstore,
            image_context
        )


    except Exception as e:

        await thinking.update(
            content=f"""
❌ Something went wrong.

{str(e)}
"""
        )

        return



    answer = result["answer"].strip()

    sources = result["sources"]



    # -----------------------------
    # BETTER REFERENCES SECTION
    # -----------------------------

    if sources:

        answer += (
            "\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "### 📚 References\n\n"
        )

        for source in sources:

            answer += f"📄 {source}\n"



    # -----------------------------
    # UPDATE THINKING MESSAGE
    # -----------------------------

    thinking.content = answer

    await thinking.update()
    
# import os
# import uuid
# import chainlit as cl

# from utils.rag_chain import generate_response
# from utils.file_loader import create_uploaded_vectorstore
# from utils.image_processor import process_image


# @cl.on_chat_start
# async def start():

#     cl.user_session.set(
#         "session_id",
#         str(uuid.uuid4())
#     )

#     cl.user_session.set(
#         "uploaded_vectorstore",
#         None
#     )

#     # Stores every uploaded document during this chat session
#     cl.user_session.set(
#         "uploaded_files",
#         []
#     )

#     cl.user_session.set(
#         "uploaded_image_path",
#         None
#     )

#     await cl.Message(
#         content="""
# # 🌍 Welcome to YatraAI

# Your AI Travel Copilot ✈️

# You can:

# - Ask travel questions
# - Plan trips
# - Upload travel documents (PDF, DOCX, TXT)
# - Upload travel images

# Your uploads are optional.
# Ask anything whenever you are ready!
# """
#     ).send()


# @cl.on_message
# async def main(message: cl.Message):

#     uploaded_vectorstore = cl.user_session.get(
#         "uploaded_vectorstore"
#     )

#     uploaded_image_path = cl.user_session.get(
#         "uploaded_image_path"
#     )

# # -----------------------------
# # CLEAR UPLOADED DOCUMENTS
# # -----------------------------

#     if message.content.lower().strip() in [
#         "clear documents",
#         "reset uploads"
#     ]:

#         cl.user_session.set(
#             "uploaded_files",
#             []
#         )

#         cl.user_session.set(
#             "uploaded_vectorstore",
#             None
#         )

#         await cl.Message(
#             content=(
#                 "🗑 Uploaded documents cleared successfully.\n\n"
#                 "YatraAI will now answer using only the built-in travel knowledge base.\n\n"
#                 "You can upload new documents anytime."
#             )
#         ).send()

#         return 

#     # -----------------------------
#     # HANDLE NEW FILE UPLOAD
#     # -----------------------------

#     if message.elements:

#         image_files = []

#         document_files = []

#         for file in message.elements:

#             extension = os.path.splitext(
#                 file.name
#             )[1].lower()

#             # IMAGE

#             if extension in [
#                 ".png",
#                 ".jpg",
#                 ".jpeg"
#             ]:

#                 image_files.append(file)

#             # DOCUMENT

#             elif extension in [
#                 ".pdf",
#                 ".txt",
#                 ".docx"
#             ]:

#                 document_files.append(file)

#         # -----------------------------
#         # HANDLE IMAGE
#         # -----------------------------

#         if image_files:

#             image_file = image_files[0]

#             cl.user_session.set(
#                 "uploaded_image_path",
#                 image_file.path
#             )

#             uploaded_image_path = image_file.path

#         # -----------------------------
#         # HANDLE DOCUMENT MEMORY
#         # -----------------------------

#         if document_files:

#             uploaded_files = cl.user_session.get(
#                 "uploaded_files"
#             )

#             # Add newly uploaded files to existing session files
#             uploaded_files.extend(
#                 [
#                     {
#                         "path": file.path,
#                         "name": file.name
#                     }
#                     for file in document_files
#                 ]
#             )

#             cl.user_session.set(
#                 "uploaded_files",
#                 uploaded_files
#             )

#             # Rebuild vectorstore using ALL uploaded documents
#             vectorstore = create_uploaded_vectorstore(
#                 uploaded_files
#             )

#             cl.user_session.set(
#                 "uploaded_vectorstore",
#                 vectorstore
#             )

#             uploaded_vectorstore = vectorstore

#             await cl.Message(
#                 content=f"""
#             ✅ Uploaded {len(document_files)} new document(s)."""

#             # 📄 Total active documents: **{len(uploaded_files)}**

#             # You can now ask questions using all uploaded documents.
#             ).send()

#     # -----------------------------
#     # PROCESS IMAGE ONLY WHEN USER ASKS
#     # -----------------------------

#     image_context = None

#     if uploaded_image_path:

#         image_context = process_image(
#             uploaded_image_path
#         )

#     # -----------------------------
#     # GENERATE RESPONSE
#     # -----------------------------

#     result = generate_response(
#         message.content,
#         cl.user_session.get("session_id"),
#         uploaded_vectorstore,
#         image_context
#     )

#     answer = result["answer"]

#     sources = result["sources"]

#     if sources:

#         answer += "\n\n---\n### 📚 Sources\n"

#         for source in sources:

#             answer += f"- {source}\n"

#     await cl.Message(
#         content=answer
#     ).send()

