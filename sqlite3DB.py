import sqlite3
import os

DEFAULT_NAME_COLUMNTYPE = [("staff_number", "INTEGER PRIMARY KEY"),\
("fname", "VARCHAR(20)"),\
    ("lname", "VARCHAR(30)"),\
        ("gender", "CHAR(1)"),\
            ("joining", "DATE")
]

class sqlite3DB:
    columnListType = []

    def __init__(self, columnListType=DEFAULT_NAME_COLUMNTYPE):
        self.columnListType = columnListType

    def initDB(self):
        """
            initDB
                Inputs:
                    None
                Output:
                    None
                Description:
                    Checks if a collections.db exists in the current directory if not it creates one
                    with default columns from createDefaultTable.  This function should be called
                    when the program is launched
        """
        exists = os.path.exists("./collections.db")

        if exists:
            print("Database exists.")
        else:
            print("Database doesn't Exist.")

        # connect to db
        connection = sqlite3.connect("collections.db")
        crsr = connection.cursor()
        
        # check if a table exists
        sql_command = ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Entries' '''
        crsr.execute(sql_command)
        if crsr.fetchone()[0] == 1:
            print('Table exists.')
        # if it doesnt exist create the table
        else:
            print("Table does not exist, creating table.")
            self.createDefaultTable(crsr)

            sql_command = ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Entries' '''
            crsr.execute(sql_command)
            if crsr.fetchone()[0] == 1:
                print('Table now exists.')
            else:
                print("Failed to create new table!")
                exit(-1)

    def parseNameColumnFromList(self, name_columntype):
        """
            parseNameColumnFromList
                Inputs:
                    name_columntype: A list of tuples, (name, type), which will be used to create comma sep
                    list for use in a SQL command such as CREATE TABLE ___ (<return value here>));
                Outputs:
                    nameColumnTypeStr: A string of flattened name and types
                Description:
                    This function creates a string of <name> <type>, ..., <name> <type>
        """
        assert len(name_columntype) >= 1

        nameColumnTypeStr = ""
        for tup in name_columntype:
            nameColumnTypeStr = nameColumnTypeStr + str(tup[0]) + " " + str(tup[1]) + ","
        
        # strip last comma
        nameColumnTypeStr = nameColumnTypeStr[:-1]
        return nameColumnTypeStr

    def createDefaultTable(self, crsr):
        """
            createDefaultTable
                Inputs:
                    crsr: Cursor into the DB
                Outputs:
                    None
                Description:
                    Creates and executes an sql command which creates a table called "Entries" with some
                    default columns.
        """
        sql_command = "CREATE TABLE Entries (" + self.parseNameColumnFromList(self.columnListType) + ");"
        crsr.execute(sql_command)

    def createConnection(self, dbFile):
        conn = None
        try:
            conn = sqlite3.connect(dbFile)
        except IOError as e:
            print(e)
        return conn

    # def createEntriesTable():
    # 