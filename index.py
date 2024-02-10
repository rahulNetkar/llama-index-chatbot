from llama_index import (
    VectorStoreIndex,
    ServiceContext,
    SimpleDirectoryReader,
    set_global_service_context,
)

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import streamlit as st


@st.cache_resource(show_spinner=False)
def create_index(api_key, file_path):
    with st.spinner(
        text="Loading and indexing the docs – hang tight! This should take 1-2 minutes."
    ):
        llm = ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model="gemini-pro",
        )

        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key,
        )

        # Setting global context to Gemini-pro and google embeddings
        service_context = ServiceContext.from_defaults(llm=llm, embed_model=embeddings)
        set_global_service_context(service_context=service_context)

        document = SimpleDirectoryReader(file_path).load_data()

        index = VectorStoreIndex.from_documents(document)

        return index
