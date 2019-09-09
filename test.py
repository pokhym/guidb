import sqlite3DB as DB

def testConstructorDefaultList():
    print("Checking database...")
    dbObj = DB.sqlite3DB()
    dbObj.createNewEntryInTable("Entries", [1, "a", "b", "f", 1111])
    dbObj.createNewEntryInTable("Entries", [2, "c", "d", "f", 2222])
    dbObj.updateEntryInTable("Entries", 2, ["fff", 3333], ["gender", "joining"])
    dbObj.updateEntryInTable("Entries", 2, ["fff", 3333], ["gender", "doesnotexist"])
    dbObj.getAll_entries()

def testConstructorCustomList():
    print("Checking database...")
    dbObj = DB.sqlite3DB([("A", "AA"), ("B", "BB")])
    # dbObj = DB.sqlite3DB([])

if __name__ == "__main__":
    # testConstructorCustomList()
    testConstructorDefaultList()