from flask import Blueprint, request, jsonify
from app import db
from app.models.space import Space

spaces_bp = Blueprint("spaces", __name__)

# CREAR UN ESPACIO
@spaces_bp.route("/spaces", methods=["POST"])
def create_space():
    data = request.get_json()

    required = ["name", "description", "location", "capacity", "price_per_hour"]
    if not all(key in data for key in required):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    space = Space(
        name=data["name"],
        description=data["description"],
        location=data["location"],
        capacity=data["capacity"],
        price_per_hour=data["price_per_hour"],
        image_url=data.get("image_url"),
    )

    db.session.add(space)
    db.session.commit()

    return jsonify({
        "id": space.id,
        "name": space.name,
        "description": space.description,
        "location": space.location,
        "capacity": space.capacity,
        "price_per_hour": space.price_per_hour,
        "img_url": space.image_url,
    }), 201

# LISTAR LOS ESPACIOS
@spaces_bp.route("/spaces", methods=["GET"])
def get_spaces():
    spaces = Space.query.all()

    result = []
    for space in spaces:
        result.append({
            "id": space.id,
            "name": space.name,
            "description": space.description,
            "location": space.location,
            "capacity": space.capacity,
            "price_per_hour": space.price_per_hour,
            "img_url": space.image_url,
        })
    
    return jsonify(result)

# EDITAR/MODIFICAR UN ESPACIO
@spaces_bp.route("/spaces/<int:space_id>", methods=["PUT"])
def update_space(space_id):
    space = Space.query.get(space_id)

    if not space:
        return jsonify({"error": "Espacio no encontrado"}), 404
    
    data = request.get_json()

    space.name = data.get("name", space.name)
    space.location = data.get("location", space.location)
    space.capacity = data.get("capacity", space.capacity)

    db.session.commit()

    return jsonify({
        "id": space.id,
        "name": space.name,
        "location": space.location,
        "capacity": space.capacity
    })

# ELIMINAR UN ESPACIO
@spaces_bp.route("/spaces/<int:space_id>", methods=["DELETE"])
def delete_space(space_id):
    space = Space.query.get(space_id)

    if not space:
        return jsonify({"error": "Espacio no encontrado"}), 404
    
    db.session.delete(space)
    db.session.commit()

    return jsonify({"message": "Espacio eliminado"})

