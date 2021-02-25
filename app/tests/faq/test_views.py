from collections import OrderedDict
import pytest
from faq.models import Question, AboutUs, UsefulLinks


@pytest.mark.django_db
def test_view_list_faq(api_client, add_faq):
    faq = add_faq()
    response = api_client.get("/faq/")
    assert response.status_code == 200
    assert response.data[0]["question"] == faq.question


@pytest.mark.django_db
def test_add_new_question(api_client):
    response = api_client.post(
        "/faq/new/",
        {
            "name": "Иванов Иван Иванович",
            "email": "test@test.com",
            "text": "Почему так?",
        },
    )
    assert response.status_code == 201
    assert Question.objects.count() == 1


@pytest.mark.django_db
def test_get_favorite_faq(api_client, add_faq):
    not_favorite_faq = add_faq()
    favorite_faq = add_faq(check=True)

    response = api_client.get("/faq/favorite-faq/")
    assert response.status_code == 200
    assert response.data[0]["question"] == favorite_faq.question


@pytest.mark.django_db
def test_get_about_us(api_client):
    about_one = AboutUs.objects.create(description="new", char="a")
    about_two = AboutUs.objects.create(description="new two", char="b")

    response = api_client.get("/faq/about_us/")
    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["char"] == about_one.char
    assert response.data[1]["char"] == about_two.char


@pytest.mark.django_db
def test_get_useful_links(api_client):
    useful_links_one = UsefulLinks.objects.create(url="https://qewr.com")
    useful_links_two = UsefulLinks.objects.create(url="https://qewr2.com")

    response = api_client.get("/faq/useful_links/")
    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["url"] == useful_links_one.url
    assert response.data[1]["url"] == useful_links_two.url
