import streamlit as st
from dotenv import load_dotenv
#note: this is the function which we will load in the main in order for our application to use the secret variables inside the main
#Now as we have initialized the function in the first line of the main, Lang Chain will be able to use it 

from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
#from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS

#from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from html_templates import css



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

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    #embeddings = HugginFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore



def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    #here, the first step is to instantiate memory
    #we need to import it from langchain which is called conversational buffer memory
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    retriever = vectorstore.as_retriever()
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory

    )
    return conversation_chain


def handle_user_question(user_question):
    response = st.session_state.conversation({'question': user_question})
    #st.write(response)
    #we are going to take this object right here and we are going to format it for the template which we will have 
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if (i%2 == 0):
            #here we will write the user input template
            message1 = st.chat_message("user")
            message1.write(message.content)
        else:
            #here we will display the bot template
            message2 = st.chat_message("assistant")
            message2.write(message.content)


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    #this variable of conversation is created in the session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None   

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None 

    st.header("Chat with multiple PDFs :books:")

    #below the header we want the user to have the user to type inputs so we will 
    user_question = st.text_input("Ask a question about your documents:")

    if user_question:
        handle_user_question(user_question)

    


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
                vectorstore = get_vectorstore(text_chunks)

                #Step 4: Create Conversational Chain
                st.session_state.conversation = get_conversation_chain(vectorstore)


if __name__ == '__main__':
    main()