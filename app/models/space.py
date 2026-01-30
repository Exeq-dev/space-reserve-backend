from app import db

class Space(db.Model):
    __tablename__ = "spaces"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    price_per_hour = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)

    reservations = db.relationship("Reservation", backref="space", lazy=True)