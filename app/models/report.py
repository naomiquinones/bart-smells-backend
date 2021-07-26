from app import db

class Report (db.Model):
    """
    Report model
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    train = db.Column(db.String(50), nullable=False)
    direction = db.Column(db.String(50), nullable=False)
    car_number = db.Column(db.String(5), nullable=False)
    votes = db.Column(db.Integer, default=0)
    rider_id = db.Column(db.Integer, db.ForeignKey('rider.id'), nullable=False)

    def __repr__(self):
        return f'Report({self.type}, {self.train} going to {self.direction} on {self.date})'

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'type': self.type,
            'description': self.description,
            'train': self.train,
            'direction': self.direction,
            'car_number': self.car_number,
            'votes': self.votes,
            'rider_id': self.rider_id
        }
