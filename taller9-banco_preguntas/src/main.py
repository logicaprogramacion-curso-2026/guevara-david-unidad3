from database import database
from entidad  import entidad
from dao      import dao
# Punto de entrada del programa
# Reemplaza este archivo con tu código (o usa el lenguaje que corresponda al curso)

def main():
    print("Hola, este es el proyecto de David Guevara")
    basedatos = database()
    entidad_dao = dao(basedatos)

if __name__ == "__main__":
    main()
