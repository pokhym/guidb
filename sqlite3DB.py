import sqlite3
import os

DEFAULT_NAME_COLUMN_TYPE = [("staff_number", "INTEGER PRIMARY KEY", "integer"),\
("fname", "VARCHAR(20)", "text"),\
    ("lname", "VARCHAR(30)", "text"),\
        ("gender", "CHAR(1)", "text"),\
            ("joining", "DATE", "text")
]

class sqlite3DB:
    # TODO: The input of columnListType is user input and thus there needs to be a function
    # which checks whether it is of the correct type using the sqlite3 function typeof()
    # this function probably needs to exist in this class
    columnListType = []
    conn = None

    def __init__(self, columnListType=DEFAULT_NAME_COLUMN_TYPE):
        """
            __init__
                Inputs:
                    None
                Output:
                    None
                Description:
                    Checks if a collections.db exists in the current directory if not it creates one
                    with default columns from createDefaultTable.  This function should be called
                    when the program is launched
        """
        self.columnListType = columnListType

        exists = os.path.exists("./collections.db")

        if exists:
            print("Database exists.")
        else:
            print("Database doesn't Exist.")

        # connect to db
        self.conn = self.createConnection("collections.db")

        crsr = self.conn.cursor()
        
        # check if a table exists
        if self.tableExist("Entries"):
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

    def createConnection(self, dbFile):
        """
            createConnection
                Inputs:
                    dbFile: Database file path
                Outputs:
                    None
                Description:
                    Creates a connection to the database and returns the conn ob
        """
        conn = None
        try:
            conn = sqlite3.connect(dbFile)
        except IOError as e:
            print(e)
        return conn
    
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
        # TODO: Change this to an if statement and a return gracefully
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

    def tableExist(self, tableName):
        """
            tableExist
                Inputs:
                    tableName: A string which is the tableName we are checking for
                Outputs:
                    bool: True if table with tableName exists false o/w
                Description:
                    This function checks if a certain table exists in the database
        """
        crsr = self.conn.cursor()
        sql_command = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + tableName +"'"
        crsr.execute(sql_command)
        return crsr.fetchone()[0] == 1

    def createNewEntryInTable(self, tableName, param):
        """
            createEntriesTable
                inputs:
                    tableName: The table which we want to modify
                    param: A list of parameters for the table
                Outputs:
                    None
                Description:
                    Creates a new entry in the the table with tableName with parameters param
        """