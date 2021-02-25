import pytest

from users.models import CustomUser


@pytest.fixture(scope="function")
def add_user():
    def _add_user(email, password):
        user = CustomUser.objects.create_user(email=email, password=password)
        return user

    return _add_user


@pytest.fixture(scope="function")
def add_superuser():
    def _add_superuser(email, password, **extra_fields):
        user = CustomUser.objects.create_superuser(
            email=email, password=password, **extra_fields
        )
        return user

    return _add_superuser
