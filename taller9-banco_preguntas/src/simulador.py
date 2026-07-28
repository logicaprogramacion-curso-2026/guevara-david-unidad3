import random
import datetime

class Simulador:
    def __init__(self, pregunta_dao, respuesta_dao):
        """
        Inicializa el simulador con los DAOs
        
        Args:
            pregunta_dao: DAO para preguntas
            respuesta_dao: DAO para respuestas de usuarios
        """
        self.pregunta_dao = pregunta_dao
        self.respuesta_dao = respuesta_dao
    
    def iniciar_evaluacion(self, usuario, cantidad_preguntas=None, tema=None, dificultad=None):
        """
        Inicia una evaluación para un usuario
        """
        # Obtener todas las preguntas
        todas_preguntas = self.pregunta_dao.obtener_todas()
        
        if not todas_preguntas:
            print("No hay preguntas disponibles en la base de datos.")
            return None
        
        # Filtrar preguntas que el usuario ya respondió
        preguntas_respondidas_ids = self.respuesta_dao.obtener_preguntas_respondidas(usuario)
        preguntas_disponibles = [p for p in todas_preguntas if p.id not in preguntas_respondidas_ids]
        
        if not preguntas_disponibles:
            print(f"¡{usuario} ya respondió todas las preguntas disponibles!")
            return None
        
        # Filtrar por tema si se especifica
        if tema:
            preguntas_disponibles = [p for p in preguntas_disponibles if p.tema == tema]
        
        # Filtrar por dificultad si se especifica
        if dificultad:
            preguntas_disponibles = [p for p in preguntas_disponibles if p.dificultad == dificultad]
        
        if not preguntas_disponibles:
            print("No hay preguntas disponibles con los filtros seleccionados.")
            return None
        
        # Seleccionar cantidad de preguntas
        if cantidad_preguntas is None or cantidad_preguntas > len(preguntas_disponibles):
            cantidad_preguntas = len(preguntas_disponibles)
        
        # Mezclar y seleccionar
        preguntas_seleccionadas = random.sample(preguntas_disponibles, cantidad_preguntas)
        
        # Iniciar evaluación
        print(f"\n{'='*60}")
        print(f"INICIANDO EVALUACIÓN PARA {usuario.upper()}")
        print(f"Preguntas: {len(preguntas_seleccionadas)}")
        if tema:
            print(f"Tema: {tema}")
        if dificultad:
            print(f"Dificultad: {dificultad}")
        print(f"{'='*60}\n")
        
        respuestas = []
        correctas = 0
        
        for i, pregunta_obj in enumerate(preguntas_seleccionadas, 1):
            print(f"\nPregunta {i} de {len(preguntas_seleccionadas)}")
            print(f"ID: {pregunta_obj.id} | Dificultad: {pregunta_obj.dificultad} | Tema: {pregunta_obj.tema}")
            print(f"Pregunta: {pregunta_obj.pregunta}")
            print(f"A) {pregunta_obj.opcion_a}")
            print(f"B) {pregunta_obj.opcion_b}")
            print(f"C) {pregunta_obj.opcion_c}")
            print(f"D) {pregunta_obj.opcion_d}")
            
            # Validar respuesta
            respuesta_valida = False
            while not respuesta_valida:
                respuesta = input("Tu respuesta (A/B/C/D): ").strip().upper()
                if respuesta in ['A', 'B', 'C', 'D']:
                    respuesta_valida = True
                else:
                    print("Respuesta no válida. Ingresa A, B, C o D.")
            
            # Verificar si es correcta
            es_correcta = respuesta == pregunta_obj.respuesta_correcta
            if es_correcta:
                correctas += 1
            
            # Guardar respuesta usando el DAO de respuestas
            self.respuesta_dao.guardar_respuesta(
                pregunta_obj.id, 
                usuario, 
                respuesta, 
                es_correcta
            )
            
            # Mostrar feedback
            if es_correcta:
                print("✓ ¡Correcto!")
            else:
                print(f"✗ Incorrecto. La respuesta correcta era: {pregunta_obj.respuesta_correcta}")
            
            respuestas.append({
                'id_pregunta': pregunta_obj.id,
                'respuesta': respuesta,
                'es_correcta': es_correcta,
                'respuesta_correcta': pregunta_obj.respuesta_correcta
            })
        
        # Calcular resultados
        total = len(preguntas_seleccionadas)
        porcentaje = (correctas / total) * 100 if total > 0 else 0
        
        resultados = {
            'usuario': usuario,
            'total_preguntas': total,
            'correctas': correctas,
            'incorrectas': total - correctas,
            'porcentaje': porcentaje,
            'fecha': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'detalles': respuestas
        }
        
        # Mostrar resumen
        print(f"\n{'='*60}")
        print("RESULTADOS DE LA EVALUACIÓN")
        print(f"{'='*60}")
        print(f"Usuario: {usuario}")
        print(f"Total preguntas: {total}")
        print(f"Correctas: {correctas}")
        print(f"Incorrectas: {total - correctas}")
        print(f"Porcentaje de aciertos: {porcentaje:.1f}%")
        
        # Calificar
        if porcentaje >= 90:
            calificacion = "Excelente"
        elif porcentaje >= 70:
            calificacion = "Bueno"
        elif porcentaje >= 50:
            calificacion = "Regular"
        else:
            calificacion = "Necesita mejorar"
        
        print(f"Calificación: {calificacion}")
        print(f"{'='*60}")
        
        return resultados
    
    def ver_historial_usuario(self, usuario):
        """Muestra el historial de un usuario"""
        estadisticas = self.respuesta_dao.obtener_estadisticas_usuario(usuario)
        
        print(f"\n{'='*50}")
        print(f"HISTORIAL DE {usuario.upper()}")
        print(f"{'='*50}")
        print(f"Total preguntas respondidas: {estadisticas['total']}")
        print(f"Respuestas correctas: {estadisticas['correctas']}")
        print(f"Respuestas incorrectas: {estadisticas['incorrectas']}")
        print(f"Porcentaje de aciertos: {estadisticas['promedio']:.1f}%")
        
        # Mostrar estadísticas por tema
        estadisticas_tema = self.respuesta_dao.obtener_estadisticas_por_tema(usuario)
        if estadisticas_tema:
            print(f"\n--- Por Tema ---")
            for tema, stats in estadisticas_tema.items():
                print(f"  {tema}: {stats['correctas']}/{stats['total']} ({stats['porcentaje']:.1f}%)")
        
        # Mostrar estadísticas por dificultad
        estadisticas_dificultad = self.respuesta_dao.obtener_estadisticas_por_dificultad(usuario)
        if estadisticas_dificultad:
            print(f"\n--- Por Dificultad ---")
            for dificultad, stats in estadisticas_dificultad.items():
                print(f"  {dificultad}: {stats['correctas']}/{stats['total']} ({stats['porcentaje']:.1f}%)")
        
        # Mostrar respuestas recientes
        respuestas = self.respuesta_dao.obtener_respuestas_usuario(usuario)
        if respuestas:
            print(f"\nÚltimas 5 respuestas:")
            for r in respuestas[:5]:
                print(f"  ID Pregunta: {r.id_pregunta} | Respuesta: {r.respuesta_seleccionada} | Correcta: {'✓' if r.es_correcta else '✗'}")
        
        print(f"{'='*50}")
        
        return estadisticas
    
    def exportar_resultados(self, usuario, formato='txt'):
        """Exporta los resultados de un usuario"""
        nombre_archivo = self.respuesta_dao.exportar_resultados_usuario(usuario, formato)
        if nombre_archivo:
            print(f"\n✓ Resultados exportados a: {nombre_archivo}")
        else:
            print(f"\n✗ No hay resultados para exportar del usuario {usuario}")
        return nombre_archivo
    
    def ver_top_usuarios(self, limite=10):
        """Muestra los mejores usuarios"""
        top = self.respuesta_dao.obtener_top_usuarios(limite)
        
        if not top:
            print("\nNo hay suficientes datos para mostrar el ranking.")
            return
        
        print(f"\n{'='*50}")
        print("TOP USUARIOS")
        print(f"{'='*50}")
        print(f"{'#':<3} {'Usuario':<20} {'Aciertos':<10} {'Total':<10} {'Promedio':<10}")
        print("-"*50)
        
        for i, usuario in enumerate(top, 1):
            print(f"{i:<3} {usuario['usuario']:<20} {usuario['correctas']:<10} {usuario['total']:<10} {usuario['promedio']:.1f}%")
        
        print(f"{'='*50}")