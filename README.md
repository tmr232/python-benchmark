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