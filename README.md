# Python-Benchmarks

A collection of Python microbenchmarks,
running across multiple OS and Python versions.

You can see the report at https://tmr232.github.io/python-benchmark/

## Current Status

The project is in a very initial state.
It works, it runs, and it produces reports.
But it only contains a small number of benchmarks, 
and the reports are very basic.

You're very welcome to add new benchmarks,
or to help with generating nicer reports.

## Adding Benchmarks

Each benckmark group is a single test-class in the tests.

The docstring of the class is used to provide a description for the group,
and the test-function docstrings are used to name each individual test case.

To add a new benchmark, either add to an existing group, or create a new one.
Make sure you document properly so it will be rendered nicely.

### Example

Say we want to compare list indexing to dict lookups.
We can write the following:

```python
import random


class TestLookup:
    # The class docstring will be used to describe the benchmark.
    # It will be rendered as Markdown.
    # Make sure to leave the first line empty so that indentation
    # can be removed automatically.
    """
    Compare using a list or a dict to index-based lookups.
    """

    # Make sure we generate the indices ahead of time, and not
    # during the benchmarking.
    # If we generate during the benchmark it'll skew the results.
    ACCESS_INDICES = random.sample(range(100_000), 1000)

    def _access(self, list_or_dict):
        for i in self.ACCESS_INDICES:
            _ = list_or_dict[i]

    # All `test_XXX` entries will be compared in the result table.
    def test_list_subscript(self, benchmark):
        # The docstrings will be used to describe the test case in the table.
        """Access list values"""
        list_ = [str(i) for i in range(100_000)]
        benchmark(self._access, list_)

    def test_dict_subscript(self, benchmark):
        """Access dict values"""
        dict_ = {i: str(i) for i in range(100_000)}
        benchmark(self._access, dict_)
```

And that's it. An entry in the table will be generated for us.