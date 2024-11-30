import pytest
from movies.serializers import RegisterSerializer


@pytest.mark.django_db
def test_register_serializer_valid_data():
    data = {
        'username': 'testuser',
        'password': 'Password123!',
    }
    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.username == data['username']
    assert user.check_password(data['password'])


@pytest.mark.django_db
def test_register_serializer_invalid_username():
    data = {
        'username': 'testuser@invalid',
        'password': 'Password123!',
    }
    serializer = RegisterSerializer(data=data)
    assert not serializer.is_valid()
    assert 'username' in serializer.errors


@pytest.mark.django_db
def test_register_serializer_missing_password():
    data = {
        'username': 'testuser',
    }
    serializer = RegisterSerializer(data=data)
    assert not serializer.is_valid()
    assert 'password' in serializer.errors


@pytest.mark.django_db
def test_register_serializer_invalid_password():
    data = {
        'username': 'testuser',
        'password': 'short',
    }
    serializer = RegisterSerializer(data=data)
    assert not serializer.is_valid()
    assert 'password' in serializer.errors
