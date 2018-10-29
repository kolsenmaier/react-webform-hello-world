import unittest
from flask.cli import FlaskGroup
from main import create_app, db
from main.api.models import Food

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def seed_db():
    db.session.add(Food(category='Bread', type='Rye', amount='10g'))
    db.session.add(Food(category='Bread', type='White', amount='50g'))
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