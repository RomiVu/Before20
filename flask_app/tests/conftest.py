import pytest
from uuid import uuid4
from datetime import datetime, timedelta

from application import create_app
from application.models import db, User, ApiToken
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
    user1 = User(email='patkennedy79@gmail.com', name='patkennedy', role="api")
    user1.set_password('123456lk@@qwer')

    user2 = User(email='kennedyfamilyrecipes@gmail.com', name='PaSsWoRd', role='admin')
    user2.set_password('qwerty123')

    user3 = User(email='loooooke@gmail.com', name='loooooke', role="api")
    user3.set_password('wedwvwe^#$gDFfs')

    user4 = User(email='donngjue@gmail.com', name='donngjue', role='admin')
    user4.set_password('asdvergvefve')

    db.session.add_all([user1,user2,user3,user4])

    api_token1 = ApiToken(token=uuid4().hex, user=user1, exipred=datetime.utcnow()-timedelta(hours=1))
    api_token2 = ApiToken(token=uuid4().hex, user=user2)
    api_token3 = ApiToken(token=uuid4().hex, user=user3)
    api_token4 = ApiToken(token=uuid4().hex, user=user4)

    db.session.add_all([api_token1,api_token2,api_token3,api_token4])


    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.session.remove()
    db.drop_all()

@pytest.fixture(scope='module')
def api_wrapper():
    def user_api(username):
        user = User.query.filter_by(name=username).first()
        print(f"AH AH AH name:{username} email:{user.email} {user.api_token.first().token}")
        return user
    return user_api