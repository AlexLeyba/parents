import pytest
from consultation.models import Consultation, Theme, Status, MapTag, ConsultationCenter


@pytest.mark.django_db
def test_create_consultation():
    theme = Theme(title="new theme")
    theme.save()
    status = Status(title="new status")
    status.save()
    consultation = Consultation(
        name="Ivan Ivanov",
        email="ivan@gmail.com",
        phone="89997504330",
        sex="Муж",
        age="18 - 35",
        district="new district",
        theme=theme,
        status=status,
    )
    consultation.save()

    assert str(consultation) == consultation.name
    assert consultation.check == False


@pytest.mark.django_db
def test_create_status():
    status = Status(title="new status")

    assert str(status) == status.title


@pytest.mark.django_db
def test_create_theme():
    theme = Theme(title="new theme")

    assert str(theme) == theme.title


@pytest.mark.django_db
def test_create_map_tag():
    map_tag = MapTag(title="new district", value="123", slug="new district")

    assert str(map_tag) == map_tag.title


@pytest.mark.django_db
def test_create_consultation_center():
    center = ConsultationCenter(
        title="new center",
        description="test",
        image="media/test.png",
        address="street 45",
        url="https://test.com",
        phone="899932456",
        email="test@gmail.com",
        skype="test",
    )

    assert str(center) == center.title
