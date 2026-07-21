from docente import docente

class docente_dao:
    def __init__(self, db):
        self.db = db
    
    def crear_tabla(self):
        self.db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS docente (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                direccion TEXT,
                telefono TEXT,
                correo TEXT
            )
        ''')

    def insertar(self, docente):
        self.db.cursor.execute('''
            INSERT INTO docente (nombre, direccion, telefono, correo)
            VALUES (?, ?, ?, ?)
        ''', (docente.nombre, docente.direccion, docente.telefono, docente.correo))
        self.db.conn.commit()
        return self.db.cursor.lastrowid
