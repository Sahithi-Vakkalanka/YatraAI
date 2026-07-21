import json

from langchain_core.prompts import ChatPromptTemplate

from utils.llm import get_llm
from utils.retriever import get_retriever
from utils.intent import is_trip_planning_request
from utils.memory import get_chat_history

from utils.user_profile import (
    update_user_profile,
    format_user_profile
)

from prompts.travel_prompt import (
    RAG_PROMPT,
    QUERY_REWRITE_PROMPT,
    PROFILE_EXTRACTION_PROMPT
)

from prompts.trip_planner_prompt import TRIP_PLANNER_PROMPT



rag_prompt = ChatPromptTemplate.from_template(
    RAG_PROMPT
)

trip_prompt = ChatPromptTemplate.from_template(
    TRIP_PLANNER_PROMPT
)

rewrite_prompt = ChatPromptTemplate.from_template(
    QUERY_REWRITE_PROMPT
)

profile_prompt = ChatPromptTemplate.from_template(
    PROFILE_EXTRACTION_PROMPT
)



def clean_response(content):

    if isinstance(content, list):

        text = ""

        for item in content:

            if isinstance(item, dict):

                if "text" in item:

                    text += item["text"]

        return text


    if isinstance(content, dict):

        return (
            content.get("text")
            or content.get("answer")
            or str(content)
        )


    return str(content)




def format_docs(docs):

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )



def extract_preferences(
        llm,
        question,
        session_id
):

    try:

        messages = profile_prompt.invoke(
            {
                "question": question
            }
        )

        response = llm.invoke(
            messages
        )


        raw = clean_response(
            response.content
        )


        raw = raw.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        )


        data = json.loads(
            raw.strip()
        )


        update_user_profile(
            session_id,
            data
        )


    except Exception:

        pass





def rewrite_question(
        llm,
        question,
        history,
        profile
):

    messages = rewrite_prompt.invoke(
        {
            "question": question,
            "chat_history": history,
            "user_profile": profile
        }
    )


    response = llm.invoke(
        messages
    )


    return clean_response(
        response.content
    )






def retrieve_uploaded_docs(
        vectorstore,
        question
):

    if vectorstore is None:

        return []


    keywords = [

        "list",
        "all",
        "mentioned",
        "destinations",
        "places",
        "locations",
        "summary",
        "summarize"

    ]


    if any(
        word in question.lower()
        for word in keywords
    ):


        return list(
            vectorstore.docstore._dict.values()
        )


    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k":2
        }
    )


    return retriever.invoke(
        question
    )






def generate_trip_plan(
        llm,
        question,
        profile,
        history,
        context
):


    messages = trip_prompt.invoke(
        {

            "question": question,

            "user_profile": profile,

            "chat_history": history,

            "context": context,

            "image_context": ""

        }
    )


    response = llm.invoke(
        messages
    )


    return clean_response(
        response.content
    )






def generate_response(
        question,
        session_id,
        uploaded_vectorstore=None,
        uploaded_image_context=None
):


    llm = get_llm()



    extract_preferences(
        llm,
        question,
        session_id
    )



    profile = format_user_profile(
        session_id
    )


    history = get_chat_history(
        session_id
    )


    chat_history = history.messages



    standalone_question = rewrite_question(
        llm,
        question,
        chat_history,
        profile
    )



    docs = []

    source_type = None




    # ---------------------------
    # IMAGE ONLY MODE
    # ---------------------------

    if uploaded_image_context:


        context = ""


        source_type = "image"



    else:


        # ---------------------------
        # DOCUMENT RAG
        # ---------------------------

        docs = retrieve_uploaded_docs(
            uploaded_vectorstore,
            standalone_question
        )


        if docs:

            source_type = "uploaded"



        # ---------------------------
        # GENERAL KNOWLEDGE RAG
        # ---------------------------

        else:


            retriever = get_retriever()


            docs = retriever.invoke(
                standalone_question
            )


            source_type = "knowledge_base"



        context = format_docs(
            docs
        )




    messages = rag_prompt.invoke(
        {

            "chat_history": chat_history,

            "user_profile": profile,

            "context": context,

            "image_context":
                uploaded_image_context
                if uploaded_image_context
                else "",

            "question": question

        }
    )




    if is_trip_planning_request(question):


        answer = generate_trip_plan(
            llm,
            question,
            profile,
            chat_history,
            context
        )


    else:


        response = llm.invoke(
            messages
        )


        answer = clean_response(
            response.content
        )





    history.add_user_message(
        question
    )


    history.add_ai_message(
        answer
    )





    # SOURCES

    if source_type == "image":

        sources = [
            "Image Analysis"
        ]


    else:

        sources = sorted(
            {

                doc.metadata.get(
                    "filename",
                    (
                        "Uploaded Document"
                        if source_type=="uploaded"
                        else "Knowledge Base"
                    )
                )

                for doc in docs

            }
        )



    return {

        "answer": answer,

        "sources": sources,

        "documents": docs

    }