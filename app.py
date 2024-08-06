
import streamlit as st
from functions import save_uploaded_file, extract_text_from_pdf, extract_text_from_image, get_assistant_response
import os

def main():
    st.title("Document Insight Assistant")

    # Initialize chat history in session state if not already present
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    uploaded_files = st.file_uploader("Choose files to upload", type=["pdf", "txt", "png", "jpg", "jpeg"], accept_multiple_files=True)

    if uploaded_files:
        all_text_content = ""
        for uploaded_file in uploaded_files:
            file_path = save_uploaded_file(uploaded_file)
            if file_path:
                if file_path.lower().endswith('.pdf'):
                    text_content = extract_text_from_pdf(file_path)
                elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    text_content = extract_text_from_image(file_path)
                else:
                    text_content = ""
                    st.write("Unsupported file type. Only PDF, TXT, and image files are supported.")

                if text_content:
                    all_text_content += text_content + "\n\n"
                else:
                    st.write(f"Failed to process the file: {uploaded_file.name}")

                # Check if the file exists before attempting to delete it
                if os.path.exists(file_path):
                    os.remove(file_path)  # Clean up
                else:
                    print(f"File {file_path} does not exist, skipping removal.")

        if all_text_content:
            st.write("Files processed successfully. Now you may ask a question.")
            st.session_state.text_content = all_text_content
        else:
            st.write("Failed to process the files.")

    user_input = st.text_input("Enter your Query:")

    if st.button("Send"):
        if 'text_content' in st.session_state:
            text_content = st.session_state.text_content
            st.write("You:", user_input)
            # Add the user's query to the chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            # Generate the response with all prior messages as context
            conversation = ""
            for message in st.session_state.chat_history:
                conversation += f"{message['role']}: {message['content']}\n"

            response = get_assistant_response(conversation, text_content)
            st.write("Gemini:", response)

            # Add the AI's response to the chat history
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        else:
            st.write("Please upload and process files first.")

    # Display chat history
    if 'chat_history' in st.session_state:
        st.write("### Conversation History")
        for message in st.session_state.chat_history:
            if message['role'] == "user":
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**AI:** {message['content']}")

if __name__ == "__main__":
    main()
