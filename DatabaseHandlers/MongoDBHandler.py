from dotenv import load_dotenv
load_dotenv()
import os
from pymongo import MongoClient
from pymongo.errors import OperationFailure

class databaseHandler:
    def __init__(self, host="localhost", port=27017):
        self.host = host
        self.port = port
        self.uri_template = os.getenv("USER_MONGO_URI")
        self.admin_user = os.getenv("ADMIN_USER")
        self.admin_pwd = os.getenv("ADMIN_PWD")
        self.connect_template = os.getenv("MONGO_URI")
        self.ADMIN_URI = self.uri_template.format(new_user=self.admin_user, new_pwd=self.admin_pwd, db_name="admin")

    """ USER MANAGEMENT """
    def createUser(self, username, password, role, db):
        client = MongoClient(self.ADMIN_URI)
        try:
            admin_db = client[db]
            result = admin_db.command("createUser", username,
                                      pwd=password,
                                      roles=[{"role": role, "db": db}])
            if result["ok"] == 1.0:
                print("User created:", username, "for database", db, "with role", role)
            else:
                print("User creation failed: ", result)
        except OperationFailure as error:
            print(f"createUser error: {error}")

    def dropUser(self, username, db):
        client = MongoClient(self.ADMIN_URI)
        try:
            admin_db = client[db]
            result = admin_db.command("dropUser", username)
            if result["ok"] == 1.0:
                print("User dropped:", username)
            else:
                print("User dropped failed: ", result)
        except OperationFailure as error:
            print(f"dropUser error: {error}")

    """ DATABASE MANAGEMENT """
    def createDatabase(self, username, password, db):
        MONGO_CLIENT = self.connect_template.format(new_user=username, new_pwd=password)
        client = MongoClient(MONGO_CLIENT)
        db_client = client[db]
        db_client["__init__"].insert_one({"created": True})
        db_client.drop_collection("__init__")
        print(f"Database '{db}' created.")

    def dropDatabase(self, username, password, db):
        MONGO_CLIENT = self.connect_template.format(new_user=username, new_pwd=password)
        client = MongoClient(MONGO_CLIENT)
        client.drop_database(db)
        print(f"Database '{db}' dropped.")

    """ TABLE MANAGEMENT """
    def createTable(self, username, password, db, table):
        MONGO_CLIENT = self.connect_template.format(new_user=username, new_pwd=password)
        client = MongoClient(MONGO_CLIENT)
        db_client = client[db]
        db_client.create_collection(table)
        print(f"Table '{table}' created.")

    def dropTable(self, username, password, db, table):
        MONGO_CLIENT = self.connect_template.format(new_user=username, new_pwd=password)
        client = MongoClient(MONGO_CLIENT)
        db_client = client[db]
        db_client.drop_collection(table)
        print(f"Table '{table}' dropped.")

    def listTable(self, username, password, db):
        MONGO_CLIENT = self.connect_template.format(new_user=username, new_pwd=password)
        client = MongoClient(MONGO_CLIENT)
        db_client = client[db]
        result = db_client.list_collection_names()
        print(f"Table in '{db}': '{result}'")
        return result

    """ CRUD OPERATIONS """
    def createEntry(self, username, password, db, table, query):
        MONGO_CLIENT = self.connect_template.format(new_user=username, new_pwd=password)
        client = MongoClient(MONGO_CLIENT)
        db_client = client[db]
        result = db_client[table].insert_one(query)
        print(f"Inserted {result.inserted_id}.")

    def readEntry(self, username, password, db, table, query):
        MONGO_CLIENT = self.connect_template.format(new_user=username, new_pwd=password)
        client = MongoClient(MONGO_CLIENT)
        db_client = client[db]
        result = db_client[table].find_one(query)
        print(f"Read {result.inserted_id}.")
        return result

    def updateEntry(self, username, password, db, table, query, update):
        MONGO_CLIENT = self.connect_template.format(new_user=username, new_pwd=password)
        client = MongoClient(MONGO_CLIENT)
        db_client = client[db]
        result = db_client[table].update_one(query, {"$set": update})
        print(f"Update {result.modified_count}.")

    def deleteEntry(self, username, password, db, table, query):
        MONGO_CLIENT = self.connect_template.format(new_user=username, new_pwd=password)
        client = MongoClient(MONGO_CLIENT)
        db_client = client[db]
        result = db_client[table].delete_one(query)
        print(f"Delete {result.deleted_count}.")
