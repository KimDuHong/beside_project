import pytest


@pytest.mark.django_db
class TestClass:
    def test_CI(self):
        assert 1 == 1
