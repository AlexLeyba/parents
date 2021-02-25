import pytest
from faq.models import FAQ, Question, AboutUs, UsefulLinks


@pytest.mark.django_db
def test_create_faq():
    faq = FAQ(question="It is me?", answer="Yes sir!")

    assert str(faq) == faq.question
    assert faq.check == False


@pytest.mark.django_db
def test_create_question():
    question = Question(
        name="Иванов Иван Иванович", email="test@test.com", text="Почему так??"
    )

    assert str(question) == question.text


@pytest.mark.django_db
def test_about_us_model():
    about_us = AboutUs(char="a", description="It is me?")

    assert str(about_us) == about_us.char


@pytest.mark.django_db
def test_useful_links_model():
    useful_links = UsefulLinks(image="media/test.png", url="https://qewr.com")

    assert str(useful_links) == useful_links.url
