from app import db

class Rider(db.Model):
    """
    Rider model
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    reports = db.relationship('Report', backref='rider', lazy=True, order_by='Report.date')

    def __repr__(self):
        return f'<Rider({self.name}, {self.email})>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'reports': [report.to_dict() for report in self.reports]
        }

    def update_email(self, email):
        self.email = email

    def update_from_form_data(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)