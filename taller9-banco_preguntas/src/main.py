# main.py
from database import database
from entidad import pregunta
from dao import dao
from respuesta_usuario_dao import RespuestaUsuarioDAO
from archivo import Archivo
from simulador import Simulador
import os

def mostrar_menu_principal():
    """Muestra el menú principal"""
    print("\n" + "="*50)
    print("SISTEMA DE GESTIÓN DE PREGUNTAS")
    print("="*50)
    print("1. Importar preguntas desde archivo")
    print("2. Exportar preguntas a archivo")
    print("3. Ver preguntas en la base de datos")
    print("4. Estadísticas de preguntas")
    print("5. Iniciar evaluación (SIMULADOR)")
    print("6. Ver historial de usuario")
    print("7. Ver ranking de usuarios")
    print("8. Exportar resultados de usuario")
    print("9. Salir")
    print("="*50)

def main():
    print("Hola, este es el proyecto de David Guevara")
    
    # Conectar a la base de datos
    basedatos = database()
    
    # Crear DAOs
    pregunta_dao = dao(basedatos)
    respuesta_dao = RespuestaUsuarioDAO(basedatos)
    
    # Crear tablas
    pregunta_dao.crear_tabla()
    respuesta_dao.crear_tabla()
    
    # Crear simulador
    simulador = Simulador(pregunta_dao, respuesta_dao)
    
    # Verificar archivos disponibles
    print("\nVerificando archivos disponibles:")
    archivos = ['preguntas_python.csv', 'preguntas_python.txt', 'preguntas_python.json']
    for archivo in archivos:
        if os.path.exists(archivo):
            print(f"  ✓ Archivo '{archivo}' encontrado")
        else:
            print(f"  ✗ Archivo '{archivo}' NO encontrado")
    
    while True:
        mostrar_menu_principal()
        opcion = input("Selecciona una opción (1-9): ").strip()
        
        if opcion == "1":  # IMPORTAR
            # ... (código de importación igual que antes) ...
            pass
        
        elif opcion == "2":  # EXPORTAR
            # ... (código de exportación igual que antes) ...
            pass
        
        elif opcion == "3":  # VER PREGUNTAS
            # ... (código de ver preguntas igual que antes) ...
            pass
        
        elif opcion == "4":  # ESTADÍSTICAS
            # ... (código de estadísticas igual que antes) ...
            pass
        
        elif opcion == "5":  # EVALUACIÓN
            total_preguntas = pregunta_dao.contar_preguntas()
            if total_preguntas == 0:
                print("\nNo hay preguntas en la base de datos. Importa preguntas primero.")
                continue
            
            usuario = input("Ingresa tu nombre de usuario: ").strip()
            if not usuario:
                print("El nombre de usuario no puede estar vacío.")
                continue
            
            print("\nFiltros opcionales (presiona Enter para omitir):")
            tema = input("Tema específico: ").strip()
            if not tema:
                tema = None
            
            dificultad = input("Dificultad (Fácil/Media/Difícil): ").strip()
            if dificultad not in ['Fácil', 'Media', 'Difícil']:
                dificultad = None
            
            try:
                cantidad = input("Número de preguntas (presiona Enter para todas): ").strip()
                if cantidad:
                    cantidad = int(cantidad)
                else:
                    cantidad = None
            except ValueError:
                cantidad = None
            
            resultados = simulador.iniciar_evaluacion(usuario, cantidad, tema, dificultad)
            
            if resultados:
                ver_detalles = input("\n¿Quieres ver los detalles de tus respuestas? (s/n): ").lower()
                if ver_detalles == 's':
                    print("\nDETALLES DE RESPUESTAS:")
                    print("-"*50)
                    for i, detalle in enumerate(resultados['detalles'], 1):
                        print(f"{i}. Pregunta ID: {detalle['id_pregunta']}")
                        print(f"   Tu respuesta: {detalle['respuesta']}")
                        print(f"   Correcta: {'✓' if detalle['es_correcta'] else '✗'}")
                        if not detalle['es_correcta']:
                            print(f"   Respuesta correcta: {detalle['respuesta_correcta']}")
                        print("-"*30)
        
        elif opcion == "6":  # HISTORIAL
            usuario = input("Ingresa el nombre de usuario: ").strip()
            if not usuario:
                print("El nombre de usuario no puede estar vacío.")
                continue
            
            estadisticas = simulador.ver_historial_usuario(usuario)
            
            if estadisticas['total'] == 0:
                print(f"\nEl usuario '{usuario}' no tiene respuestas registradas.")
        
        elif opcion == "7":  # RANKING
            try:
                limite = input("¿Cuántos usuarios quieres ver? (presiona Enter para 10): ").strip()
                if limite:
                    limite = int(limite)
                else:
                    limite = 10
                simulador.ver_top_usuarios(limite)
            except ValueError:
                print("Por favor, ingresa un número válido.")
        
        elif opcion == "8":  # EXPORTAR RESULTADOS
            usuario = input("Ingresa el nombre de usuario: ").strip()
            if not usuario:
                print("El nombre de usuario no puede estar vacío.")
                continue
            
            print("\nFormato de exportación:")
            print("1. TXT")
            print("2. CSV")
            print("3. JSON")
            formato_opcion = input("Selecciona formato (1-3): ").strip()
            
            formatos = {'1': 'txt', '2': 'csv', '3': 'json'}
            formato = formatos.get(formato_opcion, 'txt')
            
            simulador.exportar_resultados(usuario, formato)
        
        elif opcion == "9":  # SALIR
            print("\n¡Hasta luego!")
            break
        
        else:
            print("Opción no válida. Por favor, selecciona una opción del 1 al 9.")
    
    basedatos.cerrar()
    print("\nConexión cerrada.")

if __name__ == "__main__":
    main()