import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from movies.models import Collection


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_register(client):
    url = reverse('register')
    data = {
        "username": "ajithsingh",
        "password": "StrongPassword123!"
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'access_token' in response.data


@pytest.mark.django_db
def test_register_username_exists(client, user):
    url = reverse('register')
    data = {
        "username": user.username,
        "password": "NewPassword123!"
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'username' in response.data


@pytest.mark.django_db
def test_movie_list(client, user):
    url = reverse('movie-list')
    client.force_authenticate(user=user)
    response = client.get(url, {'page': 1}, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'movies' in response.data
    assert 'count' in response.data


@pytest.mark.django_db
def test_movie_list_not_authenticated(client):
    url = reverse('movie-list')
    response = client.get(url, {'page': 1}, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_collection(client, user):
    url = reverse('collection-list')
    client.force_authenticate(user=user)
    data = {
        "title": "My Favorite Movies",
        "description": "A collection of my favorite movies.",
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'collection_uuid' in response.data


@pytest.mark.django_db
def test_create_collection_duplicate_title(client, user):
    url = reverse('collection-list')
    client.force_authenticate(user=user)
    Collection.objects.create(user=user, title="My Favorite Movies", description="A collection of my favorite movies.")
    data = {
        "title": "My Favorite Movies",
        "description": "Trying to create a collection with a duplicate title."
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'title' in response.data


@pytest.mark.django_db
def test_get_collection(client, user):
    collection = Collection.objects.create(user=user, title="My Collection", description="A collection description")
    url = reverse('collection-detail', args=[collection.uuid])
    client.force_authenticate(user=user)
    response = client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'title' in response.data
    assert response.data['title'] == collection.title


@pytest.mark.django_db
def test_update_collection(client, user):
    collection = Collection.objects.create(user=user, title="My Collection", description="A collection description")
    url = reverse('collection-detail', args=[collection.uuid])
    client.force_authenticate(user=user)
    data = {
        "title": "Updated Collection Title",
        "description": "Updated description."
    }
    response = client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    collection_uuid = response.data.get('collection_uuid')
    collection = Collection.objects.get(uuid=collection_uuid)
    assert collection.title == "Updated Collection Title"
    assert collection.description == "Updated description."


@pytest.mark.django_db
def test_delete_collection(client, user):
    collection = Collection.objects.create(user=user, title="To Be Deleted", description="This collection will be deleted.")
    url = reverse('collection-detail', args=[collection.uuid])
    client.force_authenticate(user=user)
    response = client.delete(url, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Collection.objects.filter(uuid=collection.uuid).count() == 0


