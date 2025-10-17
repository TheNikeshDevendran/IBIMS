import pyodbc
class DbInventory:
    
    def __init__(self):
        self.connection=None
        self.cursor=None

    def ConnectToDb(self):
        self.connection=pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'server=NIKESH;'
                          'Database=Inventory;'
                          'Encrypt=no;'
                          'Trusted_Connection=yes;')
        self.cursor=self.connection.cursor()
        return 'Connection established'

    def CloseDb(self):
