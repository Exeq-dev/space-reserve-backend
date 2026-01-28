from flask import Blueprint, request, jsonify
from app import db
from app.models.space import Space
from app.models.reservation import Reservation
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity

reservations_bp = Blueprint("reservations", __name__)

# CREAR RESERVA
@reservations_bp.route("/reservations", methods=["POST"])
@jwt_required()
def create_reservation():
    user = get_jwt_identity()
    data = request.get_json()

    space = Space.query.get(data.get("space_id"))
    if not space:
        return jsonify({"error": "Espacio no existe"}), 404
    
    start = datetime.fromisoformat(data["start_time"])
    end = datetime.fromisoformat(data["end_time"])

    if start >= end:
        return jsonify({"error": "Horario inválido"}), 400
    
    overlapping = Reservation.query.filter(
        Reservation.space_id == space.id,
        Reservation.start_time < end,
        Reservation.end_time > start
    ).first()

    if overlapping:
        return jsonify({"error": "Horario ocupado"}), 409
    
    reservation = Reservation(
        space_id=space.id,
        user_id=user["id"],
        start_time=start,
        end_time=end
    )

    db.session.add(reservation)
    db.session.commit()

    return jsonify({
        "id": reservation.id,
        "space_id": space.id,
        "user_id": user["id"],
        "start_time": reservation.start_time.isoformat(),
        "end_time": reservation.end_time.isoformat()
    }), 201

# LISTAR RESERVAS POR ESPACIO
@reservations_bp.route("/spaces/<int:space_id>/reservations", methods=["GET"])
def get_reservations_by_space(space_id):
    reservations = Reservation.query.filter_by(space_id=space_id).all()

    result = []
    for r in reservations:
        result.append({
            "id": r.id,
            "start_time": r.start_time.isoformat(),
            "end_time": r.end_time.isoformat()
        })
    
    return jsonify(result)

# OBTENER LA DISPONIBILIDAD DE HORARIOS DE UN ESPACIO
@reservations_bp.route("/spaces/<int:space_id>/availability", methods=["GET"])
def get_availability(space_id):
    date_str = request.args.get("date")

    if not date_str:
        return jsonify({"error": "Fecha requerida (YYYY-MM-DD)"}), 400
    
    date = datetime.fromisoformat(date_str)

    day_start = date.replace(hour=8, minute=0)
    day_end = date.replace(hour=22, minute=0)

    reservations = Reservation.query.filter(
        Reservation.space_id == space_id,
        Reservation.start_time >= day_start,
        Reservation.end_time < day_end,
    ).order_by(Reservation.start_time).all()

    available_slots = []
    current_time = day_start

    for r in reservations:
        if current_time < r.start_time:
            available_slots.append({
                "start": current_time.isoformat(),
                "end": r.start_time.isoformat()
            })
        current_time = r.end_time

    if current_time < day_end:
        available_slots.append({
            "start": current_time.isoformat(),
            "end": day_end.isoformat()
        })
    
    return jsonify(available_slots)

# ELIMINAR LA RESERVA DE UN ESPACIO
@reservations_bp.route("/reservations/<int:reservation_id>", methods=["DELETE"])
@jwt_required()
def delete_reservation(reservation_id):
    user = get_jwt_identity()

    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({"error": "Reserva no encontrada"}), 404
    
    if reservation.user_id != user["id"]:
        return jsonify({"error": "No autorizado"}), 403

    db.session.delete(reservation)
    db.session.commit()

    return jsonify({"message": "Reserva cancelada correctamente"})