from docente import docente
from database import database

database_pe = database()
docente_1 = docente("Juan Pérez", "Las Aguas", "0911111111", "jperez@uide.edu.ec")
database_pe.cerrar()