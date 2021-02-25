import pytest
from faq.models import FAQ


@pytest.fixture(scope="function")
def add_faq():
    def _add_faq(check: bool = None):
        if check is None:
            faq = FAQ.objects.create(question="Why it is?", answer="Obama")
            return faq
        else:
            faq = FAQ.objects.create(question="Why it is?", answer="Obama", check=check)
            return faq

    return _add_faq
