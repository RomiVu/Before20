'''
test main_buleprint
'''

def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200

def test_home_page_post(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client.post('/')
    assert response.status_code == 405

def test_invaild_page_get(test_client):
    """
    GIVEN a Flask application
    WHEN the '/bulltshit' page is requested (GET)
    THEN check that a '404' status code is returned
    """
    response = test_client.get('/bulltshit')
    assert response.status_code == 404

