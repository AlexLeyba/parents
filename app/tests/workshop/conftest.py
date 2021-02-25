import io

import pytest
from PIL import Image

from django.contrib.contenttypes.models import ContentType
from workshop.models import Workshop, Day, Like, Comment, PartOfDay, Video


@pytest.fixture(scope="function")
def add_workshop():
    def _add_workshop():
        workshop = Workshop.objects.create(title="workshop")
        return workshop

    return _add_workshop


@pytest.fixture(scope="function")
def add_part_of_the_day(add_day_to_workshop):
    def _add_part_of_the_day():
        part_of_the_day = PartOfDay.objects.create(
            title="Part 1", text="Example text", day=add_day_to_workshop()
        )
        return part_of_the_day

    return _add_part_of_the_day


@pytest.fixture(scope="function")
def add_like():
    def _add_like(obj, user):
        content_type = ContentType.objects.get_for_model(obj)
        like = Like.objects.create(
            user=user, object_id=obj.id, content_type=content_type
        )
        return like

    return _add_like


@pytest.fixture(scope="function")
def add_comment():
    def _add_comment(obj, user, parent_comment):
        content_type = ContentType.objects.get_for_model(obj)
        comment = Comment.objects.create(
            user=user,
            text="text",
            object_id=obj.id,
            content_type=content_type,
            parent_comment=parent_comment,
        )
        return comment

    return _add_comment


@pytest.fixture(scope="function")
def add_fake_image():
    file_obj = io.BytesIO()
    image = Image.new("RGBA", size=(50, 50), color=(256, 0, 0))
    image.save(file_obj, "png")
    file_obj.seek(0)
    file_obj.name = "fake.png"
    file_obj.size = 1000
    return file_obj


@pytest.fixture(scope="function")
def add_day_to_workshop(add_workshop):
    def _add_day_to_workshop():
        day = Day.objects.create(
            title="day1",
            desc="desc",
            image="media/RGB.jpg",
            publish=True,
            workshop=add_workshop(),
        )
        return day

    return _add_day_to_workshop


@pytest.fixture(scope="function")
def add_model_instance_to_day(add_day_to_workshop):
    def _add_model_instance_to_day(model):
        instance = model.objects.create(
            title=f"{model.__name__} 1",
            url="https://www.google.com",
            day=add_day_to_workshop(),
        )
        return instance

    return _add_model_instance_to_day


@pytest.fixture(scope="function")
def add_media_model():
    def _add_media_model(model):
        instance = model.objects.create(
            title=f"{model.__name__} 1", url="https://www.google.com"
        )
        return instance

    return _add_media_model


@pytest.fixture(scope="function")
def add_video(add_part_of_the_day):
    def _add_video():
        video = Video.objects.create(
            url="https:///www.google.com", part_day=add_part_of_the_day()
        )
        return video

    return _add_video
