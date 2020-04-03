'''
test for API
'''

def test_api_access_failed(test_client, init_database):
    response = test_client.get('/get_api_token')
    assert response.status_code == 405 # can use GET http request

    response = test_client.post('/get_api_token', json=dict(username='looooke'))
    assert response.json == {"status": 400, "msg": "invaild user information"} # user post info is not enough

    response = test_client.post('/get_api_token', json=dict(username='looooke', password='adwqfqwsasadas'))
    assert response.json == {"status": 400, "msg": "invaild user information"} # password is flase

    response = test_client.post('/get_api_token', json=dict(username='looooke', password='corret password'))
    assert response.json == {"status": 400, "msg": "invaild user information"} # role is not a admin 


def test_api_token_verified(test_client, init_database, api_wrapper):
    response = test_client.post('/get_api_token', json=dict(username='loooooke', password='wedwvwe^#$gDFfs'))
    token = api_wrapper('loooooke').api_token.first().token
    assert response.json == {"status":200, "msg": "success", "token": token}


def test_api_token_expired(test_client, init_database, api_wrapper):
    # user'role is admin or api but token expired
    token = api_wrapper('patkennedy').api_token.first().token
    response = test_client.post('/api', json=dict(token=token, opt='create', params={"a":123,"b":456}))
    
    assert response.json == {"status":401, "msg": "token exipred, please apply for a new one."} 


def test_db_create_user(test_client, init_database):
    pass

def test_db_update_user(test_client, init_database):
    pass

def test_db_delete_user(test_client, init_database):
    pass

def test_db_read_user(test_client, init_database):
    pass

def test_db_create_post(test_client, init_database):
    pass

def test_db_update_post(test_client, init_database):
    pass

def test_db_delete_post(test_client, init_database):
    pass

def test_db_read_post(test_client, init_database):
    pass

def test_db_create_category(test_client, init_database):
    pass

def test_db_update_category(test_client, init_database):
    pass

def test_db_delete_category(test_client, init_database):
    pass

def test_db_read_category(test_client, init_database):
    pass