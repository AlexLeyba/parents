import pytest
from consultation.models import Status, Theme, ConsultationCenter
from rest_framework.test import APIClient


@pytest.fixture(scope="function")
def api_client():
    api_client = APIClient()
    return api_client


@pytest.fixture(scope="function")
def add_status():
    def _add_status(title):
        status = Status(title=title)
        status.save()
        return status

    return _add_status


@pytest.fixture(scope="function")
def add_theme():
    def _add_theme(title):
        theme = Theme(title=title)
        theme.save()
        return theme

    return _add_theme


@pytest.fixture(scope="function")
def add_center_consultation():
    def _add_center_consultation(title):
        center_consultation = ConsultationCenter(
            title=title,
            description="test",
            address="street 45",
            url="https://test.com",
            phone="899932456",
            email="test@gmail.com",
        )
        center_consultation.save()
        return center_consultation

    return _add_center_consultation
