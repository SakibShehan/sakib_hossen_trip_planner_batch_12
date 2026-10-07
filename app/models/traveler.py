from .. import db
from .trip_traveler import trip_travelers


class Traveler(db.Model):
    __tablename__ = "travelers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(254), nullable=False, unique=True, index=True)
    trips = db.relationship("Trip", secondary=trip_travelers, back_populates="travelers")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }