from collections import OrderedDict
import pytest


@pytest.mark.django_db
def test_view_category(api_client, add_category):
    category = add_category()

    response = api_client.get("/alphabet/")

    assert response.status_code == 200
    assert response.data[0]["title"] == category.title


@pytest.mark.django_db
def test_view_detail_article(api_client, add_article):
    article = add_article()

    response = api_client.get(f"/alphabet/article/{article.id}/")

    assert response.status_code == 200
    assert response.data["article"]["title"] == article.title


@pytest.mark.django_db
def test_search(api_client, add_article, add_video):
    article = add_article()
    first_video = add_video(title="video one")
    two_video = add_video(title="video two")

    response = api_client.get(f"/alphabet/search/", {"search": article.title})
    assert response.status_code == 200
    assert response.data["articles"][0]["title"] == article.title
    assert response.data["articles_count"] == 1
    assert response.data["videos_count"] == 0

    response = api_client.get("/alphabet/search/", {"search": "artic"})
    assert response.status_code == 200
    assert response.data["articles"][0]["title"] == article.title
    assert response.data["articles_count"] == 1
    assert response.data["videos_count"] == 0

    response = api_client.get("/alphabet/search/", {"search": "video"})
    assert response.status_code == 200
    assert response.data["videos"][0]["title"] == first_video.title
    assert response.data["videos"][1]["title"] == two_video.title
    assert response.data["articles_count"] == 0
    assert response.data["videos_count"] == 2


@pytest.mark.django_db
def test_search_invalid_request(api_client):
    response = api_client.get(f"/alphabet/search/")
    assert response.status_code == 400


@pytest.mark.django_db
def test_get_last_five_articles(api_client, add_article_without_author):
    for article in range(5):
        article = add_article_without_author()

    response = api_client.get("/alphabet/last_five_articles/")
    assert response.status_code == 200
    assert len(response.data) == 5


@pytest.mark.django_db
def test_get_steps(api_client, add_step, add_step_tag):
    step_one = add_step(title="step one")
    step_two = add_step(title="step two")
    tag_one = add_step_tag(title="teg step one", step=step_one)
    tag_two = add_step_tag(title="tag two for step one", step=step_one)
    tag_three = add_step_tag(title="teg for step two", step=step_two)

    response = api_client.get("/alphabet/steps/")
    assert response.status_code == 200
    assert response.data[0]["title"] == step_one.title
    assert response.data[0]["step_tags"][0]["title"] == tag_one.title
    assert response.data[0]["step_tags"][1]["title"] == tag_two.title
    assert response.data[1]["step_tags"][0]["title"] == tag_three.title


@pytest.mark.django_db
def test_get_sorted_articles(
    api_client, add_step, add_step_tag, add_article_with_step_tags
):
    step_one = add_step(title="step one")
    step_two = add_step(title="step two")
    tag_one = add_step_tag(title="teg step one", step=step_one)
    tag_two = add_step_tag(title="tag two for step one", step=step_one)
    tag_three = add_step_tag(title="teg for step two", step=step_two)
    article_one = add_article_with_step_tags(
        title="article one", step_tags=[tag_one, tag_two]
    )
    article_two = add_article_with_step_tags(title="article two", step_tags=[tag_three])

    response = api_client.post(
        "/alphabet/sorted_articles/", {"step_tags": [tag_one.id, tag_two.id]}
    )

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == article_one.title

    response = api_client.post(
        "/alphabet/sorted_articles/", {"step_tags": [tag_three.id]}
    )

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == article_two.title
