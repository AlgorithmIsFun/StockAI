from dotenv import load_dotenv
load_dotenv()
import os
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
class databaseHandler:
    def __init__(self, host="localhost", port=27017):
        self.host = host
        self.port = port
        self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        self.CHROMA_PATH = "data/rag_chroma_db"
        self.vector_store = None
    """ USER MANAGEMENT Not supported"""
    def createUser(self, username, password, role, db):
        pass

    def dropUser(self, username, db):
        pass

    """ DATABASE MANAGEMENT """
    def createDatabase(self, username, password, db):
        self.vector_store = Chroma.from_documents(
            documents=db,
            embedding=self.embeddings,
            persist_directory=self.CHROMA_PATH,  # Optional: directory to save the database
            collection_name="knowledge_base_v1"  # Optional: collection name
        )
        print("Ingestion complete.")
    def dropDatabase(self, username, password, db):
        pass

    """ TABLE MANAGEMENT """
    def createTable(self, username, password, db, table):
        # Load Documents
        loader = TextLoader(db) #document location
        documents = loader.load()
        # Split Data into Chunks
        ids = self.vector_store.add_documents(documents)
        print(f"Added 1 new document with ID: {ids[0]}")

    def dropTable(self, username, password, db, table):
        where_filter = {"source": db}
        self.vector_store.delete(where=where_filter)
        print(f"Successfully deleted all documents matching filter: {where_filter}")

    def listTable(self, username, password, db):
        return self.vector_store

    """ CRUD OPERATIONS Not supported"""
    def createEntry(self, username, password, db, table, query):
        pass
    def readEntry(self, username, password, db, table, query):
        pass
    def updateEntry(self, username, password, db, table, query, update):
        pass
    def deleteEntry(self, username, password, db, table, query):
        pass