from application.models import User
 

def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    assert new_user.email == 'patkennedy79@gmail.com'
    assert new_user.password_hash != 'hsad@#sfds_123qe!@#@1'
    assert new_user.check_password("hsad@#sfds_123qe!@#@1")
    assert not new_user.is_anonymous
    assert new_user.role == 'user'
