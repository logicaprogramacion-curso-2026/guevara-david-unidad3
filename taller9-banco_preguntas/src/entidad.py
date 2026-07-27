class pregunta:
    def __init__(self, id=None, pregunta=None, opcion_a=None, opcion_b=None, opcion_c=None, opcion_d=None,
                       respuesta_correcta=None, dificultad=None, tema=None):
        self.id = id
        self.pregunta = pregunta
        self.opcion_a = opcion_a
        self.opcion_b = opcion_b
        self.opcion_c = opcion_c
        self.opcion_d = opcion_d
        self.respuesta_correcta = respuesta_correcta
        self.dificultad = dificultad #: str (Fácil, Media, Difícil)
        self.tema = tema