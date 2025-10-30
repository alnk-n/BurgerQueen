def main():
    # import database
    import sqlite3
    #import homepage script from dashboards.py
    from dashboards import homePage

    # define I/O for database 
    con = sqlite3.connect("data/burgerqueen.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM sqlite_master")
    
    #run homepage script
    homePage(con, cursor)

    con.close()


if __name__ == "__main__":
   main()