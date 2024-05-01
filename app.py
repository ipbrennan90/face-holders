import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.schema.runnable.config import RunnableConfig
from langchain_experimental.text_splitter import SemanticChunker

from operator import itemgetter
import chainlit as cl  # importing chainlit for our app

from dotenv import load_dotenv

load_dotenv()

loader = PyMuPDFLoader("https://d18rn0p25nwr6d.cloudfront.net/CIK-0001326801/c7318154-f6ae-4866-89fa-f0c589f2ee3d.pdf")

document = loader.load()

text_splitter = SemanticChunker(OpenAIEmbeddings())

documents = text_splitter.split_documents(document)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

qdrant_vector_store = Qdrant.from_documents(
    documents,
    embeddings,
    location=":memory:",
    collection_name="Meta 10k Filing",
)

retriever = qdrant_vector_store.as_retriever()

template = """You are an expert advisor for investors, you are helping a prospective investor in the Meta company answer questions they have on the recent Meta 10k filings document.
You should provide a detailed answer to the question based on the information in the provided context. When asked questions on different parts of the Meta business such as
the board of directors, answer with the names of the employees when possible.

Context:
{context}

Question:
{question}
"""

prompt = ChatPromptTemplate.from_template(template)

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, streaming=True)

retrieval_augmented_chain = {"context": itemgetter("question") | retriever, "question": itemgetter("question")}  | prompt | llm | StrOutputParser()

@cl.on_chat_start
async def on_chat_start():
  cl.user_session.set("runnable", retrieval_augmented_chain)


@cl.on_message
async def main(message: cl.Message):
  runnable = cl.user_session.get("runnable")
  msg = cl.Message(content="")

  async for chunk in runnable.astream(
      {"question": message.content},
      config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()])
  ):
      await msg.stream_token(chunk)

  await msg.send()





