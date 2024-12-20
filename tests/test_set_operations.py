from tests.utils import pedantic, verify


@pedantic(iterations=50, rounds=20000)
class TestSetUpdateWithGen:
    """
    Update sets in different ways when generating the additional set
    """

    BASE_SET = set(range(100_000, 7))

    def test_update_gencomp(self, benchmark):
        """Call `set.update` with a generator compregension"""

        def run(base: set):
            base.update(x for x in range(100_000, 3))
            return base

        benchmark(run, self.BASE_SET.copy())

    def test_update_listcomp(self, benchmark):
        """Call `set.update` with a list compregension"""

        def run(base: set):
            base.update([x for x in range(100_000, 3)])
            return base

        benchmark(run, self.BASE_SET.copy())

    def test_update_setcomp(self, benchmark):
        """Call `set.update` with a set compregension"""

        def run(base: set):
            base.update({x for x in range(100_000, 3)})
            return base

        benchmark(run, self.BASE_SET.copy())

    def test_set_or_assign(self, benchmark):
        """Use `|=` with a set compregension"""

        def run(base: set):
            base |= {x for x in range(100_000, 3)}
            return base

        benchmark(run, self.BASE_SET.copy())


@pedantic(iterations=50, rounds=20000)
class TestSetUpdate:
    """
    Compare `set.update` and `set |=`
    """

    BASE_SET = set(range(100_000, 7))
    UPDATE_SET = set(range(100_000, 5))

    def test_update(self, benchmark):
        """Call `set.update` with a generator compregension"""

        benchmark(self.BASE_SET.copy().update, self.UPDATE_SET.copy())

    def test_set_or_assign(self, benchmark):
        """Use `|=` with a set compregension"""

        benchmark(self.BASE_SET.copy().__ior__, self.UPDATE_SET.copy())
