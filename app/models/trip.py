from .. import db
from .trip_traveler import trip_travelers


class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    max_travelers = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="PLANNED")  # may be PLANNED, ONGOING, COMPLETED, CANCELLED

    travelers = db.relationship("Traveler", secondary=trip_travelers, back_populates="trips")

    expenses = db.relationship(
        "Expense", back_populates="trip", cascade="all, delete-orphan"
    )


    def to_dict(self):
        return {
            "id": self.id,
            "destination": self.destination,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "budget": self.budget,
            "max_travelers": self.max_travelers,
            "status": self.status
        }