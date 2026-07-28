import csv
import json
import os
from entidad import pregunta 

class Archivo:
    def __init__(self, ruta_archivo):
        """
        Inicializa el cargador de archivos
        
        Args:
            ruta_archivo (str): Ruta al archivo a cargar
        """
        self.ruta_archivo = ruta_archivo
        self.extension = self._obtener_extension()
    
    def _obtener_extension(self):
        """Obtiene la extensión del archivo"""
        return os.path.splitext(self.ruta_archivo)[1].lower()

    def _detectar_codificacion(self):
        """Detecta la codificación del archivo"""
        codificaciones = ['utf-8-sig', 'utf-8', 'latin-1', 'windows-1252', 'iso-8859-1']
        
        for encoding in codificaciones:
            try:
                with open(self.ruta_archivo, 'r', encoding=encoding) as f:
                    f.read()
                return encoding
            except UnicodeDecodeError:
                continue
        
        # Si ninguna funciona, usar latin-1 por defecto
        return 'latin-1'
    
    def cargar_preguntas(self):
        """
        Carga las preguntas según la extensión del archivo
        
        Returns:
            list: Lista de diccionarios con los datos de las preguntas
            
        Raises:
            ValueError: Si el formato no es soportado
            FileNotFoundError: Si el archivo no existe
        """
        if self.extension == '.csv':
            return self._cargar_desde_csv()
        elif self.extension == '.txt':
            return self._cargar_desde_txt()
        elif self.extension == '.json':
            return self._cargar_desde_json()
        else:
            raise ValueError(f"Formato no soportado: {self.extension}. Use .csv, .txt o .json")
    
    def _cargar_desde_csv(self):
        """Carga preguntas desde un archivo CSV"""
        preguntas = []

        encoding = self._detectar_codificacion()
        print(f"Detectada codificación: {encoding}")
        
        try:
            with open(self.ruta_archivo, 'r', encoding=encoding) as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    pregunta = {
                        'pregunta': row.get('Pregunta', ''),
                        'opcion_a': row.get('OpcionA', ''),
                        'opcion_b': row.get('OpcionB', ''),
                        'opcion_c': row.get('OpcionC', ''),
                        'opcion_d': row.get('OpcionD', ''),
                        'respuesta_correcta': row.get('RespuestaCorrecta', ''),
                        'dificultad': row.get('Dificultad', ''),
                        'tema': row.get('Tema', '')
                    }
                    preguntas.append(pregunta)
            
            return preguntas
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Archivo CSV no encontrado: {self.ruta_archivo}")
        except Exception as e:
            raise Exception(f"Error al leer archivo CSV: {e}")
    
    def _cargar_desde_txt(self):
        """Carga preguntas desde un archivo TXT"""
        preguntas = []

        encoding = self._detectar_codificacion()
        print(f"Detectada codificación: {encoding}")        
        
        try:
            with open(self.ruta_archivo, 'r', encoding=encoding) as file:
                lineas = file.readlines()
                
                # Saltar la primera línea si es encabezado
                start_idx = 0
                if lineas and ('Pregunta' in lineas[0] or 'ID' in lineas[0]):
                    start_idx = 1
                
                for linea in lineas[start_idx:]:
                    if linea.strip():  # Ignorar líneas vacías
                        # Intentar parsear como CSV simple (separado por comas)
                        partes = linea.strip().split(',')
                        
                        # Si no tiene suficientes partes, intentar con tabulador
                        if len(partes) < 3:
                            partes = linea.strip().split('\t')
                        
                        # Intentar diferentes formatos de TXT
                        if len(partes) >= 3:
                            # Formato: ID,Pregunta,RespuestaCorrecta,Dificultad,Tema,Opciones
                            pregunta = {
                                'pregunta': partes[1] if len(partes) > 1 else partes[0],
                                'opcion_a': partes[2] if len(partes) > 2 else '',
                                'opcion_b': partes[3] if len(partes) > 3 else '',
                                'opcion_c': partes[4] if len(partes) > 4 else '',
                                'opcion_d': partes[5] if len(partes) > 5 else '',
                                'respuesta_correcta': partes[2] if len(partes) > 2 else '',
                                'dificultad': partes[3] if len(partes) > 3 else 'Media',
                                'tema': partes[4] if len(partes) > 4 else 'General'
                            }
                            preguntas.append(pregunta)
                        else:
                            # Formato simple: Pregunta|OpcionA|OpcionB|OpcionC|OpcionD|Respuesta
                            partes = linea.strip().split('|')
                            if len(partes) >= 6:
                                pregunta = {
                                    'pregunta': partes[0],
                                    'opcion_a': partes[1],
                                    'opcion_b': partes[2],
                                    'opcion_c': partes[3],
                                    'opcion_d': partes[4],
                                    'respuesta_correcta': partes[5],
                                    'dificultad': partes[6] if len(partes) > 6 else 'Media',
                                    'tema': partes[7] if len(partes) > 7 else 'General'
                                }
                                preguntas.append(pregunta)
            
            if not preguntas:
                raise Exception("No se encontraron preguntas en el archivo TXT")
            
            return preguntas
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Archivo TXT no encontrado: {self.ruta_archivo}")
        except Exception as e:
            raise Exception(f"Error al leer archivo TXT: {e}")
    
    def _cargar_desde_json(self):
        """Carga preguntas desde un archivo JSON con detección de codificación"""
        preguntas = []
        encoding = self._detectar_codificacion()
        print(f"Detectada codificación: {encoding}")
        
        try:
            with open(self.ruta_archivo, 'r', encoding=encoding) as file:
                data = json.load(file)
                
                # Buscar las preguntas en diferentes estructuras posibles
                items = []
                
                # Caso 1: El JSON tiene la estructura con "cuestionario"
                if isinstance(data, dict) and 'cuestionario' in data:
                    cuestionario = data['cuestionario']
                    if 'preguntas' in cuestionario:
                        items = cuestionario['preguntas']
                    else:
                        items = [cuestionario]
                
                # Caso 2: El JSON tiene directamente "preguntas"
                elif isinstance(data, dict) and 'preguntas' in data:
                    items = data['preguntas']
                
                # Caso 3: El JSON es un array directamente
                elif isinstance(data, list):
                    items = data
                
                else:
                    raise ValueError("Formato JSON no válido. Estructuras soportadas: "
                                   "{'cuestionario': {'preguntas': [...]}}, "
                                   "{'preguntas': [...]}, "
                                   "o directamente un array [...]")
                
                print(f"Se encontraron {len(items)} preguntas en el JSON")
                
                for item in items:
                    # Extraer la pregunta
                    pregunta_texto = item.get('pregunta', item.get('Pregunta', ''))
                    
                    # Extraer opciones (pueden estar en diferentes formatos)
                    opciones = item.get('opciones', {})
                    if isinstance(opciones, dict):
                        opcion_a = opciones.get('A', opciones.get('a', ''))
                        opcion_b = opciones.get('B', opciones.get('b', ''))
                        opcion_c = opciones.get('C', opciones.get('c', ''))
                        opcion_d = opciones.get('D', opciones.get('d', ''))
                    else:
                        # Si no hay opciones anidadas, buscar directamente
                        opcion_a = item.get('opcion_a', item.get('OpcionA', ''))
                        opcion_b = item.get('opcion_b', item.get('OpcionB', ''))
                        opcion_c = item.get('opcion_c', item.get('OpcionC', ''))
                        opcion_d = item.get('opcion_d', item.get('OpcionD', ''))
                    
                    respuesta = (item.get('respuesta_correcta') or 
                                item.get('RespuestaCorrecta') or 
                                item.get('respuesta') or 
                                item.get('Respuesta') or '')
                    
                    dificultad = (item.get('dificultad') or 
                                 item.get('Dificultad') or 
                                 'Media')
                    
                    tema = (item.get('tema') or 
                           item.get('Tema') or 
                           'General')
                    
                    # Solo agregar si tiene al menos una pregunta
                    if pregunta_texto:
                        # Crear objeto Pregunta
                        p = pregunta(
                            id=None,
                            pregunta=pregunta_texto,
                            opcion_a=opcion_a,
                            opcion_b=opcion_b,
                            opcion_c=opcion_c,
                            opcion_d=opcion_d,
                            respuesta_correcta=respuesta,
                            dificultad=dificultad,
                            tema=tema
                        )
                        preguntas.append(p)
                    else:
                        print(f"Advertencia: Se encontró un ítem sin pregunta: {item}")
            
            if not preguntas:
                raise Exception("No se encontraron preguntas en el archivo JSON")
            
            print(f"Se cargaron {len(preguntas)} preguntas correctamente")
            return preguntas
            
        except json.JSONDecodeError as e:
            raise Exception(f"Error al decodificar JSON: {e}")
        except Exception as e:
            raise Exception(f"Error al leer archivo JSON: {e}")

    def _exportar_a_txt(self, preguntas, nombre_archivo):
        with open(nombre_archivo, 'w') as f:
            for p in preguntas:
                f.write(f"{p.pregunta}|{p.opcion_a}|{p.opcion_b}|{p.opcion_c}|{p.opcion_d}|{p.respuesta_correcta}|{p.dificultad}|{p.tema}\n")

    def _exportar_a_csv(self, preguntas, nombre_archivo):
        with open(nombre_archivo, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Pregunta', 'Opción A', 'Opción B', 'Opción C', 'Opción D', 'Respuesta Correcta', 'Dificultad', 'Tema'])
            for p in preguntas:
                writer.writerow([p.pregunta, p.opcion_a, p.opcion_b, p.opcion_c, p.opcion_d, p.respuesta_correcta, p.dificultad, p.tema])

    def _exportar_a_json(self, preguntas, nombre_archivo):
        with open(nombre_archivo, 'w') as f:
            json.dump([p.__dict__ for p in preguntas], f)

