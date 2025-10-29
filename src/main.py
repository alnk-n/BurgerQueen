def main():
    import sqlite3
    from dashboards import homePage

    con = sqlite3.connect("data/burgerqueen.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM sqlite_master")
    
    homePage(con, cursor)

    con.close()


if __name__ == "__main__":
   main()