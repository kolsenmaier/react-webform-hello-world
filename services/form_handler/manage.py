import unittest
from flask.cli import FlaskGroup
from main import create_app, db
from main.api.models import FoodCategory
from main.api.models import FoodType

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def seed_db():
    db.session.add(FoodCategory(name='Bread'))
    db.session.add(FoodCategory(name='Corn'))
    db.session.add(FoodCategory(name='Greens'))
    db.session.add(FoodCategory(name='Oats'))
    db.session.add(FoodCategory(name='Peas'))
    db.session.add(FoodCategory(name='Pellets'))
    db.session.add(FoodCategory(name='Seeds'))
    db.session.add(FoodCategory(name='Other'))
    db.session.commit()
    db.session.add(FoodType(name='White', catid=1, isvisible=True))
    db.session.add(FoodType(name='Whole wheat', catid=1, isvisible=True))
    db.session.add(FoodType(name='Sourdough', catid=1, isvisible=True))
    db.session.add(FoodType(name='Rye', catid=1, isvisible=True))
    db.session.add(FoodType(name='Other', catid=1, isvisible=True))
    db.session.add(FoodType(name='Canned', catid=2, isvisible=True))
    db.session.add(FoodType(name='Frozen', catid=2, isvisible=True))
    db.session.add(FoodType(name='Fresh', catid=2, isvisible=True))
    db.session.add(FoodType(name='Lettuce', catid=3, isvisible=True))
    db.session.add(FoodType(name='Other', catid=3, isvisible=True))
    db.session.add(FoodType(name='Rolled', catid=4, isvisible=True))
    db.session.add(FoodType(name='Instant', catid=4, isvisible=True))
    db.session.add(FoodType(name='Frozen', catid=5, isvisible=True))
    db.session.add(FoodType(name='Fresh', catid=5, isvisible=True))
    db.session.add(FoodType(name='Duck pellets', catid=6, isvisible=True))
    db.session.add(FoodType(name='Bird seed', catid=7, isvisible=True))
    db.session.add(FoodType(name='Other', catid=7, isvisible=True))
    db.session.commit()

@cli.command()
def test():
    # Runs the tests without code coverage
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    cli()