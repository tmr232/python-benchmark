"""
Various tests relating to set access.
"""




class TestSetAccess:
    """
    Get any item from set

    In this case we want to get a single element out of a set.
    It does not matter which element, but we need one.
    """


    def test_set_list_subscript(self, benchmark, set_of_range):
        """Get a member by converting to a list first"""
        def run():
            _ = list(set_of_range)[0]

        benchmark(run)

    def test_set_iter_next(self, benchmark, set_of_range):
        """Get an item by using iter and next"""
        def run():
            _ = next(iter(set_of_range))

        benchmark(run)