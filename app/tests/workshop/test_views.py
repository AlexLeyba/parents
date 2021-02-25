from collections import OrderedDict

import pytest
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from workshop.models import Workshop, Day, Methodology, Film, Book, Comment, Like, Info


@pytest.mark.django_db
def test_view_list_workshops(api_client, add_workshop):
    workshop = add_workshop()
    response = api_client.get("/workshop/")
    assert response.status_code == 200
    assert response.data[0]["title"] == workshop.title


@pytest.mark.django_db
def test_view_detail_part_of_the_day(api_client, add_part_of_the_day):
    part_of_day = add_part_of_the_day()
    response = api_client.get(f"/workshop/part/{part_of_day.id}/")
    assert response.status_code == 200
    assert response.data == {
        "id": part_of_day.id,
        "title": part_of_day.title,
        "text": part_of_day.text,
        "day": part_of_day.day.id,
        "images": [],
        "videos": [],
    }


@pytest.mark.django_db
def test_view_list_methodologies_without_day(api_client, add_media_model):
    methodology = add_media_model(model=Methodology)
    response = api_client.get("/workshop/methodology/")
    assert response.status_code == 200
    assert response.data[0]["title"] == methodology.title


@pytest.mark.django_db
def test_view_list_films_without_day(api_client, add_media_model):
    film = add_media_model(model=Film)
    response = api_client.get("/workshop/film/")
    assert response.status_code == 200
    assert response.data[0]["title"] == film.title


@pytest.mark.django_db
def test_view_list_books_without_day(api_client, add_media_model):
    book = add_media_model(model=Book)
    response = api_client.get("/workshop/book/")
    assert response.status_code == 200
    assert response.data[0]["title"] == book.title


@pytest.mark.django_db
def test_get_days_list(api_client, add_day_to_workshop):
    add_day_to_workshop()
    add_day_to_workshop()

    response = api_client.get("/workshop/days/")

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_view_detail_day(
    api_client, add_day_to_workshop, add_comment, django_user_model
):
    day = add_day_to_workshop()
    user = django_user_model.objects.create(
        email="someone@someone.com", password="something"
    )
    comment = add_comment(obj=day, user=user, parent_comment=None)
    response = api_client.get(f"/workshop/days/{day.id}/")
    assert response.status_code == 200
    assert response.data["title"] == day.title
    assert response.data["comments_count"] == 1
    assert response.data["comment"][0]["text"] == comment.text


@pytest.mark.django_db
def test_add_comment_to_day(api_client, add_day_to_workshop, add_token):
    day, token = add_day_to_workshop(), add_token()
    api_client.force_authenticate(token=token, user=token.user)
    response = api_client.post(
        f"/workshop/add-day-comment/{day.id}/", {"text": "comment"}
    )
    assert response.status_code == 201
    comment = Comment.objects.last()
    assert response.data == {"text": comment.text, "parent_comment": None}
    assert day.get_comments_count() == 1


@pytest.mark.django_db
def test_add_reply_to_comment(api_client, add_day_to_workshop, add_comment, add_token):
    day, token = add_day_to_workshop(), add_token()
    comment = add_comment(obj=day, user=token.user, parent_comment=None)
    api_client.force_authenticate(token=token, user=token.user)
    response = api_client.post(
        f"/workshop/add-replay-to-comment/{comment.id}/",
        {"text": "answer", "parent_comment": comment.id},
    )
    reply = Comment.objects.get(parent_comment=comment)
    assert response.status_code == 201
    assert response.data == {"text": reply.text, "parent_comment": comment.id}

    response = api_client.get(f"/workshop/days/{day.id}/")
    assert response.data["comment"][0]["text"] == comment.text
    assert response.data["comment"][0]["replies"][0]["text"] == reply.text


@pytest.mark.django_db
def test_add_like(api_client, add_token, add_day_to_workshop):
    token, day = add_token(), add_day_to_workshop()
    api_client.force_authenticate(token=token, user=token.user)
    response = api_client.post(f"/workshop/create-day-like/{day.id}/", {"status": True})
    assert len(Like.objects.filter(user=token.user)) == 1
    assert day.get_likes_count() == 1
    assert day.get_dislikes_count() == 0
    assert response.status_code == 201


@pytest.mark.django_db
def test_change_mark_like(api_client, add_token, add_day_to_workshop, add_like):
    token, day = add_token(), add_day_to_workshop()
    api_client.force_authenticate(token=token, user=token.user)
    add_like(obj=day, user=token.user)
    response = api_client.post(
        f"/workshop/create-day-like/{day.id}/", {"status": False}
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_like(api_client, add_token, add_day_to_workshop, add_like):
    token, day = add_token(), add_day_to_workshop()
    api_client.force_authenticate(token=token, user=token.user)
    add_like(obj=day, user=token.user)
    response = api_client.post(f"/workshop/create-day-like/{day.id}/", {"status": True})
    assert response.status_code == 204


@pytest.mark.django_db
def test_get_workshop_info(api_client):
    info = Info(title="test test test")
    info.save()

    response = api_client.get("/workshop/info/")

    assert response.status_code == 200
    assert response.data[0]["title"] == info.title
