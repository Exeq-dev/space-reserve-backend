from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.user import User
from flask_jwt_extended import create_access_token


auth_bp = Blueprint("auth", __name__)

# REGISTRO DE USUARIOS
@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")

    if not all([first_name, last_name, email, password]):
        return jsonify({"error": "Faltan datos!"}), 400
    
    if User.query.filter_by(email = email).first():
        return jsonify({"error": "Email ya registrado"}), 400
    
    if len(first_name) < 3:
        return jsonify({"error": "El nombre debe tener al menos 3 carácteres"}), 400
    
    if '@' not in email:
        return jsonify({"error": "El correo debe contener @"}), 400
    
    if len(password) <= 6:
        return jsonify({"error": "La contraseña debe contener al menos 6 carácteres"}), 400

    hashed_password = generate_password_hash(password)

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password,
        role_id=1
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado correctamente"}), 201


# INICIO DE SESIÓN
@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Credenciales inválidas"}), 401
    
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Credenciales inválidas"}), 401
    
    access_token = create_access_token(
        identity={
            "id": user.id,
            "role": user.role.name
        }
    )

    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "email": user.email,
            "role": user.role.name
        }
    })

