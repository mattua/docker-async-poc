import time
import sqlite3
from constants import database_name
from uuid import uuid4
import os

def init():
    os.remove(database_name)
    create_tables()
    
def create_tables():
    sql_statements = [ 
        """CREATE TABLE jobs (
                id VARCHAR PRIMARY KEY, 
                status NOT NULL
        );""",
        """CREATE TABLE runs (
                id VARCHAR PRIMARY KEY, 
                status NOT NULL
        );"""
        ]

    # create a database connection
    
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        for statement in sql_statements:
            cursor.execute(statement)
        
        conn.commit()
   
def insert_job(job_id):
    sqliteConnection = sqlite3.connect(database_name)
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    sqlite_insert_query = "INSERT INTO jobs (id, status) VALUES ('"+str(job_id)+"','pending')"
    cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()
    print("Record inserted successfully into table ", cursor.rowcount)
    cursor.close()

def insert_run(run_id):
    sqliteConnection = sqlite3.connect(database_name)
    cursor = sqliteConnection.cursor()
    sqlite_insert_query = "INSERT INTO runs (id, status) VALUES ('"+str(run_id)+"','pending')"
    cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()
    cursor.close()

def mark_run_complete():
    sqliteConnection = sqlite3.connect(database_name)
    cursor = sqliteConnection.cursor()
    # note the database is transient so we only expect one run
    sqlite_insert_query = "update runs set status = 'complete'"
    cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()
    cursor.close()

if __name__ == "__main__":
    init()
    insert_run(uuid4())
    for i in range(1,10):
        insert_job(uuid4())
        time.sleep(0.1)
    mark_run_complete()