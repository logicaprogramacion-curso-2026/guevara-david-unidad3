from docente import docente
from database import database
from docente_dao import docente_dao

database_pe = database()
docente_dao = docente_dao(database_pe)
docente_dao.crear_tabla()
#docente_1 = docente("Juan Pérez", "Las Aguas", "0911111111", "jperez@uide.edu.ec")
docente_dao.insertar(docente_1)
database_pe.cerrar()