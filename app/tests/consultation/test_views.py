import pytest
from consultation.views import StatusList, AddConsultation
from consultation.models import MapTag


@pytest.mark.django_db
def test_get_status_list(api_client, add_status, add_theme):
    status_one = add_status(title="status one")
    status_two = add_status(title="status two")
    theme_one = add_theme(title="theme one")
    theme_two = add_theme(title="theme two")

    response = api_client.get("/consultation/status-list/")

    assert response.status_code == 200
    assert response.data["statuses"][0]["title"] == status_one.title
    assert response.data["statuses"][1]["title"] == status_two.title
    assert response.data["themes"][0]["title"] == theme_one.title
    assert response.data["themes"][1]["title"] == theme_two.title


@pytest.mark.django_db
def test_create_consultation(api_client, add_status, add_theme):
    status = add_status(title="status")
    theme = add_theme(title="theme")

    data = {
        "name": "Ivan Ivanov",
        "email": "ivan@gmail.com",
        "phone": "8999234333",
        "sex": "Муж",
        "age": "18 - 35",
        "status": status.id,
        "theme": theme.id,
        "district": "new district",
    }

    response = api_client.post(
        "/consultation/create-consultation/", data=data, format="json"
    )

    assert response.status_code == 201
    assert response.data["name"] == data["name"]


@pytest.mark.django_db
def test_get_map_tags(api_client):
    map_tag = MapTag.objects.create(
        title="district one", value="124", slug="district one"
    )
    map_tag.save()
    map_tag_two = MapTag.objects.create(
        title="district two", value="124", slug="district two"
    )
    map_tag_two.save()
    response = api_client.get("/consultation/map_tags/")
    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["title"] == map_tag.title
    assert response.data[1]["title"] == map_tag_two.title


@pytest.mark.django_db
def test_get_centers_consultations(api_client, add_center_consultation):
    one_center = add_center_consultation(title="one center")
    two_center = add_center_consultation(title="two center")

    response = api_client.get("/consultation/centers/")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["title"] == one_center.title
    assert response.data[1]["title"] == two_center.title
