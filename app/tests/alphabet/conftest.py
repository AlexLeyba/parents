import pytest
from alphabet.models import Category, Article, Author, Tag, Video, StepTag, Step


@pytest.fixture(scope="function")
def add_tag():
    def _add_tag(title):
        tag = Tag.objects.create(title=title)
        return tag

    return _add_tag


@pytest.fixture(scope="function")
def add_category():
    def _add_category():
        category = Category.objects.create(title="Категория")
        return category

    return _add_category


@pytest.fixture(scope="function")
def add_author(django_user_model):
    def _add_author():
        user = django_user_model.objects.create(email="test@test.com", password="1231")
        author = Author.objects.create(user=user, position="Director")
        return author

    return _add_author


@pytest.fixture(scope="function")
def add_article(add_category, add_author, add_tag):
    def _add_article():
        tag1, tag2 = add_tag(title="First"), add_tag(title="Second")
        article = Article.objects.create(
            title="Article",
            annotation="Annotation",
            description="Description",
            text="Text",
            author=add_author(),
            category=add_category(),
        )
        article.tags.add(tag1, tag2)
        article.save()
        return article

    return _add_article


@pytest.fixture(scope="function")
def add_article_with_step_tags(add_category, add_tag):
    def _add_article(title, step_tags):
        tag1, tag2 = add_tag(title="First"), add_tag(title="Second")
        article = Article.objects.create(
            title=title,
            annotation="Annotation",
            description="Description",
            text="Text",
            category=add_category(),
        )
        article.tags.add(tag1, tag2)
        for step_tag in step_tags:
            article.step_tags.add(step_tag)
        article.save()
        return article

    return _add_article


@pytest.fixture(scope="function")
def add_article_without_author(add_category, add_tag):
    def _add_article_without_author():
        tag1, tag2 = add_tag(title="First"), add_tag(title="Second")
        article = Article.objects.create(
            title="Article",
            annotation="Annotation",
            description="Description",
            text="Text",
            category=add_category(),
        )
        article.tags.add(tag1, tag2)
        article.save()
        return article

    return _add_article_without_author


@pytest.fixture(scope="function")
def add_video(add_category):
    def _add_video(title):
        video = Video.objects.create(
            title=title, url="https://qwreyt.com", category=add_category()
        )
        return video

    return _add_video


@pytest.fixture(scope="function")
def add_step():
    def _add_step(title):
        step = Step.objects.create(title=title)
        step.save()
        return step

    return _add_step


@pytest.fixture(scope="function")
def add_step_tag():
    def _add_step_tag(title, step):
        step_tag = StepTag.objects.create(title=title, step=step)
        step_tag.save()
        return step_tag

    return _add_step_tag
