from tests.utils import verify


@verify
class TestTupleComprehension:
    """
    Compare various ways to write "tuple comprehensions"
    """

    DATA = list(range(1000000))

    def test_generator_comprehension(self, benchmark):
        """tuple from generator comprehension"""

        def run(data):
            return tuple(x for x in data)

        benchmark(run, self.DATA)

    def test_list_comprehension(self, benchmark):
        """tuple from list comprehension"""

        def run(data):
            return tuple([x for x in data])

        benchmark(run, self.DATA)
