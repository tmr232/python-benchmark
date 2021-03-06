import collections
import dataclasses
import typing

import attrs


class TestBasicClassInit:
    """Compare initialization of different class types.
    The idea is to compare attrs, dataclasses, and plain classes"""

    def test_plain(self, benchmark):
        """Initialize a plain class"""

        class Person:
            def __init__(self, name, age):
                self.name = name
                self.age = age

        benchmark(Person, "Arthur", 42)

    def test_plain_with_slots(self, benchmark):
        """Initialize a plain class with slots"""

        class Person:
            __slots__ = ["name", "age"]

            def __init__(self, name, age):
                self.name = name
                self.age = age

        benchmark(Person, "Arthur", 42)

    def test_attrs(self, benchmark):
        """Initialize an attrs class"""

        @attrs.define
        class Person:
            name: str
            age: int

        benchmark(Person, "Arthur", 42)

    def test_attrs_frozen(self, benchmark):
        """Initialize a frozen attrs class"""

        @attrs.frozen
        class Person:
            name: str
            age: int

        benchmark(Person, "Arthur", 42)

    def test_dataclass(self, benchmark):
        """Initialize a dataclass"""

        @dataclasses.dataclass
        class Person:
            name: str
            age: int

        benchmark(Person, "Arthur", 42)

    def test_typing_namedtuple(self, benchmark):
        """Initialize a typing.NamedTuple class"""

        class Person(typing.NamedTuple):
            name: str
            age: int

        benchmark(Person, "Arthur", 42)

    def test_collections_namedtuple(self, benchmark):
        """Initialize a collections.namedtuple class"""

        Person = collections.namedtuple("Person", "name age")

        benchmark(Person, "Arthur", 42)

    if hasattr(typing, "TypedDict"):
        # Requires Python >=3.8
        def test_typeddict(self, benchmark):
            """Initialize a typing.TypedDict"""

            class Person(typing.TypedDict):
                name: str
                age: int

            benchmark(Person, name="Arthur", age=42)


class TestBasicClassMemberAccess:
    """Compare member access of different class types.
    The idea is to compare attrs, dataclasses, and plain classes"""

    def test_plain(self, benchmark):
        """Access members of a plain class"""

        class Person:
            def __init__(self, name, age):
                self.name = name
                self.age = age

        p = Person("Arthur", 42)

        def run():
            p.name
            p.age

        benchmark(run)

    def test_plain_with_slots(self, benchmark):
        """Access members of a plain class with slots"""

        class Person:
            __slots__ = ["name", "age"]

            def __init__(self, name, age):
                self.name = name
                self.age = age

        def run(p=Person("Arthur", 42)):
            p.name
            p.age

        benchmark(run)

    def test_attrs(self, benchmark):
        """Access members of an attrs class"""

        @attrs.define
        class Person:
            name: str
            age: int

        def run(p=Person("Arthur", 42)):
            p.name
            p.age

        benchmark(run)

    def test_attrs_frozen(self, benchmark):
        """Access members of a frozen attrs class"""

        @attrs.frozen
        class Person:
            name: str
            age: int

        def run(p=Person("Arthur", 42)):
            p.name
            p.age

        benchmark(run)

    def test_dataclass(self, benchmark):
        """Access members of a dataclass"""

        @dataclasses.dataclass
        class Person:
            name: str
            age: int

        def run(p=Person("Arthur", 42)):
            p.name
            p.age

        benchmark(run)

    def test_typing_namedtuple(self, benchmark):
        """Access members of a typing.NamedTuple class"""

        class Person(typing.NamedTuple):
            name: str
            age: int

        def run(p=Person("Arthur", 42)):
            p.name
            p.age

        benchmark(run)

    def test_collections_namedtuple(self, benchmark):
        """Access members of a collections.namedtuple class"""

        Person = collections.namedtuple("Person", "name age")

        def run(p=Person("Arthur", 42)):
            p.name
            p.age

        benchmark(run)
