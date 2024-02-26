import streamlit as st






def main():
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")

    st.header("Chat with multiple PDFs :books:")

    #below the header we want the user to have the user to type inputs so we will 
    st.text_input("Ask a question about your documents:")

    #now we also want a side bar where the user is going to upload the documents
    #Also if we want to keep or put things inside it then we are gonna use the with keyword
    with st.sidebar:
        st.subheader("Your documents")
        st.file_uploader("Upload your PDFs here and click on 'Process'")
        #now we will create a button with the name and whose functionality is to process
        st.button("Process")

if __name__ == '__main__':
    main()