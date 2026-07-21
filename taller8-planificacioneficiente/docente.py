class docente:
    def __init__(self, 
                 nombre,
                 direccion=None,
                 telefono=None,
                 correo=None):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        print("Constructor con argumentos")
