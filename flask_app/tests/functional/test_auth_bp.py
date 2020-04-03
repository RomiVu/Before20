'''
test auth_buleprint
'''

def test_login_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b"Password" in response.data
    assert b"Username" in response.data
    assert b"Remember Me" in response.data


def test_valid_login_logout(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(username='PaSsWoRd', password='qwerty123'),
                                follow_redirects=True)
    assert response.status_code == 200

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200


def test_invalid_login(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/login',
                                data=dict(username='PaSsWoRd', password='sadsdas'),
                                follow_redirects=True)
    assert response.status_code == 200 # failed to login then back to /login


def test_valid_registration(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted to (POST)
    THEN check the response is valid and the user is logged in
    """
    response = test_client.post('/register',
                                data=dict(username='patkennedy79@yahoo.com',
                                          email='FlaskIsGreat',
                                          password='FlaskIsGreat'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data


def test_invalid_registration(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/register',
                                data=dict(email='patkennedy79@hotmail.com',
                                          username='FlaskIsGreat',
                                          password='FlskIsGreat'),   # Does NOT match!
                                follow_redirects=True)
    assert response.status_code == 200 # failed and then back to /register

