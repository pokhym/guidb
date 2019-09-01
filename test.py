import sqlite3
import os.path
import tkinter

"""
    COLUMNS
"""

# create table with all the entries
def create_table(crsr):
    sql_command = """CREATE TABLE entries (  
staff_number INTEGER PRIMARY KEY,  
fname VARCHAR(20),  
lname VARCHAR(30),  
gender CHAR(1),  
joining DATE);"""
    crsr.execute(sql_command)

# initalize DB and check if it exists
def init_db():
    exists = os.path.exists("./collections.db")

    if exists:
        print("Database exists.")
    else:
        print("Database doesn't Exist.")

    # connect to db
    connection = sqlite3.connect("collections.db")
    crsr = connection.cursor()
    
    # check if a table exists
    sql_command = ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='entries' '''
    crsr.execute(sql_command)
    if crsr.fetchone()[0] == 1:
        print('Table exists.')
    # if it doesnt exist create the table
    else:
        print("Table does not exist, creating table.")
        create_table(crsr)

        sql_command = ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='entries' '''
        crsr.execute(sql_command)
        if crsr.fetchone()[0] == 1:
            print('Table now exists.')
        else:
            print("Failed to create new table!")
            exit(-1)

# main loop
def main():
    print("Checking database...")
    init_db()

if __name__ == "__main__":
    main()