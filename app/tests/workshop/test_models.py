import pytest
from workshop.models import (
    Workshop,
    Day,
    PartOfDay,
    Methodology,
    Film,
    Book,
    Like,
    Comment,
    Video,
    Image,
    Info,
)
from users.models import CustomUser


@pytest.mark.django_db
def test_create_info_model():
    info = Info(title="test test test")

    assert str(info) == info.title
