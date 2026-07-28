# dao.py
from entidad import pregunta

class dao:
    def __init__(self, db):
        self.db = db
    
    def crear_tabla(self):
        self.db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS preguntas (
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
        self.db.conn.commit()

    def insertar(self, pregunta_obj):
        """
        Inserta una pregunta en la base de datos
        
        Args:
            pregunta_obj: Objeto de tipo Pregunta
            
        Returns:
            int: ID de la pregunta insertada
        """
        self.db.cursor.execute('''
            INSERT INTO preguntas (pregunta,
                                 opcion_a, opcion_b, opcion_c, opcion_d,
                                 respuesta_correcta, dificultad, tema)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (pregunta_obj.pregunta, 
              pregunta_obj.opcion_a,
              pregunta_obj.opcion_b, 
              pregunta_obj.opcion_c,
              pregunta_obj.opcion_d, 
              pregunta_obj.respuesta_correcta,
              pregunta_obj.dificultad, 
              pregunta_obj.tema))
        self.db.conn.commit()
        return self.db.cursor.lastrowid
    
    def insertar_varios(self, preguntas_lista):
        """
        Inserta múltiples preguntas en la base de datos
        
        Args:
            preguntas_lista: Lista de objetos de tipo Pregunta
            
        Returns:
            list: Lista de IDs de las preguntas insertadas
        """
        ids = []
        for pregunta_obj in preguntas_lista:
            id_pregunta = self.insertar(pregunta_obj)
            ids.append(id_pregunta)
        return ids
    
    def obtener_todas(self):
        """
        Obtiene todas las preguntas de la base de datos
        
        Returns:
            list: Lista de objetos Pregunta
        """
        self.db.cursor.execute('SELECT * FROM preguntas')
        filas = self.db.cursor.fetchall()
        
        preguntas = []
        for fila in filas:
            pregunta_obj = pregunta(
                id=fila[0],
                pregunta=fila[1],
                opcion_a=fila[2],
                opcion_b=fila[3],
                opcion_c=fila[4],
                opcion_d=fila[5],
                respuesta_correcta=fila[6],
                dificultad=fila[7],
                tema=fila[8]
            )
            preguntas.append(pregunta_obj)
        
        return preguntas
    
    def obtener_por_id(self, id_pregunta):
        """
        Obtiene una pregunta por su ID
        
        Args:
            id_pregunta: ID de la pregunta
            
        Returns:
            Pregunta: Objeto Pregunta o None si no existe
        """
        self.db.cursor.execute('SELECT * FROM preguntas WHERE id = ?', (id_pregunta,))
        fila = self.db.cursor.fetchone()
        
        if fila:
            return pregunta(
                id=fila[0],
                pregunta=fila[1],
                opcion_a=fila[2],
                opcion_b=fila[3],
                opcion_c=fila[4],
                opcion_d=fila[5],
                respuesta_correcta=fila[6],
                dificultad=fila[7],
                tema=fila[8]
            )
        return None
    
    def contar_preguntas(self):
        """
        Cuenta el total de preguntas en la base de datos
        
        Returns:
            int: Número total de preguntas
        """
        self.db.cursor.execute('SELECT COUNT(*) FROM preguntas')
        return self.db.cursor.fetchone()[0]
    
    def eliminar_todas(self):
        """
        Elimina todas las preguntas de la base de datos
        """
        self.db.cursor.execute('DELETE FROM preguntas')
        self.db.conn.commit()