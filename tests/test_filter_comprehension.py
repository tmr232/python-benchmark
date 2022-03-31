
class TestFilter:
    def test_list_compregension_only(self, benchmark, set_of_range):
        """Filter in the comprehension"""
        def run():
            for _ in [x for x in set_of_range if True]:
                pass
        benchmark(run)

    def test_filter_list_comprehension(self, benchmark, set_of_range):
        """Use filter on list comprehension"""
        def run():
            for _ in filter(lambda _: True, [x for x in set_of_range]):
                pass

        benchmark(run)


    def test_filter_generator_comprehension(self, benchmark, set_of_range):
        """Use filter on generator comprehension"""
        def run():
            for _ in filter(lambda _: True, (x for x in set_of_range)):
                pass

        benchmark(run)