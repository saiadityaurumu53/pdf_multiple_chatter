import streamlit as st
from dotenv import load_dotenv
#note: this is the function which we will load in the main in order for our application to use the secret variables inside the main
#Now as we have initialized the function in the first line of the main, Lang Chain will be able to use it 

from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter



def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        #now initializing the PDF reader object
        pdf_reader = PdfReader(pdf)
        #here, the pdf object that has pages is given
        #Now, we will read each page and add it to the text
        for page in pdf_reader.pages:
            text += page.extract_text()

    return text

def get_text_chunks(text):
    #we will use the LangChain
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks





def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")

    st.header("Chat with multiple PDFs :books:")

    #below the header we want the user to have the user to type inputs so we will 
    st.text_input("Ask a question about your documents:")

    #now we also want a side bar where the user is going to upload the documents
    #Also if we want to keep or put things inside it then we are gonna use the with keyword
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        #now we will create a button with the name and whose functionality is to process
        #Here, the multiple files are stored here in the pdf_docs variable

        if st.button("Process"):
            with st.spinner("Processing"):
                #Now if the button is pressed then this if block is then executed

                #Step1:  we are going to get the pdf text : Here, we are gonna take the raw text from our pdfs
                raw_text = get_pdf_text(pdf_docs)
                #st.write(raw_text)

                #Step2: get the text chunks
                text_chunks = get_text_chunks(raw_text)
                st.write(text_chunks)

                #Step 3: Create the vector store with the Embeddings


if __name__ == '__main__':
    main()