import os
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
from langchain_community.vectorstores.mongodb_atlas import MongoDBAtlasVectorSearch
from langchain_community.document_loaders import DirectoryLoader
from langchain.chains.retrieval_qa.base import RetrievalQA
import gradio as gr
from gradio.themes.base import Base
from dotenv import load_dotenv, find_dotenv

# loading environment variables
load_dotenv(find_dotenv())

client = MongoClient(os.getenv("MONGODB_URL"))
dbName = "langchain_demo"
collectionName = "collection_of_text_blobs"
collection = client[dbName][collectionName]

loader = DirectoryLoader('./sample_files', glob="./*.txt", show_progress=True)
data = loader.load()

embeddings = OpenAIEmbeddings()

vector_stores = MongoDBAtlasVectorSearch.from_documents(documents=data, embedding=embeddings, collection=collection)


def query_data(query):
    docs = vector_stores.similarity_search(query, k=1)
    as_output = docs[0].page_content
    llm = OpenAI(temperature=1)
    retriever = vector_stores.as_retriever()
    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriver=retriever

    )
    retriever_output = qa.run(query)

    return as_output, retriever_output
