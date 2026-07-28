# main.py
from database import database
from dao import dao
from archivo import Archivo
from entidad import pregunta 


def main():
    print("Hola, este es el proyecto de David Guevara")
    
    # Conectar a la base de datos
    basedatos = database()
    entidad_dao = dao(basedatos)
    
    # Crear la tabla si no existe
    entidad_dao.crear_tabla()
    
    # Preguntar qué tipo de archivo cargar
    print("\nSelecciona el tipo de archivo a cargar:")
    print("1. CSV (preguntas_python.csv)")
    print("2. TXT (preguntas_python.txt)")
    print("3. JSON (preguntas_python.json)")
    
    opcion = input("Ingresa el número de opción (1-3): ").strip()
    
    # Determinar el nombre del archivo según la opción
    archivos = {
        '1': 'preguntas_python.csv',
        '2': 'preguntas_python.txt',
        '3': 'preguntas_python.json'
    }
    
    nombre_archivo = archivos.get(opcion)
    
    if not nombre_archivo:
        print("Opción no válida. Usando CSV por defecto.")
        nombre_archivo = 'preguntas_python.csv'
    
    try:
        # Crear instancia del cargador de archivos
        cargador = Archivo(nombre_archivo)
        
        # Cargar las preguntas desde el archivo
        preguntas = cargador.cargar_preguntas()
        
        print(f"\nSe encontraron {len(preguntas)} preguntas en el archivo.")
        
        # Verificar si son objetos o diccionarios
        if preguntas and isinstance(preguntas[0], dict):
            # Si son diccionarios, convertirlos a objetos
            print("Convirtiendo diccionarios a objetos Pregunta...")
            preguntas_objetos = []
            for data in preguntas:
                nueva_pregunta = pregunta(
                    id=None,
                    pregunta=data['pregunta'],
                    opcion_a=data['opcion_a'],
                    opcion_b=data['opcion_b'],
                    opcion_c=data['opcion_c'],
                    opcion_d=data['opcion_d'],
                    respuesta_correcta=data['respuesta_correcta'],
                    dificultad=data['dificultad'],
                    tema=data['tema']
                )
                preguntas_objetos.append(nueva_pregunta)
        else:
            # Ya son objetos Pregunta
            preguntas_objetos = preguntas
        
        # Mostrar la primera pregunta como ejemplo
        if preguntas_objetos:
            print(f"\nEjemplo de la primera pregunta:")
            print(f"Pregunta: {preguntas_objetos[0].pregunta}")
            print(f"Opciones: A) {preguntas_objetos[0].opcion_a}, B) {preguntas_objetos[0].opcion_b}, C) {preguntas_objetos[0].opcion_c}, D) {preguntas_objetos[0].opcion_d}")
        
        # Usar el DAO para insertar las preguntas
        print("\nGuardando preguntas en la base de datos...")
        ids_insertados = entidad_dao.insertar_varios(preguntas_objetos)
        
        print(f"\n¡Proceso completado! Se guardaron {len(ids_insertados)} preguntas en la base de datos.")
        
        # Mostrar algunas estadísticas
        total_preguntas = entidad_dao.contar_preguntas()
        print(f"Total de preguntas en la base de datos: {total_preguntas}")
        
        # Opcional: Mostrar las primeras 5 preguntas guardadas
        if total_preguntas > 0:
            print("\nPrimeras 5 preguntas guardadas:")
            preguntas_guardadas = entidad_dao.obtener_todas()
            for i, p in enumerate(preguntas_guardadas[:5], 1):
                print(f"{i}. ID: {p.id} - {p.pregunta[:50]}...")
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Asegúrate de que el archivo exista en la carpeta del proyecto.")
    except Exception as e:
        print(f"\nError al procesar el archivo: {e}")
        import traceback
        traceback.print_exc()
    
    # Cerrar la conexión
    basedatos.cerrar()
    print("\nConexión cerrada.")

if __name__ == "__main__":
    main()