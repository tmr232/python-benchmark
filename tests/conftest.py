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


@pytest.fixture
def benchmark_and_verify(request, saved_result, benchmark):
    class Benchmark:
        def _check_result(self, function_to_benchmark, *args, **kwargs):
            result = function_to_benchmark(*args, **kwargs)
            nodeid = request.node.nodeid
            if saved_result and saved_result.result != result:
                pytest.fail(reason=f"Result different from {saved_result.nodeid}")
                return
            saved_result.result = result
            saved_result.nodeid = nodeid

        def __call__(self, function_to_benchmark, *args, **kwargs):
            self._check_result(function_to_benchmark, *args, **kwargs)

            return benchmark(function_to_benchmark, *args, **kwargs)

        def pedantic(
            self,
            target,
            args=(),
            kwargs=None,
            setup=None,
            rounds=1,
            warmup_rounds=0,
            iterations=1,
        ):
            self._check_result(target, *args, **(kwargs or {}))

            return benchmark.pedantic(
                target=target,
                args=args,
                kwargs=kwargs,
                setup=setup,
                rounds=rounds,
                warmup_rounds=warmup_rounds,
                iterations=iterations,
            )

    return Benchmark()
