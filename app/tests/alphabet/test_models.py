import pytest
from alphabet.models import (
    Author,
    Tag,
    Category,
    Article,
    Video,
    MetaTags,
    Gallery,
    Step,
    StepTag,
)


@pytest.mark.django_db
def test_create_author(django_user_model):
    user = django_user_model.objects.create(email="test@test.com", password="123")
    author = Author(user=user, position="Директор")
    assert str(author) == f"{author.user.first_name} {author.user.last_name}"


@pytest.mark.django_db
def test_create_tag():
    tag = Tag(title="Дети")
    assert str(tag) == tag.title


@pytest.mark.django_db
def test_create_category():
    category = Category(title="Категория")
    assert str(category) == category.title


@pytest.mark.django_db
def test_create_article():
    article = Article(title="Статья 1", description="Описание", text="Текст")
    assert str(article) == article.title


@pytest.mark.django_db
def test_create_video():
    category = Category.objects.create(title="Категория")
    video = Video(title="Видео", url="https://www.youtube.com", category=category)

    assert str(video) == video.title


@pytest.mark.django_db
def test_create_meta_tags_model():
    article = Article(title="Статья 1", description="Описание", text="Текст")
    tags = MetaTags(desc="test test test", words="test test test", article=article)

    assert str(tags) == article.title


@pytest.mark.django_db
def test_create_images_for_slider():
    article = Article(title="Статья 1", description="Описание", text="Текст")
    image = Gallery(image="test.png", article=article)

    assert str(article) == article.title


@pytest.mark.django_db
def test_create_step():
    step = Step(title="step one", number=1)

    assert str(step) == step.title


@pytest.mark.django_db
def test_create_step_tag():
    step = Step(title="step one")
    step_tag = StepTag(title="Дети", step=step)
    assert str(step_tag) == step_tag.title
