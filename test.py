import sqlite3DB as DB

def testConstructorDefaultList():
    print("Checking database...")
    dbObj = DB.sqlite3DB()

def testConstructorCustomList():
    print("Checking database...")
    dbObj = DB.sqlite3DB([("A", "AA"), ("B", "BB")])

if __name__ == "__main__":
    testConstructorCustomList()
    # testConstructorDefaultList()