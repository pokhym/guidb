import sqlite3DB as DB

def test():
    print("Checking database...")
    dbObj = DB.sqlite3DB([("A", "AA"), "B", "BB"])
    dbObj.initDB()
    # dbObj.parseNameColumnFromList()

def main():
    print("Checking database...")
    dbObj = DB.sqlite3DB()
    dbObj.initDB()

if __name__ == "__main__":
    # main()
    test()