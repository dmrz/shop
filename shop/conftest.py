from collections import UserDict
from unittest.mock import ANY

import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from products.models import Product


class AnyDict(UserDict):
    """
    Returns a dict that will use unittest.mock.ANY
    as a value for keys that present in dict it is
    going to be compared with for equality (or not equality),
    but not in dict itself. It will also ensure that comparing
    dict is just a dict, not OrderedDict or other subtype.
    """

    def _fill_with_any(self, other):
        missing_keys = set(other) - set(self.data)
        self.data = {**self.data, **{key: ANY for key in missing_keys}}

    def __eq__(self, other):
        self._fill_with_any(other)
        return super().__eq__(dict(other))

    def __ne__(self, other):
        self._fill_with_any(other)
        return super().__ne__(dict(other))


@pytest.fixture
def anydict():
    return AnyDict


@pytest.fixture()
def product_factory(faker):
    def factory():
        return Product.objects.create(
            name=faker.catch_phrase(),
            description=faker.text(),
            price=faker.pydecimal(3, 2, True))
    return factory


@pytest.yield_fixture()
def api_client(admin_user):
    client = APIClient()
    # Admin user created implicitly using admin_user fixture
    client.login(username='admin', password='password')
    yield client
    client.logout()


@pytest.fixture()
def reverse_url():
    def _reverse(*args, **kwargs):
        url = reverse(*args, **kwargs)
        return f'http://testserver{url}'
    return _reverse
