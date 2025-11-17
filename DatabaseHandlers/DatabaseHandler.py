"""DB todo list
- Create user
- Drop user
- Create a db
- Drop a db
- create a Table/collection
- Drop a Table/collection
- List Table/collection
CRUD:
- Create one entry
- Read one entry
- Update one entry
- Delete one entry
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))
from MongoDBHandler import databaseHandler as MongoHandler
from MySQLDBHandler import databaseHandler as MySQLHandler
from CouchDBHandler import databaseHandler as CouchHandler
from ChromaDBHandler import databaseHandler as ChromaHandler
technology = {
    "MongoDB": MongoHandler,
    "MySQL": MySQLHandler,
    "CouchDB": CouchHandler,
    "Chroma": ChromaHandler,
}
""" USER MANAGEMENT """
class DatabaseHandler:
    def createUser(self, tech, username, password, role, db):
        technology[tech]().createUser(username, password, role, db)
    def dropUser(self, tech, username, db):
        technology[tech]().dropUser(username, db)

    """ DATABASE MANAGEMENT """
    def createDatabase(self, tech, username, password, db):
        technology[tech]().createDatabase(username, password, db)
    def dropDatabase(self, tech, username, password, db):
        technology[tech]().dropDatabase(username, password, db)

    """ TABLE MANAGEMENT """
    def createTable(self, tech, username, password, db, table):
        technology[tech]().createTable(username, password, db, table)
    def dropTable(self, tech, username, password, db, table):
        technology[tech]().dropTable(username, password, db, table)
    def listTable(self, tech, username, password, db):
        technology[tech]().listTable(username, password, db)

    """ CRUD OPERATIONS """
    def createEntry(self, tech, username, password, db, table, query):
        technology[tech]().createEntry(username, password, db, table, query)
    def readEntry(self, tech, username, password, db, table, query):
        technology[tech]().readEntry(username, password, db, table, query)
    def updateEntry(self, tech, username, password, db, table, query, update):
        technology[tech]().updateEntry(username, password, db, table, query, update)
    def deleteEntry(self, tech, username, password, db, table, query):
        technology[tech]().deleteEntry(username, password, db, table, query)
