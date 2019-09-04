import sqlite3DB as DB

def testConstructorDefaultList():
    print("Checking database...")
    dbObj = DB.sqlite3DB()
    dbObj.initDB()
def testConstructorCustomList():
    print("Checking database...")
    dbObj = DB.sqlite3DB([("A", "AA"), ("B", "BB")])
    dbObj.initDB()

if __name__ == "__main__":
    # main()
    testConstructorCustomList()