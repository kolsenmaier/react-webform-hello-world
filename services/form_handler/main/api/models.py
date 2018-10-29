from main import db

class FoodCategory(db.Model):
    __tablename__ = 'foodcategory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

class FoodType(db.Model):
    __tablename__ = 'foodtype'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(128), nullable=False)
    catid = db.Column(db.Integer, db.ForeignKey('foodcategory.id'))
    isvisible = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(self, type, catid):
        self.type = type
        self.catid = catid

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type,
            'catid': self.catid,
            'isvisible': self.isvisible
        }