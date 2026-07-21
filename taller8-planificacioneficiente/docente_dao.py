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
