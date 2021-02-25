import pytest


@pytest.mark.django_db
def test_create_user(add_user):
    user = add_user(email="normal@user.com", password="foo")
    assert user.email == "normal@user.com"
    assert str(user) == user.email
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_try_create_user_with_empty_email(add_user):
    with pytest.raises(ValueError):
        add_user(password="foo", email=None)


@pytest.mark.django_db
def test_create_superuser(add_superuser):
    admin_user = add_superuser(email="super@user.com", password="foo")
    assert admin_user.email == "super@user.com"
    assert admin_user.is_active
    assert admin_user.is_staff
    assert admin_user.is_superuser
    assert str(admin_user) == admin_user.email


@pytest.mark.django_db
def test_try_create_no_staff_superuser(add_superuser):
    with pytest.raises(ValueError) as not_staff:
        add_superuser(email="super@user.com", password="foo", is_staff=False)
    assert "is_staff=True" in str(not_staff.value)


@pytest.mark.django_db
def test_try_create_no_superuser_user(add_superuser):
    with pytest.raises(ValueError) as not_superuser:
        add_superuser(email="super@user.com", password="foo", is_superuser=False)
    assert "is_superuser=True" in str(not_superuser.value)


@pytest.mark.django_db
def test_create_user_token(add_token):
    token = add_token()
    assert token.key
