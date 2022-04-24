from typing import Any, Optional

import attrs
import pytest


@pytest.fixture(
    params=[
        100000,
    ]
)
def set_of_range(request):
    yield set(range(request.param))


@attrs.define
class TestResult:
    nodeid: Optional[str] = None
    result: Any = attrs.field(default=None, repr=False)

    def __bool__(self):
        return self.nodeid is not None


@pytest.fixture(scope="class")
def saved_result():
    return TestResult()
