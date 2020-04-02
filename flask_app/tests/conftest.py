import pytest

from application import create_app
from application.models import db, User
from config import TestingConfig


@pytest.fixture(scope='module')
def new_user():
    user = User(email='patkennedy79@gmail.com', name='FlaskIsAwesome', role="user")
    user.set_password("hsad@#sfds_123qe!@#@1")
    return user


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(TestingConfig)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(email='patkennedy79@gmail.com', name='patkennedy')
    user1.set_password('FlaskIsAwesome')
    user2 = User(email='kennedyfamilyrecipes@gmail.com', name='PaSsWoRd')
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.session.remove()
    db.drop_all()
