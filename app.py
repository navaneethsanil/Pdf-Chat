import os
import streamlit as st
from backend import upload_document, query_document

# Initialize session state variables
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False  # Tracks whether a document has been uploaded
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "query_history" not in st.session_state:
    st.session_state.query_history = []
if "response" not in st.session_state:
    st.session_state.response = []
if "document_path" not in st.session_state:
    st.session_state.document_path = None

# Function to reset upload state
def reset_upload():
    st.session_state.uploaded = False
    st.session_state.chat_history = []
    st.session_state.query_history = []
    st.session_state.response = []
    st.session_state.document_path = None

with st.sidebar:
    uploaded_file = st.file_uploader("Upload your PDF document", type=("pdf"))

    # Button to reset upload state
    if st.session_state.uploaded:
        if st.button("Upload New Document"):
            reset_upload()

    # Create the uploaded_files directory if it doesn't exist
    if not os.path.exists("./uploaded_files"):
        os.makedirs("./uploaded_files")
    
    if uploaded_file and not st.session_state.uploaded:
        with st.spinner("Uploading document, please wait..."):
            # Save the uploaded file to a temporary path
            temp_file_path = f"./uploaded_files/{uploaded_file.name}"
            
            # Write the uploaded file to the temporary path
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(uploaded_file.read())
            
            # Pass the temporary file path to your upload_document function
            upload_document(temp_file_path)
            
            # Store the document path in session state and set uploaded flag
            st.session_state.document_path = temp_file_path
            st.session_state.uploaded = True

        st.success("Document uploaded successfully!")
        st.write("Now you can ask anything about the document.")

if st.session_state.uploaded:
    st.title("PDF Chat")
    query = st.chat_input("What is the document about?")
    if query:
        with st.spinner("Searching for answer, please wait..."):
            answer = query_document(
                query, 
                chat_history=st.session_state.chat_history
            )

        # Update session state with the query and response
        st.session_state.chat_history.append({"role": "user", "content": query})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.session_state.query_history.append(query)
        st.session_state.response.append(answer)

    # Display chat history
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
else:
    st.title("PDF Chat")
    st.warning("To continue, please upload your document first.") 
