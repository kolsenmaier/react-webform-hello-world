from main import db

class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.String(128), nullable=False)
    isvisible = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(self, category, type, amount):
        self.category = category
        self.type = type
        self.amount = amount