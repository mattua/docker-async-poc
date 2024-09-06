import time
import sqlite3
from constants import database_name,output_file_path
from uuid import uuid4
from random import random
from os import path


def init():
    pass
    #os.remove(output_file)

def get_pending_jobs():
    jobs = []
    try:
        with sqlite3.connect(database_name) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM jobs where status = 'pending'")
            rows = cur.fetchall()
            for row in rows:
                job_id = row[0]
                status = row[1]
                jobs.append((job_id,status))             
    except:
        pass
    return jobs

def mark_job_complete(job_id):
    sqliteConnection = sqlite3.connect(database_name)
    cursor = sqliteConnection.cursor()
    # note the database is transient so we only expect one run
    sqlite_insert_query = "update jobs set status = 'complete' where id = '"+job_id+"'"
    cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()
    cursor.close()

def is_run_complete():
    try:
        with sqlite3.connect(database_name) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM runs')
            status = cur.fetchall()[0][1]
            return status == "complete"
                
    except:
        return False
    
    
def get_response_for_job(job_id):
    records = []
    for i in range(1,10):

        record = {
            "assetId":uuid4(),
            "price": 95+random(),
            "yield": 4+random(),
            "spread": 30+random()
        }
        records.append(record)
    return records
    
def write_to_csv(records):

    csv_data = generate_csv_data(records)
    print(csv_data)

    write_to_file(csv_data,output_csv)

def generate_csv_data(data) -> str: 
  
    if not data:
        return ""
    # Defining CSV columns in a list to maintain 
    # the order 
    csv_columns = data[0].keys() 
  
    # Generate the first row of CSV  
    csv_data = ",".join(csv_columns) + "\n"
  
    for record in data:

    # Generate the single record present 
        new_row = list() 
        for col in csv_columns: 
            new_row.append(str(record[col])) 
    
        # Concatenate the record with the column information  
        # in CSV format 
        csv_data += ",".join(new_row) + "\n"
  
    return csv_data 
  
  
def write_to_file(data: str, filepath: str) -> bool: 
  
    try: 
        with open(filepath, "w+") as f: 
            f.write(data) 
    except: 
        raise Exception(f"Saving data to {filepath} encountered an error") 

def generate_output_file_name():
    return path.join(output_file_path,str(uuid4())+".txt")

output_csv=generate_output_file_name()


if __name__ == "__main__":

    init()
    all_records = []
    while True:
        time.sleep(0.5)
        jobs = get_pending_jobs()
        # producer has stated no more jobs coming and queue is empty, time to stop
        if len(jobs)==0 and is_run_complete():
            print("no more jobs")
            import sys
            write_to_csv(all_records)
            sys.exit(0)

        for job in jobs:
            records = get_response_for_job(job)
            all_records += records
            #print(records)
            time.sleep(0.1)
            mark_job_complete(job[0])
            
         