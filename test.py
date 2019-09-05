import sqlite3DB as DB

def testConstructorDefaultList():
    print("Checking database...")
    dbObj = DB.sqlite3DB()
    dbObj.createNewEntryInTable("Entries", [2, "c", "d", "f", 1111])
    dbObj.getAll_entries()

def testConstructorCustomList():
    print("Checking database...")
    dbObj = DB.sqlite3DB([("A", "AA"), ("B", "BB")])
    # dbObj = DB.sqlite3DB([])

if __name__ == "__main__":
    # testConstructorCustomList()
    testConstructorDefaultList()