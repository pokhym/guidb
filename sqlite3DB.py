import sqlite3
import os

DEFAULT_NAME_COLUMN_TYPE = [("staffnumber", "INTEGER PRIMARY KEY", "integer"),\
("fname", "VARCHAR(20)", "text"),\
    ("lname", "VARCHAR(30)", "text"),\
        ("gender", "CHAR(1)", "text"),\
            ("joining", "DATE", "text")
]

class sqlite3DB:
    # TODO: The input of columnListType is user input and thus there needs to be a function
    # which checks whether it is of the correct type using the sqlite3 function typeof()
    # this function probably needs to exist in this class
    # TODO: columnListType currently is set up for only one table. It might be produent to
    # allow it to be used for multiple tables
    dictColumnListType = {}
    conn = None

    def __init__(self, columnListType=DEFAULT_NAME_COLUMN_TYPE, tableName="Entries"):
        """
            __init__
                Inputs:
                    columnListType: Contains the names of columns and their types
                    tableName: A default table name to be used
                Output:
                    None
                Description:
                    Checks if a collections.db exists in the current directory if not it creates one
                    with default columns from createDefaultTable.  This function should be called
                    when the program is launched
        """
        self.dictColumnListType = {tableName: columnListType}

        exists = os.path.exists("./collections.db")

        if exists:
            print("[LOG] (init) Database exists.")
        else:
            print("[LOG] (init) Database doesn't Exist.")

        # connect to db
        self.conn = self.createConnection("collections.db")

        crsr = self.conn.cursor()
        
        # check if a table exists
        if self.tableExist("Entries"):
            print('[LOG] (init) Table exists.')
        # if it doesnt exist create the table
        else:
            print("[LOG] (init) Table does not exist, creating table.")
            self.createDefaultTable(crsr, tableName)

            sql_command = ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Entries' '''
            crsr.execute(sql_command)
            if crsr.fetchone()[0] == 1:
                print('[LOG] (init) Table now exists.')
            else:
                print("[ERROR] (init) Failed to create new table!")
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
            print("[ERROR] " + e)
        return conn
    
    def closeConnection(self):
        """
            closeConnection
                Inputs:
                    None
                Outputs:
                    None
                Description:
                    Commits all pending transactions and then closes the connection
        """
        self.conn.commit()
        self.conn.close()

    def getAll_entries(self):
        """
            getAll_entries
                Inputs:
                    None
                Outputs:
                    None
                Description:
                    Hardcoded to print every entry from the table Entries
        """
        cur = self.conn.cursor()
        with self.conn:
            cur.execute("SELECT * FROM Entries")
            print(cur.fetchall())
    
    def getEntryInTable(self):
        """
            #TODO: NEED TO FINISH
        """

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
    
    def parseNameFromList(self, name_columntype):
        """
            parseNameFromList
                Inputs:
                    name_columntype: name_columntype: A list of tuples, (name, type), which will be used to create comma sep
                    list for use in a SQL command such as CREATE TABLE ___ (<return value here>));
                Outputs:
                    nameColumnTypeStr: A new string containing only the comma separated names of the columns
                    in the table
        """
        # TODO: Change this to an if statement and a return gracefully
        assert len(name_columntype) >= 1

        nameColumnTypeStr = ""
        for tup in name_columntype:
            nameColumnTypeStr = nameColumnTypeStr + str(tup[0]) + ","
        
        # strip last comma
        nameColumnTypeStr = nameColumnTypeStr[:-1]
        return nameColumnTypeStr
    
    def createDefaultTable(self, crsr, tableName):
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
        sql_command = "CREATE TABLE Entries (" + self.parseNameColumnFromList(self.dictColumnListType[tableName]) + ");"
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
                    boolean: False if creation of new entry failed, True if succeeded
                    -1: Entry already exists
                    -2: Mismatch in # columns
                    -3: Table does not exist
                    0: Success
                Description:
                    Creates a new entry in the the table with tableName with parameters param
        """
        if self.tableExist(tableName) == False:
            print("[ERROR] (createNewEntryInTable) Table does not exist")
            return -4
        
        # TODO: Make sure this assert is turned into a graceful return condition
        assert len(param) == len(self.dictColumnListType[tableName])

        # https://stackoverflow.com/questions/2440147/how-to-check-the-existence-of-a-row-in-sqlite-with-python
        crsr = self.conn.cursor()
        crsr.execute("SELECT " + self.dictColumnListType[tableName][0][0] + \
            " FROM " + tableName + " WHERE " + self.dictColumnListType[tableName][0][0] + " = ?", [param[0]])
        data = crsr.fetchone()
        if data is None:
            print("[LOG] (createNewEntryInTable) Creating entry.")
        else:
            print("[LOG] (createNewEntryInTable) Entry already exists.")
            return -1 

        if len(param) == len(self.dictColumnListType[tableName]):
            sql_command = "INSERT INTO " + tableName + "(" + self.parseNameFromList(self.dictColumnListType[tableName]) + \
                ") VALUES(" + "?," * (len(self.dictColumnListType[tableName]) - 1) + "?" + ");"
        # fail condition
        else:
            print("[ERROR] (createNewEntryInTable) Failed to update entry in table due to mismatch in # columns: " + tableName)
            return -2
        crsr = self.conn.cursor()
        crsr.execute(sql_command, param)
        self.conn.commit()
        return 0

    def parseNameUpdateCommand(self, namelist):
        """
            parseNameUpdateCommand
                Inputs:
                    namelist: List of names (columns) we want to update
                Outputs:
                    A comma separated list of "name=?"
                Description:
                    This function creates an output string of columns with =?
        """
        outputStr = ""
        arrayOfNames = namelist
        # build new string
        for name in arrayOfNames:
            outputStr = outputStr + name + "=?,"
        outputStr = outputStr[:-1]
        return outputStr
    
    def updateEntryInTable(self, tableName, primaryKey, param, name):
        """
            updateEntryInTable
                Inputs:
                    tableName: table name to be updated
                    primaryKey: The primary key of the row we want to edit
                    param: List of parameters to be updated in the row
                    name: The list of the columns that we want to update parameters in
                Outputs:
                    boolean: False if update failed, True if succeeded
                    -1: Entry does not exist
                    -2: Some input columns in input do not exist in table
                    -3: Mismatch in # of columns
                    -4: Table Does not exist
                    0: Success
                Description:
                    Updates a specific entry in the table
        """
        # TODO: Make sure errors are gracefully handled in GUI

        if self.tableExist(tableName) == False:
            print("[ERROR] (updateEntryInTable) Table does not exist")
            return -4

        # make sure primary key exists
        # https://stackoverflow.com/questions/2440147/how-to-check-the-existence-of-a-row-in-sqlite-with-python
        crsr = self.conn.cursor()
        crsr.execute("SELECT " + self.dictColumnListType[tableName][0][0] + \
            " FROM " + tableName + " WHERE " + self.dictColumnListType[tableName][0][0] + " = ?", [primaryKey])
        data = crsr.fetchone()
        if data is None:
            print("[LOG] (updateEntryInTable) Entry does not exist.")
            return -1
        else:
            print("[LOG] (updateEntryInTable) Entry already exists.")

        # Make sure our names exist in the table's columns
        count = 0
        for n in name:
            for column in self.dictColumnListType[tableName]:
                if column[0] == n and self.dictColumnListType[tableName][0][0] == n:
                    print("[ERROR] (updateEntryInTable) You are trying to edit the primary key column.")
                    return False
                if column[0] == n:
                    count = count + 1
        if count == len(name):
            print("[LOG] (updateEntryInTable) All columns to be edited exist.")
        else:
            print("[ERROR] (updateEntryInTable) Some input columns do not exist.")
            return -2


        if len(param) <= len(self.dictColumnListType[tableName]):
            sql_command = "UPDATE " + tableName + " SET " + self.parseNameUpdateCommand(name) + " WHERE " + self.dictColumnListType[tableName][0][0] + " = " + str(primaryKey) + ";"
        else:
            print("[ERROR] (updateEntryInTable) Failed to update entry in table due to mismatch in # columns: " + tableName)
            return -3
        crsr = self.conn.cursor()
        crsr.execute(sql_command, param)
        self.conn.commit()
        return 0
    
    def removeEntryInTable(self, tableName, primaryKey):
        """
            removeEntryIntable
                Inputs:
                    tableName:
                    primaryKey:
                Outputs:
                    0: Remove worked
                    -1: Table does not exist
                    -2: Remove failed due to an entry not existing in table
                Description:
                    This function removes an entry in the table if it exists
        """
        # TODO: Make sure errors are gracefully handled in GUI
        if self.tableExist(tableName) == False:
            print("[ERROR] (removeEntryInTable) Table does not exist")
            return -1
        
        # make sure primary key exists
        # https://stackoverflow.com/questions/2440147/how-to-check-the-existence-of-a-row-in-sqlite-with-python
        crsr = self.conn.cursor()
        crsr.execute("SELECT " + self.dictColumnListType[tableName][0][0] + \
            " FROM " + tableName + " WHERE " + self.dictColumnListType[tableName][0][0] + " = ?", [primaryKey])
        data = crsr.fetchone()
        if data is None:
            print("[LOG] (removeEntryInTable) Entry does not exist.")
            return -2
        else:
            print("[LOG] (removeEntryInTable) Entry exists.")

        sql_command = "DELETE FROM " + tableName + " WHERE id=?"

        crsr.execute(sql_command)
        self.conn.commit()
        return 0