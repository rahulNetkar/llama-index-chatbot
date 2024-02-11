import streamlit as st
import os
from index import create_index
from llama_index.memory import ChatMemoryBuffer

st.set_page_config(
    page_title="Chat with your personal file, powered by LlamaIndex",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
st.title("Chat with your personal file, powered by LlamaIndex 💬🦙")
st.info(
    "Check out my other Gen AI projects here [Github](https://www.github.com/rahulNetkar)",
    icon="📃",
)


save_path = "data"

if not os.path.exists(save_path):
    os.makedirs(save_path)

# Sidebar
with st.sidebar:
    api_key = st.text_input("API Key", placeholder="Paste your Gemini-Pro API key")

    st.markdown(
        """
                ### [Get your own api key](https://ai.google.dev/tutorials/setup)
                .\n        
                """
    )

    uploaded_file = st.file_uploader(
        "Upload your file",
        type="pdf",
        help="Please upload the pdf",
        accept_multiple_files=True,
    )

    try:
        if uploaded_file is not None:
            # To read file as bytes:
            for file in uploaded_file:
                bytes_data = file.getvalue()

            # Save the uploaded file to the 'data' directory
            with open(os.path.join(save_path, file.name), "wb") as out_file:
                out_file.write(bytes_data)

            st.success("PDF file saved in data directory")
    except Exception as e:
        print(e)
        st.warning("Please upload file")

    st.markdown(
        """
                .\n
                .\n
                .\n
                Made with :heart: by [Rahul Netkar](www.github.com/rahulNetkar) . 
                [Twitter](https://twitter.com/RahulNetkar) . [LinkedIn](https://www.linkedin.com/in/rahul-netkar-aa065a1b1/)
                """
    )


if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question about the file you uploaded",
        }
    ]

try:
    index = create_index(api_key=api_key, file_path=save_path)

    memory = ChatMemoryBuffer.from_defaults(token_limit=1500)

    if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(
            chat_mode="context",
            memory=memory,
        )

    if prompt := st.chat_input(
        "Your question"
    ):  # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:  # Display the prior chat messages
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chat_engine.chat(prompt)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)
except Exception as e:
    st.toast(e)
# except ValidationError as e:
#     st.warning("Please paste the api key before uploading the file")
