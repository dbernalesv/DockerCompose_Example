# Importar Flask para crear aplicación web y jsonify para convertir objetos de Python a JSON
from flask import Flask, jsonify
# Importar PyMongo para interactuar con la base de datos MongoDB
from flask_pymongo import PyMongo

# Configuración inicial de Flask
app = Flask(__name__)

# Configuración de la base de datos: establecer la URI de conexión con MongoDB
app.config["MONGO_URI"] = "mongodb://diego:password@localhost:27017/miapp?authSource=admin"
# Inicializar PyMongo con la configuración actual de la aplicación Flask
mongo = PyMongo(app)

# Definición de la clase Animal
class Animal:
    def __init__(self, tipo, estado, _id=None):  # Constructor de la clase
        self.tipo = tipo  # Tipo de animal, por ejemplo: 'perro'
        self.estado = estado  # Estado del animal, por ejemplo: 'saludable'
        self._id = _id  # ID del documento de MongoDB, opcional en la creación

    @staticmethod
    def find():
        # Método estático para encontrar todos los animales en la base de datos y convertirlos a instancias de Animal
        return [Animal(**doc) for doc in mongo.db.animals.find()]

    @staticmethod
    def create(tipo, estado):
        # Método estático para crear un nuevo animal en la base de datos
        mongo.db.animals.insert_one({'tipo': tipo, 'estado': estado})

# Definición de rutas Flask
@app.route('/')
def list_animals():
    # Función para listar todos los animales
    animales = Animal.find()
    # Convertir las instancias de Animal en diccionarios para la respuesta JSON
    return jsonify([{'tipo': animal.tipo, 'estado': animal.estado} for animal in animales])

@app.route('/crear')
def create_animal():
    # Función para crear un nuevo animal con valores predefinidos
    Animal.create('perro', 'test')
    # Devolvemos una respuesta simple para indicar que la operación fue exitosa
    return 'ok'

# Punto de entrada principal de la aplicación Flask
if __name__ == '__main__':
    # Ejecutamos la aplicación en el puerto 3000 y habilitamos el modo de depuración para el desarrollo
    app.run(port=3000, debug=True)






