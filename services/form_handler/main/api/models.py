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

    def __init__(self, type, catid, isvisible):
        self.type = type
        self.catid = catid
        self.isvisible = isvisible

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type,
            'category_id': self.catid
        }

class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    gpid = db.Column(db.String(128), nullable=True)
    types = db.Column(db.String(128), nullable=True)

    def __init__(self, name, gpid, types):
        self.name = name
        self.gpid = gpid
        self.types = types

class Submission(db.Model):
    __tablename__ = 'submission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lid = db.Column(db.Integer, db.ForeignKey('location.id'))
    fid = db.Column(db.Integer, db.ForeignKey('foodtype.id'))
    numducks = db.Column(db.Integer, nullable=False)
    grams = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    def __init__(self, lid, fid, numducks, grams, datetime):
        self.lid = lid
        self.fid = fid
        self.numducks = numducks
        self.grams = grams
        self.datetime = datetime

    def to_json(self):
        return {
            'id': self.id,
            'location_id': self.lid,
            'foodtype_id': self.fid,
            'numducks': self.numducks,
            'grams': self.grams,
            'datetime': self.datetime.strftime('%Y-%m-%d %H:%M:%S')
        }