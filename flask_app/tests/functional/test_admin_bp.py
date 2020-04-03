'''
test for admin_blueprint
'''

def test_admin_authorized(test_client, init_database):
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
    WHEN get'/admin' page as role of 'user'
    THEN check the response is successful
    """
    response = test_client.get('/admin')
    assert response.status_code == 200


def test_admin_denied(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(username='patkennedy', password='FlaskIsAwesome'),
                                follow_redirects=True)

    assert response.status_code == 200

    """
    GIVEN a Flask application
    WHEN get'/admin' page as role of 'user'
    THEN check the response failed.
    """
    response = test_client.get('/admin')
    assert response.status_code == 200 # back to main_bp.index
