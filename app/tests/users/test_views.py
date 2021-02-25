import pytest
from users.models import CustomUser


@pytest.mark.django_db
def test_charge_user_information(add_user, api_client):
    user = add_user(email="test@gmail.com", password="foo")

    assert user.first_name == ""
    assert user.last_name == ""
    assert user.surname == ""

    response = api_client.patch(
        f"/users/profile/{user.id}/",
        data={"first_name": "Ivan", "surname": "Ivanov"},
        format="json",
    )
    assert response.status_code == 200
    assert response.data["first_name"] == "Ivan"


@pytest.mark.django_db
def test_charge_user_information_invalid_id(api_client):
    response = api_client.patch(
        "/users/profile/999/",
        data={"first_name": "Ivan", "surname": "Ivanov"},
        format="json",
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_user_profile(add_user, api_client):
    user = add_user(email="test@gmail.com", password="foo")

    response = api_client.get(f"/users/profile/{user.id}/")
    assert response.status_code == 200
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_get_user_profile_invalid_id(api_client):
    response = api_client.get("/users/profile/999/")
    assert response.status_code == 404
