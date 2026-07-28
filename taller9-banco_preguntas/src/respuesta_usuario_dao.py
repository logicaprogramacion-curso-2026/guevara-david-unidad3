from respuesta_usuario import RespuestaUsuario
import datetime

class RespuestaUsuarioDAO:
    def __init__(self, db):
        self.db = db
    
    def crear_tabla(self):
        """Crea la tabla de respuestas de usuarios si no existe"""
        self.db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS respuestas_usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pregunta INTEGER,
                usuario TEXT,
                respuesta_seleccionada TEXT,
                es_correcta INTEGER,
                fecha_respuesta TEXT,
                FOREIGN KEY (id_pregunta) REFERENCES entidad(id)
            )
        ''')
        self.db.conn.commit()
    
    def guardar_respuesta(self, id_pregunta, usuario, respuesta_seleccionada, es_correcta):
        """
        Guarda la respuesta de un usuario
        
        Args:
            id_pregunta: ID de la pregunta
            usuario: Nombre del usuario
            respuesta_seleccionada: Opción seleccionada (A, B, C, D)
            es_correcta: Booleano indicando si es correcta
        
        Returns:
            int: ID de la respuesta guardada
        """
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.cursor.execute('''
            INSERT INTO respuestas_usuario 
            (id_pregunta, usuario, respuesta_seleccionada, es_correcta, fecha_respuesta)
            VALUES (?, ?, ?, ?, ?)
        ''', (id_pregunta, usuario, respuesta_seleccionada, 1 if es_correcta else 0, fecha))
        self.db.conn.commit()
        return self.db.cursor.lastrowid
    
    def guardar_respuestas(self, respuestas_lista):
        """
        Guarda múltiples respuestas de un usuario
        
        Args:
            respuestas_lista: Lista de tuplas (id_pregunta, usuario, respuesta_seleccionada, es_correcta)
        
        Returns:
            list: Lista de IDs de las respuestas guardadas
        """
        ids = []
        for respuesta in respuestas_lista:
            id_pregunta, usuario, respuesta_seleccionada, es_correcta = respuesta
            id_respuesta = self.guardar_respuesta(id_pregunta, usuario, respuesta_seleccionada, es_correcta)
            ids.append(id_respuesta)
        return ids
    
    def obtener_respuestas_usuario(self, usuario):
        """
        Obtiene todas las respuestas de un usuario
        
        Args:
            usuario: Nombre del usuario
        
        Returns:
            list: Lista de objetos RespuestaUsuario
        """
        self.db.cursor.execute('''
            SELECT * FROM respuestas_usuario WHERE usuario = ? ORDER BY fecha_respuesta DESC
        ''', (usuario,))
        filas = self.db.cursor.fetchall()
        
        respuestas = []
        for fila in filas:
            respuesta = RespuestaUsuario(
                id=fila[0],
                id_pregunta=fila[1],
                usuario=fila[2],
                respuesta_seleccionada=fila[3],
                es_correcta=bool(fila[4]),
                fecha_respuesta=fila[5]
            )
            respuestas.append(respuesta)
        return respuestas
    
    def obtener_respuesta_por_pregunta(self, id_pregunta, usuario):
        """
        Obtiene la respuesta de un usuario para una pregunta específica
        
        Args:
            id_pregunta: ID de la pregunta
            usuario: Nombre del usuario
        
        Returns:
            RespuestaUsuario: Objeto RespuestaUsuario o None si no existe
        """
        self.db.cursor.execute('''
            SELECT * FROM respuestas_usuario 
            WHERE id_pregunta = ? AND usuario = ?
        ''', (id_pregunta, usuario))
        fila = self.db.cursor.fetchone()
        
        if fila:
            return RespuestaUsuario(
                id=fila[0],
                id_pregunta=fila[1],
                usuario=fila[2],
                respuesta_seleccionada=fila[3],
                es_correcta=bool(fila[4]),
                fecha_respuesta=fila[5]
            )
        return None
    
    def obtener_preguntas_respondidas(self, usuario):
        """
        Obtiene los IDs de preguntas que ya respondió un usuario
        
        Args:
            usuario: Nombre del usuario
        
        Returns:
            list: Lista de IDs de preguntas
        """
        self.db.cursor.execute('''
            SELECT DISTINCT id_pregunta FROM respuestas_usuario WHERE usuario = ?
        ''', (usuario,))
        filas = self.db.cursor.fetchall()
        return [fila[0] for fila in filas]
    
    def obtener_estadisticas_usuario(self, usuario):
        """
        Obtiene estadísticas de un usuario
        
        Args:
            usuario: Nombre del usuario
        
        Returns:
            dict: Diccionario con estadísticas
        """
        self.db.cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(es_correcta) as correctas,
                AVG(es_correcta) as promedio
            FROM respuestas_usuario 
            WHERE usuario = ?
        ''', (usuario,))
        fila = self.db.cursor.fetchone()
        
        if fila and fila[0] > 0:
            total = fila[0]
            correctas = fila[1] or 0
            return {
                'total': total,
                'correctas': correctas,
                'incorrectas': total - correctas,
                'promedio': (fila[2] or 0) * 100
            }
        return {'total': 0, 'correctas': 0, 'incorrectas': 0, 'promedio': 0}
    
    def obtener_estadisticas_por_tema(self, usuario):
        """
        Obtiene estadísticas de un usuario agrupadas por tema
        
        Args:
            usuario: Nombre del usuario
        
        Returns:
            dict: Diccionario con estadísticas por tema
        """
        self.db.cursor.execute('''
            SELECT 
                e.tema,
                COUNT(*) as total,
                SUM(r.es_correcta) as correctas
            FROM respuestas_usuario r
            JOIN entidad e ON r.id_pregunta = e.id
            WHERE r.usuario = ?
            GROUP BY e.tema
        ''', (usuario,))
        filas = self.db.cursor.fetchall()
        
        estadisticas = {}
        for fila in filas:
            tema = fila[0] or 'Sin especificar'
            total = fila[1]
            correctas = fila[2] or 0
            estadisticas[tema] = {
                'total': total,
                'correctas': correctas,
                'incorrectas': total - correctas,
                'porcentaje': (correctas / total * 100) if total > 0 else 0
            }
        return estadisticas
    
    def obtener_estadisticas_por_dificultad(self, usuario):
        """
        Obtiene estadísticas de un usuario agrupadas por dificultad
        
        Args:
            usuario: Nombre del usuario
        
        Returns:
            dict: Diccionario con estadísticas por dificultad
        """
        self.db.cursor.execute('''
            SELECT 
                e.dificultad,
                COUNT(*) as total,
                SUM(r.es_correcta) as correctas
            FROM respuestas_usuario r
            JOIN entidad e ON r.id_pregunta = e.id
            WHERE r.usuario = ?
            GROUP BY e.dificultad
        ''', (usuario,))
        filas = self.db.cursor.fetchall()
        
        estadisticas = {}
        for fila in filas:
            dificultad = fila[0] or 'Sin especificar'
            total = fila[1]
            correctas = fila[2] or 0
            estadisticas[dificultad] = {
                'total': total,
                'correctas': correctas,
                'incorrectas': total - correctas,
                'porcentaje': (correctas / total * 100) if total > 0 else 0
            }
        return estadisticas
    
    def eliminar_respuestas_usuario(self, usuario):
        """
        Elimina todas las respuestas de un usuario
        
        Args:
            usuario: Nombre del usuario
        
        Returns:
            int: Número de respuestas eliminadas
        """
        self.db.cursor.execute('DELETE FROM respuestas_usuario WHERE usuario = ?', (usuario,))
        self.db.conn.commit()
        return self.db.cursor.rowcount
    
    def contar_respuestas_totales(self):
        """
        Cuenta el total de respuestas en la base de datos
        
        Returns:
            int: Número total de respuestas
        """
        self.db.cursor.execute('SELECT COUNT(*) FROM respuestas_usuario')
        return self.db.cursor.fetchone()[0]
    
    def obtener_top_usuarios(self, limite=10):
        """
        Obtiene los usuarios con mejor rendimiento
        
        Args:
            limite: Número de usuarios a mostrar
        
        Returns:
            list: Lista de tuplas (usuario, promedio, total)
        """
        self.db.cursor.execute('''
            SELECT 
                usuario,
                AVG(es_correcta) as promedio,
                COUNT(*) as total,
                SUM(es_correcta) as correctas
            FROM respuestas_usuario
            GROUP BY usuario
            HAVING COUNT(*) >= 5
            ORDER BY promedio DESC
            LIMIT ?
        ''', (limite,))
        
        resultados = []
        for fila in self.db.cursor.fetchall():
            resultados.append({
                'usuario': fila[0],
                'promedio': (fila[1] or 0) * 100,
                'total': fila[2],
                'correctas': fila[3] or 0
            })
        return resultados
    
    def exportar_resultados_usuario(self, usuario, formato='txt'):
        """
        Exporta los resultados de un usuario a un archivo
        
        Args:
            usuario: Nombre del usuario
            formato: 'txt', 'csv' o 'json'
        
        Returns:
            str: Nombre del archivo generado
        """
        import os
        import json
        import csv
        
        # Crear directorio de resultados si no existe
        os.makedirs('resultados', exist_ok=True)
        
        respuestas = self.obtener_respuestas_usuario(usuario)
        estadisticas = self.obtener_estadisticas_usuario(usuario)
        
        if not respuestas:
            return None
        
        fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if formato == 'txt':
            nombre_archivo = f"resultados/{usuario}_resultados_{fecha}.txt"
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write(f"RESULTADOS DE {usuario.upper()}\n")
                f.write("="*50 + "\n")
                f.write(f"Total preguntas: {estadisticas['total']}\n")
                f.write(f"Correctas: {estadisticas['correctas']}\n")
                f.write(f"Incorrectas: {estadisticas['incorrectas']}\n")
                f.write(f"Porcentaje: {estadisticas['promedio']:.1f}%\n")
                f.write("\nDETALLES DE RESPUESTAS:\n")
                f.write("-"*50 + "\n")
                for r in respuestas:
                    f.write(f"Pregunta ID: {r.id_pregunta}\n")
                    f.write(f"Respuesta: {r.respuesta_seleccionada}\n")
                    f.write(f"Correcta: {'SI' if r.es_correcta else 'NO'}\n")
                    f.write(f"Fecha: {r.fecha_respuesta}\n")
                    f.write("-"*30 + "\n")
        
        elif formato == 'csv':
            nombre_archivo = f"resultados/{usuario}_resultados_{fecha}.csv"
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID Pregunta', 'Respuesta Seleccionada', 'Es Correcta', 'Fecha'])
                for r in respuestas:
                    writer.writerow([
                        r.id_pregunta,
                        r.respuesta_seleccionada,
                        'SI' if r.es_correcta else 'NO',
                        r.fecha_respuesta
                    ])
        
        elif formato == 'json':
            nombre_archivo = f"resultados/{usuario}_resultados_{fecha}.json"
            data = {
                'usuario': usuario,
                'estadisticas': estadisticas,
                'respuestas': [
                    {
                        'id_pregunta': r.id_pregunta,
                        'respuesta_seleccionada': r.respuesta_seleccionada,
                        'es_correcta': r.es_correcta,
                        'fecha_respuesta': r.fecha_respuesta
                    }
                    for r in respuestas
                ]
            }
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        return nombre_archivo