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
    db.session.add(FoodCategory(name='Other'))
    db.session.commit()
    db.session.add(FoodType(type='Rye', catid=1, isvisible=True))
    db.session.add(FoodType(type='White', catid=1, isvisible=False))
    db.session.add(FoodType(type='Raisins', catid=2, isvisible=True))
    db.session.commit()

@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    cli()