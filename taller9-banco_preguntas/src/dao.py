from entidad import entidad

class dao:
    def __init__(self, db):
        self.db = db
    
    def crear_tabla(self):
        self.db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS entidad (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pregunta           TEXT NOT NULL,
                opcion_a           TEXT,
                opcion_b           TEXT,
                opcion_c           TEXT,
                opcion_d           TEXT,
                respuesta_correcta TEXT,
                dificultad         TEXT,
                tema               TEXT
            )
        ''')

    def insertar(self, docente):
        self.db.cursor.execute('''
            INSERT INTO entidad (pregunta,
                                 opcion_a, opcion_b, opcion_c, opcion_d,
                                 respuesta_correcta, dificultad, tema)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (docente.nombre, docente.direccion, 
              docente.telefono, docente.correo))
        self.db.conn.commit()
        return self.db.cursor.lastrowid
