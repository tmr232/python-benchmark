import random


class TestLookup:
    """
    Compare using a list or a dict to index-based lookups.
    """

    ACCESS_INDICES = random.sample(range(100_000), 1000)

    def _access(self, list_or_dict):
        for i in self.ACCESS_INDICES:
            _ = list_or_dict[i]

    def test_list_subscript(self, benchmark):
        """Access list values"""
        list_ = [str(i) for i in range(100_000)]
        benchmark(self._access, list_)

    def test_dict_subscript(self, benchmark):
        """Access dict values"""
        dict_ = {i: str(i) for i in range(100_000)}
        benchmark(self._access, dict_)
