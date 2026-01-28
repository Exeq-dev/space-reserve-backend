from flask import Blueprint, request, jsonify
from app import db
from app.models.space import Space

spaces_bp = Blueprint("spaces", __name__)

# CREAR UN ESPACIO
@spaces_bp.route("/spaces", methods=["POST"])
def create_space():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    if not data.get("name"):
        return jsonify({"error": "El nombre es obligatorio"}), 400

    if not data.get("location"):
        return jsonify({"error": "La ubicación es obligatoria"}), 400

    if not isinstance(data.get("capacity"), int):
        return jsonify({"error": "La capacidad debe ser un número"}), 400

    space = Space(
        name=data["name"],
        location=data["location"],
        capacity=data["capacity"]
    )

    db.session.add(space)
    db.session.commit()

    return jsonify({
        "id": space.id,
        "name": space.name,
        "location": space.location,
        "capacity": space.capacity
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
            "location": space.location,
            "capacity": space.capacity
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

