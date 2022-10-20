"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Usuario, Favoritos, Planeta, Personaje
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

########################
#     METODOS GET       #
########################

# METODO GET PARA OBTENER LOS USUARIOS
@app.route('/user', methods=['GET'])
def get_user():
    user= Usuario.query.all()
    result= list(map(lambda x: x.serialize(),user))
    print(result)
    
    return jsonify(result), 200

# METODO GET PARA OBTENER UN SOLO USUARIO
@app.route('/user/<int:id_character>', methods=['GET'])
def get_every_user(id_character):
    user= Usuario.query.filter_by(id=id_character).first()
    result= user.serialize()
    print(result)
    
    return jsonify(result), 200

# METODO GET PARA OBTENER PLANETAS
@app.route('/planets', methods=['GET'])
def get_planet():
    planet= Planeta.query.all()
    result= list(map(lambda x: x.serialize(),planet))
    print(result)
    
    return jsonify(result), 200

# METODO GET PARA OBTENER UN SOLO PLANETA
@app.route('/planets/<int:id_planet>', methods=['GET'])
def get_every_planet(id_planet):
    planet= Planeta.query.filter_by(id=id_planet).first()
    result= planet.serialize()
    print(result)
    
    return jsonify(result), 200

# METODO GET PARA OBTENER PERSONAJE
@app.route('/characters', methods=['GET'])
def get_personaje():
    personaje= Personaje.query.all()
    result= list(map(lambda x: x.serialize(),personaje))
    print(result)
    
    return jsonify(result), 200

# METODO GET PARA OBTENER UN SOLO PERSONAJE
@app.route('/characters/<int:id_characters>', methods=['GET'])
def get_every_character(id_characters):
    personaje= Personaje.query.filter_by(id=id_characters).first()
    result= personaje.serialize()
    print(result)
    
    return jsonify(result), 200

# METODO GET PARA OBTENER FAVORITO
@app.route('/favorites', methods=['GET'])
def get_favotites():
    favorito= Favoritos.query.all()
    result= list(map(lambda x: x.serialize(),favorito))
    print(result)
    
    return jsonify(result), 200

# METODO GET PARA OBTENER UN SOLO FAVORITO
@app.route('/favorites/<int:id_favorites>', methods=['GET'])
def get_every_favorite(id_favorites):
    favorito= Favoritos.query.filter_by(id=id_favorites).first()
    result= favorito.serialize()
    print(result)
    
    return jsonify(result), 200

########################
#      METODOS POST      #
########################

# METODO PARA HACER POST PARA UN USUARIO
@app.route('/usuario', methods=['POST'])
def new_person():

    # First we get the payload json
    body = json.loads(request.data)
    print(body)
    query_user = Usuario.query.filter_by(email=body["email"]).first()
    print(query_user)

    if query_user is None:
        #guardar datos recibidos a la tabla User
        new_user = Usuario(name=body["name"],last_name=body["last_name"],email=body["email"],password=body["password"])
        db.session.add(new_user)
        db.session.commit()
        response_body = {
                "msg": "created user"
            }

        return jsonify(response_body), 200

    response_body = {
            "msg": "existed user"
        }
    return jsonify(response_body), 400

# METODO PARA QUE ADMIN HAGA POST A UN PLANETA
@app.route('/planeta', methods=['POST'])
def new_planet():

    # First we get the payload json
    body = json.loads(request.data)
    print(body)
    query_user = Planeta.query.filter_by(name=body["name"]).first()
    print(query_user)

    if query_user is None:
        #guardar datos recibidos a la tabla User
        new_user = Planeta(name=body["name"],rotation_period=body["rotation_period"],orbital_period=body["orbital_period"],diameter=body["diameter"],gravity=body["gravity"])
        db.session.add(new_user)
        db.session.commit()
        response_body = {
                "msg": "created planet"
            }

        return jsonify(response_body), 200

    response_body = {
            "msg": "existed planet"
        }
    return jsonify(response_body), 400

# METODO PARA CREAR UN PLANETA FAVORTO NUEVO
@app.route('/favorite/planet/<int:user_id>/<int:planet_id>', methods=['POST'])
def favorite_planet(user_id, planet_id):

  
    user_id_favorites = Favoritos.query.filter_by(user_id=id_usuario).first()
    if user_id_favorites:
        # Control de planetas
        user_id_planets = Favoritos.query.filter_by(id_planeta=planet_id).first()
        if user_id_planets: 
            # Si este favorito ya existe
            response_body = {"msg": "Este usuario ya tiene a este planeta como favorito"}
            return jsonify(response_body), 400
        else: 
            #Si este planeta no lo tiene
            new_favorites = favorite_planet(id_usuario=user_id, id_planeta=planet_id)
        
            db.session.add(new_favorites)
            db.session.commit()
            
            response_body = {"msg": "Favorito creado" }
            return jsonify(response_body), 200
    else:
        # Ya existe ese planeta para ese usuario
        response_body = {"msg": "No existe el usuario"}
        return jsonify(response_body), 400



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
