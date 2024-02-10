import streamlit as st
import os


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

    submit = st.button("Create index")

    st.markdown(
        """
                .\n
                Made with :heart: by [Rahul Netkar](www.github.com/rahulNetkar) . 
                [Twitter](https://twitter.com/RahulNetkar) . [LinkedIn](https://www.linkedin.com/in/rahul-netkar-aa065a1b1/)
                """
    )
