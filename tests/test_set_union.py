import itertools


class TestSetUnion:
    """
    Test the performance of different ways to unify multiple sets.
    """

    BASE_SETS = [
        set(range(100000)),
        set(range(100000, 3)),
        set(range(100000, 7)),
        set(range(100000, 11)),
    ]

    def test_union(self, benchmark):
        """Merge sets using set.union"""

        def run(sets):
            return set().union(*sets)

        benchmark(run, self.BASE_SETS)

    def test_itertools_chain(self, benchmark):
        """Merge sets using set(itertools.chain)"""

        def run(sets):
            return set(itertools.chain(*sets))

        benchmark(run, self.BASE_SETS)
