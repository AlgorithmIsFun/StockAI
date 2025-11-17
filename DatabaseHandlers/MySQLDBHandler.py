from dotenv import load_dotenv
load_dotenv()
import os
import mysql.connector
from mysql.connector import Error
class databaseHandler:
    def __init__(self, host="localhost", port=3306):
        self.host = host
        self.port = port
        self.ADMIN_USER = os.getenv("ADMIN_USER")
        self.ADMIN_PASSWORD = os.getenv("ADMIN_PWD")

    def connect(self, username, password, database=None):
        return mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=username,
            password=password,
            database=database
        )
    """ USER MANAGEMENT """
    def createUser(self, username, password, role, db):
        try:
            conn = self.connect(self.ADMIN_USER, self.ADMIN_PASSWORD)
            cursor = conn.cursor()
            cursor.execute(f"CREATE USER '{username}'@'%' IDENTIFIED BY '{password}';")
            conn.commit()
            print(f"User {username} created.")
        except Error as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()

    def dropUser(self, username, db):
        try:
            conn = self.connect(self.ADMIN_USER, self.ADMIN_PASSWORD)
            cursor = conn.cursor()
            cursor.execute(f"DROP USER IF EXISTS '{username}'@'%';")
            conn.commit()
            print(f"User {username} dropped.")
        except Error as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()

    """ DATABASE MANAGEMENT """
    def createDatabase(self, username, password, db):
        try:
            conn = self.connect(self.ADMIN_USER, self.ADMIN_PASSWORD)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db};")
            conn.commit()
            print(f"Database {db} created.")
        except Error as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()

    def dropDatabase(self, username, password, db):
        try:
            conn = self.connect(self.ADMIN_USER, self.ADMIN_PASSWORD)
            cursor = conn.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {db};")
            conn.commit()
            print(f"Database {db} dropped.")
        except Error as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()

    """ TABLE MANAGEMENT """
    def createTable(self, username, password, db, table):
        try:
            conn = self.connect(username, password, db)
            cursor = conn.cursor()
            cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {table}(
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            data JSON
                        );
                    """)
            conn.commit()
            print(f"Table {table} created.")
        except Error as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()

    def dropTable(self, username, password, db, table):
        try:
            conn = self.connect(username, password, db)
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {table};")
            conn.commit()
            print(f"Table {table} dropped.")
        except Error as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()

    def listTable(self, username, password, db):
        try:
            conn = self.connect(username, password, db)
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            return [tbl[0] for tbl in tables]
        except Error as e:
            print("Error:", e)
            return []
        finally:
            cursor.close()
            conn.close()

    """ CRUD OPERATIONS """
    def createEntry(self, username, password, db, table, query):
        try:
            conn = self.connect(username, password, db)
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {table} (data) VALUES (%s)", [query])
            conn.commit()
            print("Entry created.")
        except Error as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()

    def readEntry(self, username, password, db, table, query):
        try:
            conn = self.connect(username, password, db)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM {table} WHERE id = %s", [query])
            return cursor.fetchone()
        except Error as e:
            print("Error:", e)
            return None
        finally:
            cursor.close()
            conn.close()
    def updateEntry(self, username, password, db, table, query, update):
        try:
            conn = self.connect(username, password, db)
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE {table} SET data = %s WHERE id = %s",
                [query, update]
            )
            conn.commit()
            print("Entry updated.")
        except Error as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()

    def deleteEntry(self, username, password, db, table, query):
        try:
            conn = self.connect(username, password, db)
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table} WHERE id = %s", [query])
            conn.commit()
            print("Entry deleted.")
        except Error as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()
