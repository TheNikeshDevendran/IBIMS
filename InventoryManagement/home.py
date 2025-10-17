import pyodbc
import pandas as pd
Connection=pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'server=NIKESH;'
                          'Database=Inventory;'
                          'Encrypt=no;'
                          'Trusted_Connection=yes;')
cursor=Connection.cursor()

vendors=cursor.execute("SELECT DISTINCT VendorName FROM Products;").fetchall()
for vendor in vendors:
    print(cursor.execute('select * from products where VendorName=?',vendor).fetchall())

            