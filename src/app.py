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
from models import db, Planets, Characters, Vehicles, Favorites, User
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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

# --------------------------------MÉTODOS GET

@app.route('/user', methods=['GET'])
def get_user():
    all_user = User.query.all()
    result = [element.serialize() for element in all_user]
    response_body = {
        "msg": "Muy bien, obtuviste tus usuarios!",
        "user": result
    }
    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()
    result = [element.serialize() for element in all_planets]
    response_body = {
        "msg": "Muy bien, obtuviste tus planetas!",
        "planets": result
    }
    return jsonify(response_body), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    all_characters = Characters.query.all()
    result = [element.serialize() for element in all_characters]
    response_body = {
        "msg": "Muy bien, obtuviste tus personajes!",
        "characters": result
    }
    return jsonify(response_body), 200

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    all_vehicles = Vehicles.query.all()
    result = [element.serialize() for element in all_vehicles]
    response_body = {
        "msg": "Muy bien, obtuviste tus vehiculos!",
        "vehicles": result
    }
    return jsonify(response_body), 200

@app.route('/favorites', methods=['GET'])
def get_favorites():
    all_favorites = Favorites.query.all()
    result = [element.serialize() for element in all_favorites]
    response_body = {
        "msg": "Muy bien, obtuviste tus Favoritos!",
        "favorites": result
    }
    return jsonify(response_body), 200

# ------------------------------------------MÉTODOS GET POR ID-
@app.route('/users/<int:users_id>', methods=['GET'])
def get_users_id(users_id):
    un_user = User.query.get(users_id)
    result = un_user.serialize()
    response_body = {"msg": "Usuario recibido",
                     "users": result}
    return jsonify(response_body), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planets_id(planets_id):
    un_planet= Planets.query.get(planets_id)
    result= un_planet.serialize()
    response_body = {"msg": "Planeta recibido",
                     "planets": result}
    return jsonify(response_body), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_characters_id(characters_id):
    un_character = Characters.query.get(characters_id)
    result = un_character.serialize()
    response_body = {"msg": "Character recibido",
                     "character": result}
    return jsonify(response_body), 200

@app.route('/vehicles/<int:vehicles_id>', methods=['GET'])
def get_vehicles_id(vehicles_id):
    un_vehicle= Vehicles.query.get(vehicles_id)
    result= un_vehicle.serialize()
    response_body = {"msg": "Vehicle recibido",
                     "vehicles": result}
    return jsonify(response_body), 200

# --------------------------------------MÉTODOS POST

@app.route('/users', methods= ['POST'])
def createUser():
    data = request.data
    data = json.loads(data)
    newUser = User(name = data["name"], email = data["email"], id = data["id"])
    db.session.add(newUser)
    db.session.commit()

    return jsonify(newUser.serialize())

@app.route('/planets', methods= ['POST'])
def createPlanet():
    data = request.data
    data = json.loads(data)
    newPlanet = Planets(id = data["id"], name = data["name"], climate = data["climate"], terrain = data ["terrain"], description = data["description"], diameter= data ["diameter"], rotation_period= data ["rotation_period"], orbital_period= data ["orbital_period"] )
    db.session.add(newPlanet)
    db.session.commit()

    return jsonify(newPlanet.serialize())

@app.route('/characters', methods= ['POST'])
def createCharacter():
    data = request.data
    data = json.loads(data)
    newCharacter = Characters(id = data["id"], name = data["name"], description = data["description"], gender= data ["gender"], mass= data ["mass"])
    db.session.add(newCharacter)
    db.session.commit()

    return jsonify(newCharacter.serialize())

@app.route('/vehicles', methods= ['POST'])
def createVehicles():
    data = request.data
    data = json.loads(data)
    newVehicles = Vehicles(id = data["id"], name = data["name"], clase = data["clase"], capacidad = data ["capacidad"], length = data ["length"])
    db.session.add(newVehicles)
    db.session.commit()

    return jsonify(newVehicles.serialize())

# --------------------------MÉTODOS DELETE

@app.route('/users/<int:users_id>', methods= ['DELETE'])
def deleteUser(users_id):
    borrarUser = User.query.get(users_id)
    db.session.delete(borrarUser)
    db.session.commit()

    return jsonify(borrarUser.serialize())

@app.route('/planets/<int:planets_id>', methods= ['DELETE'])
def deletePlanet(planets_id):
    borrarPlanet = Planets.query.get(planets_id)
    db.session.delete(borrarPlanet)
    db.session.commit()

    return jsonify(borrarPlanet.serialize())

@app.route('/characters/<int:characters_id>', methods= ['DELETE'])
def deleteCharacters(characters_id):
    borrarCharacter = Characters.query.get(characters_id)
    db.session.delete(borrarCharacter)
    db.session.commit()

    return jsonify(borrarCharacter.serialize())

@app.route('/vehicles/<int:vehicles_id>', methods= ['DELETE'])
def deleteVehicle(vehicles_id):
    borrarVehicles = Vehicles.query.get(vehicles_id)
    db.session.delete(borrarVehicles)
    db.session.commit()

    return jsonify(borrarVehicles.serialize())

# -------------------POST DE FAVORITES 

@app.route('/favorite/planets/<int:planets_id>', methods=['POST'])
def favorite_planet(planet_id):
    body_request = request.get_json()

    user_id = body_request.get("user_id", None)
    planet_id = body_request.get("planet_id", None)

    newplanetFavorite = Favorites(user_id=user_id, planet_id=planet_id)
    db.session.add(newplanetFavorite)
    db.session.commit()

    return jsonify(newplanetFavorite.serialize())

@app.route('/favorite/characters/<int:characters_id>', methods=['POST'])
def favorite_character(character_id):
    body_request = request.get_json()

    user_id = body_request.get("user_id", None)
    character_id = body_request.get("planet_id", None)

    newcharacterFavorite = Favorites(user_id=user_id, planet_id=character_id)
    db.session.add(newcharacterFavorite)
    db.session.commit()

    return jsonify(newcharacterFavorite.serialize())

@app.route('/favorite/vehicles/<int:vehicles_id>', methods=['POST'])
def favorite_vehicle(vehicle_id):
    body_request = request.get_json()

    user_id = body_request.get("user_id", None)
    vehicle_id = body_request.get("planet_id", None)

    newvehicleFavorite = Favorites(user_id=user_id, planet_id=vehicle_id)
    db.session.add(newvehicleFavorite)
    db.session.commit()

    return jsonify(newvehicleFavorite.serialize())

# ------------------------DELETE FAVORITES
@app.route('/favorite/planets/<int:planet_id>', methods= ['DELETE'])
def deleteFavPlanet(planet_id):
    borrarPlanetFavorite = Favorites.query.get(planet_id)
    db.session.delete(borrarPlanetFavorite)
    db.session.commit()

    response_body = {"msg": "borrado"}
    return jsonify(borrarPlanetFavorite.serialize())

@app.route('/favorite/characters/<int:character_id>', methods= ['DELETE'])
def deleteFavCharacter(character_id):
    borrarCharacterFav = Favorites.query.get(character_id)
    db.session.delete(borrarCharacterFav)
    db.session.commit()

    return jsonify(borrarCharacterFav.serialize())

@app.route('/favorite/vehicles/<int:vehicles_id>', methods= ['DELETE'])
def deleteFavVehicle(vehicle_id):
    borrarVehicleFav = Favorites.query.get(vehicle_id)
    db.session.delete(borrarVehicleFav)
    db.session.commit()

    return jsonify(borrarVehicleFav.serialize())

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
