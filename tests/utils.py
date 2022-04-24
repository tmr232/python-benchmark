from typing import Optional

import attrs
import pytest

CONFIG_NAME = "__benchmark_config__"


def get_custom_benchmark(cls):
    @pytest.fixture(name="benchmark")
    def custom_benchmark(self, request, saved_result, benchmark):
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

                config: BenchmarkConfig = getattr(cls, "__benchmark_config__", None)
                if config:
                    if config.verify:
                        self._check_result(function_to_benchmark, *args, **kwargs)
                    return benchmark.pedantic(
                        target=function_to_benchmark,
                        rounds=config.rounds,
                        iterations=config.iterations,
                        args=args,
                        kwargs=kwargs,
                    )
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

    return custom_benchmark


def customize_benchmark(cls):
    benchmark = get_custom_benchmark(cls)
    setattr(cls, "benchmark", benchmark)


@attrs.define
class BenchmarkConfig:
    iterations: int = 1
    rounds: int = 1
    verify: bool = False


def update_config(cls, **changes):
    old = getattr(cls, CONFIG_NAME, BenchmarkConfig())
    new = attrs.evolve(old, **changes)
    setattr(cls, CONFIG_NAME, new)


def verify(cls: type):
    customize_benchmark(cls)
    update_config(cls, verify=True)

    return cls


def pedantic(*, iterations: Optional[int] = None, rounds: Optional[int] = None):
    def decorator(cls):
        customize_benchmark(cls)
        update_config(cls, iterations=iterations, rounds=rounds)
        return cls

    return decorator
