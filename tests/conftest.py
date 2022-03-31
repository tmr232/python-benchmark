import pytest


@pytest.fixture(
    params=[
        100000,
    ]
)
def set_of_range(request):
    yield set(range(request.param))
