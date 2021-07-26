from app import db

class Rider(db.Model):
    """
    Rider model
    """
    id = db.Column(db.Integer, primary_key=True)
    ridername = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    reports = db.relationship('Report', backref='rider', lazy=True)

    def __repr__(self):
        return f'<Rider({self.ridername}, {self.email})>'

    def to_dict(self):
        return {
            'id': self.id,
            'ridername': self.ridername,
            'email': self.email,
            'reports': [report.to_dict() for report in self.reports]
        }