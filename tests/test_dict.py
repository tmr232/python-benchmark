from tests.utils import verify


class TestDictLiteralCreation:
    """Compare different methods of creating a dict literal"""

    def test_literal(self, benchmark):
        """Create a dict using a literal"""

        def run():
            return {"a": 1, "b": 2, "c": 3}

        benchmark(run)

    def test_keywords(self, benchmark):
        """Create a dict using keyword arguments"""

        def run():
            return dict(a=1, b=2, c=3)

        benchmark(run)


class TestDictComprehension:
    """Compare different comprehensions for dict creation"""

    VALUES = list(range(100000))

    def test_dict(self, benchmark):
        """Create a dict comprehension"""

        def run():
            return {v: v for v in self.VALUES}

        benchmark(run)

    def test_list(self, benchmark):
        """Create a dict from a list comprehension"""

        def run():
            return dict([(v, v) for v in self.VALUES])

        benchmark(run)

    def test_generator(self, benchmark):
        """Create a dict from a generator comprehension"""

        def run():
            return dict((v, v) for v in self.VALUES)

        benchmark(run)
