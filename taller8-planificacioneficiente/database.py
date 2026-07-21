import sqlite3

class database:
    def __init__(self,
                 db_name="planificadoreficiente.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        print("Conexion exitosa")

    def cerrar(self):
        self.conn.close()