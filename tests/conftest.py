import pytest
import rich
@pytest.hookimpl(hookwrapper=True)
def pytest_benchmark_group_stats(config, benchmarks, group_by):
    for bench in benchmarks:
        rich.inspect(bench)
        break
    yield


@pytest.fixture(params=[100000,])
def set_of_range(request):
    yield set(range(request.param))