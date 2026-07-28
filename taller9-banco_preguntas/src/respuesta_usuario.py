class RespuestaUsuario:
    def __init__(self, id=None, id_pregunta=None, usuario=None, 
                 respuesta_seleccionada=None, es_correcta=None, 
                 fecha_respuesta=None):
        self.id = id
        self.id_pregunta = id_pregunta
        self.usuario = usuario
        self.respuesta_seleccionada = respuesta_seleccionada
        self.es_correcta = es_correcta
        self.fecha_respuesta = fecha_respuesta