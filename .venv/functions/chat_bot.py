import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

def chat_bot(document_path, user_input):
        
        # Load and process the document(s)
        document=TextLoader(document_path).load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        chunks=text_splitter.split_documents(documents=document)

        # Create vector store and retriever
        embedding=OpenAIEmbeddings(model="text-embedding-3-large")
        llm=ChatOpenAI(model="gpt-4o")
        vector_store=Chroma.from_documents(chunks, embedding)
        retriever=vector_store.as_retriever()

        # Initialize the chat history
        chat_history = []


        prompt_template=ChatPromptTemplate.from_messages([
        ("system",""" You are an assistance for anserwing questions about 
        tournament poker rules. Use the provided context to respond. If the answer 
        isn't clear, acknowledge that you don't know. Limit your response to three 
        concise sentences.{context} 
        """),
        ("human","{history}\nUser: {input}")
        ])

         # Create chain
        qa_chain = create_stuff_documents_chain(llm, prompt_template)
        rag_chain = create_retrieval_chain(retriever, qa_chain)

        # Format history as a single string
        history_text = "\n".join([f"User: {msg['user']}\nBot: {msg['bot']}" for msg in chat_history])

        # Get response from RAG chain
        response = rag_chain.invoke({"input": user_input, "history": history_text})
    
        # Extract bot's answer
        bot_answer = response['answer']
    
        return bot_answer

