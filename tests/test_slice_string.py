import operator
import re

from tests.utils import verify, pedantic


@verify
@pedantic(iterations=50, rounds=20_000)
class TestPairs3:
    """
    Try and optimiza splitting a 6-character string into a tuple
    of 3 2-character strings.

    This is based on [Will McGugan](https://twitter.com/willmcgugan)'s
    [tweet](https://twitter.com/willmcgugan/status/1510158982660378626).
    """

    TEXT = "ABCDEF"

    def test_pairs3_slice(self, benchmark):
        """Split the string using simple slices"""

        def split(text):
            return text[0:2], text[2:4], text[4:6]

        benchmark(split, self.TEXT)

    def test_pairs3_re(self, benchmark):
        """Split the string using regex"""

        def split(text, _match=re.compile(r"(..)(..)(..)").match):
            return _match(text).groups()

        benchmark(split, self.TEXT)

    def test_pairs3_slice_cached(self, benchmark):
        """Split the string using cached slices"""

        def split(text, group1=slice(0, 2), group2=slice(2, 4), group3=slice(4, 6)):
            return text[group1], text[group2], text[group3]

        benchmark(split, self.TEXT)

    def test_pairs3_cached_itemgetter(self, benchmark):
        """Split the string using a cached itemgetter"""

        split = operator.itemgetter(slice(0, 2), slice(2, 4), slice(4, 6))

        benchmark(split, self.TEXT)
