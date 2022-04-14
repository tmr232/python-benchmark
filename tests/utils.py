import pytest


class Verify:
    @pytest.fixture
    def benchmark(self, benchmark_and_verify):
        return benchmark_and_verify
