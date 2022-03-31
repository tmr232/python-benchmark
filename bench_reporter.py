import json
import operator
import types
from collections import defaultdict
from contextlib import suppress
from pathlib import Path
from typing import Sequence

import rich
import cattrs
import attrs
import typer
from rich.console import Console
from rich.markdown import Markdown
import importlib.util
import sys

from rich.table import Table


@attrs.define
class Stats:
    min: float
    max: float
    mean: float
    stddev: float

@attrs.define
class Benchmark:
    name: str
    fullname: str
    params: dict|None
    stats: Stats

@attrs.define
class BenchmarkSave:
    benchmarks: list[Benchmark]

    @classmethod
    def from_file(cls, file:Path)->"BenchmarkSave":
        raw_data = file.read_text("utf8")
        dict_data = json.loads(raw_data)
        return  cattrs.structure(dict_data, cls)


@attrs.define
class Source:
    module: types.ModuleType
    cls: type
    func: types.MethodType

@attrs.define
class AnnotatedBenchmark:
    benchmark: Benchmark
    source: Source

@attrs.define
class Group:
    module: types.ModuleType
    cls: type
    benchmarks: list[AnnotatedBenchmark] = attrs.field(factory=list)

def import_by_path(name: str, path: str):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return module

def get_source(benchmark:Benchmark)->Source:
    filename, classname, testname = benchmark.fullname.split("::")

    test_module = import_by_path(filename, filename)
    test_class = getattr(test_module, classname)
    testfunc_name, _, _ = testname.partition("[")
    testfunc = getattr(test_class, testfunc_name)

    return Source(module=test_module, cls=test_class, func=testfunc)

def group_benchmarks(benchmarks:Sequence[Benchmark])->Sequence[Group]:
    groups:dict[type, Group] = {}

    for benchmark in benchmarks:
        try:
            source = get_source(benchmark)
        except ValueError:
            continue
        annotated_benchmark = AnnotatedBenchmark(benchmark=benchmark, source=source)
        group = groups.get(source.cls)
        if group:
            group.benchmarks.append(annotated_benchmark)
        else:
            group = Group(module=source.module, cls=source.cls)
            group.benchmarks.append(annotated_benchmark)
            groups[source.cls] = group

    return list(groups.values())

def render_group(group:Group):


    group_doc = group.cls.__doc__


    table = Table(title=group_doc)
    table.add_column("Benchmark")
    table.add_column("Min", justify="right")
    table.add_column("Relative", justify="right")

    benchmarks = sorted(group.benchmarks, key=operator.attrgetter("benchmark.stats.min"))
    base = benchmarks[0].benchmark.stats.min
    for benchmark in benchmarks:
        relative = benchmark.benchmark.stats.min / base
        table.add_row(benchmark.source.func.__doc__, f"{benchmark.benchmark.stats.min:g}", f"{relative:g}")

    console = Console()
    console.print(table)

def main(benchmark_file:Path):
    data = BenchmarkSave.from_file(benchmark_file)

    groups = group_benchmarks(data.benchmarks)
    for group in groups:
        render_group(group)

if __name__ == '__main__':
    typer.run(main)