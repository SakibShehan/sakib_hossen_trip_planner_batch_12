from .. import db

# This table will map trips and travlers in mamy to many relationship
trip_travelers = db.Table(
    "trip_travelers",
    db.Column("trip_id", db.Integer, db.ForeignKey("trips.id"), primary_key=True),
    db.Column("traveler_id", db.Integer, db.ForeignKey("travelers.id"), primary_key=True),
)