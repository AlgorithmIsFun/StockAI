from dotenv import load_dotenv
load_dotenv()
import couchdb
import os
import traceback

class databaseHandler:
    def __init__(self, host="localhost", port=5984):
        self.host = host
        self.port = port
        self.server = self.connect()

    def connect(self, user=None, password=None):
        try:
            if user and password:
                self.admin_user = user
                self.admin_pwd = password
            else:
                self.admin_user = os.getenv("ADMIN_USER")
                self.admin_pwd = os.getenv("ADMIN_PWD")
            self.server = couchdb.Server(f'http://{self.admin_user}:{self.admin_pwd}@{self.host}:{self.port}/')
            print(f"Connected to CouchDB server: {self.server}")
            return self.server
        except Exception as e:
            print(f"Could not connect to CouchDB: {e}")
    """ USER MANAGEMENT """
    def createUser(self, username, password, role, db):
        try:
            self.server = self.connect()
            users_db = self.server['_users']
            print("Accessed _users database:", users_db)
            user_doc = {
                "_id": f"org.couchdb.user:{username}",
                "name": username,
                "type": "user",
                "roles": role,  # Roles define access rights
                "password": password  # CouchDB hashes this on save
            }
            doc_id, doc_rev = users_db.save(user_doc)
            print(f"User '{username}' created successfully")
        except couchdb.Unauthorized:
            print("Error: Authentication failed. Check the admin credentials in ADMIN_URL.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            traceback.print_exc()
    def dropUser(self, username, db):
        pass

    """ DATABASE MANAGEMENT """
    def createDatabase(self, username, password, db):
        try:
            self.server = self.connect(username, password)
            if db in self.server:
                # Access existing database
                db = self.server[db]
                print(f"Accessed existing database: {db}")
            else:
                # Create a new database
                db = self.server.create(db)
                print(f"Created new database: {db}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def dropDatabase(self, username, password, db):
        try:
            self.server = self.connect(username, password)
            if db in self.server:
                del self.server[db]
                print(f"Database '{db}' was successfully deleted.")
            else:
                print(f"Database '{db}' does not exist on the server.")
        except Exception as e:
            print(f"An error occurred: {e}")

    """ TABLE MANAGEMENT """
    #Note: CouchDB does not support tables, so this will remain no implementation
    def createTable(self, username, password, db, table):
        pass
    def dropTable(self, username, password, db, table):
        pass
    def listTable(self, username, password, db):
        pass

    """ CRUD OPERATIONS """
    def createEntry(self, username, password, db, table, query):
        try:
            self.server = self.connect(username, password)
            if db in self.server:
                doc_id, doc_rev = db.save(query)
                print(f"Document created with ID: {doc_id} and Revision: {doc_rev}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def readEntry(self, username, password, db, table, query):
        try:
            self.server = self.connect(username, password)
            if db in self.server:
                retrieved_doc = db[table]
                print(f"Retrieved Document: {retrieved_doc}")
                return retrieved_doc
        except Exception as e:
            print(f"An error occurred: {e}")
    def updateEntry(self, username, password, db, table, query, update):
        try:
            self.server = self.connect(username, password)
            if db in self.server:
                retrieved_doc = db[table]
                retrieved_doc[query] = update
                updated_id, updated_rev = db.save(retrieved_doc)
                print(f"Document updated. New Revision: {updated_rev}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def deleteEntry(self, username, password, db, table, query):
        try:
            self.server = self.connect(username, password)
            if db in self.server:
                retrieved_doc = db[table]
                db.delete(retrieved_doc)
                print(f"Document deleted.")
        except Exception as e:
            print(f"An error occurred: {e}")