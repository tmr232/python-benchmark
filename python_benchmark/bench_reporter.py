import inspect
import json
import operator
import os
import textwrap
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
from jinja2 import Environment, PackageLoader
from markdown_it import MarkdownIt


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
    params: dict | None
    stats: Stats


@attrs.define
class MachineInfo:
    python_implementation: str
    python_version: str
    system: str
    release: str


@attrs.define
class BenchmarkSave:
    benchmarks: list[Benchmark]
    machine_info: MachineInfo

    @classmethod
    def from_file(cls, file: Path) -> "BenchmarkSave":
        raw_data = file.read_text("utf8")
        dict_data = json.loads(raw_data)
        return cattrs.structure(dict_data, cls)


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
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def get_source(benchmark: Benchmark) -> Source:
    filename, classname, testname = benchmark.fullname.split("::")

    test_module = import_by_path(filename, filename)
    test_class = getattr(test_module, classname)
    testfunc_name, _, _ = testname.partition("[")
    testfunc = getattr(test_class, testfunc_name)

    return Source(module=test_module, cls=test_class, func=testfunc)


def group_benchmarks(benchmarks: Sequence[Benchmark]) -> Sequence[Group]:
    groups: dict[type, Group] = {}

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


def render_group(group: Group):
    group_doc = group.cls.__doc__

    table = Table(title=group_doc)
    table.add_column("Benchmark")
    table.add_column("Min", justify="right")
    table.add_column("Relative", justify="right")

    benchmarks = sorted(
        group.benchmarks, key=operator.attrgetter("benchmark.stats.min")
    )
    base = benchmarks[0].benchmark.stats.min
    for benchmark in benchmarks:
        relative = benchmark.benchmark.stats.min / base
        table.add_row(
            benchmark.source.func.__doc__,
            f"{benchmark.benchmark.stats.min:g}",
            f"{relative:g}",
        )

    console = Console()
    console.print(table)


@attrs.define
class DisplayBenchmark:
    name: str
    min: str
    scaled: str
    link: str | None


@attrs.define
class DisplayGroup:
    name: str
    description: str
    benchmarks: list[DisplayBenchmark]


def render_docstring(doc: str | None) -> str:
    if not doc:
        return ""
    doc = textwrap.dedent(doc)
    return MarkdownIt("gfm-like").render(doc)


def render_groups_html(
    groups: Sequence[Group],
    machine_info: MachineInfo,
    link_base: str | None = None,
):
    display_groups = []
    for group in groups:
        benchmarks = sorted(
            group.benchmarks, key=operator.attrgetter("benchmark.stats.min")
        )
        display_benchmarks = []
        base = benchmarks[0].benchmark.stats.min
        for benchmark in benchmarks:
            relative = benchmark.benchmark.stats.min / base
            display_benchmarks.append(
                DisplayBenchmark(
                    name=benchmark.source.func.__doc__,
                    min=f"{benchmark.benchmark.stats.min:g}",
                    scaled=f"{relative:g}",
                    link=get_link(link_base, benchmark.source) if link_base else None,
                )
            )

        display_group = DisplayGroup(
            name=group.cls.__name__,
            description=render_docstring(group.cls.__doc__),
            benchmarks=display_benchmarks,
        )
        display_groups.append(display_group)

    info = {
        "Python Implementation": machine_info.python_implementation,
        "Python Version": machine_info.python_version,
        "Operating System": f"{machine_info.system} {machine_info.release}",
    }.items()

    env = Environment(loader=PackageLoader("python_benchmark", "templates"))
    template = env.get_template("report.html.jinja2")
    return template.render(groups=display_groups, info=info)


app = typer.Typer()


@app.command()
def single_html(benchmark_file: Path, out: Path):
    data = BenchmarkSave.from_file(benchmark_file)

    groups = group_benchmarks(data.benchmarks)

    out.write_text(render_groups_html(groups, data.machine_info), "utf8")


@app.command()
def single_file(benchmark_file: Path):
    data = BenchmarkSave.from_file(benchmark_file)

    groups = group_benchmarks(data.benchmarks)
    for group in groups:
        render_group(group)


@app.command()
def directory(benchmark_dir: Path):
    for file in benchmark_dir.glob("**/*.json"):
        print(file)
        single_file(file)


def get_link(base: str, source: Source) -> str:
    # This is truly terrible. But I want to see that it works.
    lines, start = inspect.getsourcelines(source.func)
    end = start + len(lines) - 1
    path = source.module.__name__
    base = base.rstrip("/")
    return f"{base}/{path}#L{start}-L{end}="


@app.command()
def directory_html(
    benchmark_dir: Path,
    out_dir: Path,
    repo_base_url: str | None = None,
):
    out_dir.mkdir(exist_ok=True)

    files_to_process = []
    for root, dirs, files in os.walk(benchmark_dir):
        if not files:
            continue
        last = sorted(files)[-1]
        files_to_process.append(Path(root, last))

    saves = [BenchmarkSave.from_file(file) for file in files_to_process]
    names = []
    for save in saves:
        name = f"{save.machine_info.system}-{save.machine_info.python_implementation}-{save.machine_info.python_version}.html"
        names.append(name)

        groups = group_benchmarks(save.benchmarks)
        (out_dir / name).write_text(
            render_groups_html(groups, save.machine_info, link_base=repo_base_url),
            "utf8",
        )
        print(f"Written report to {out_dir / name}")

    env = Environment(loader=PackageLoader("python_benchmark", "templates"))
    template = env.get_template("index.html.jinja2")
    (out_dir / "index.html").write_text(template.render(names=sorted(names)), "utf8")
    print(f"Written index to {out_dir / 'index.html'}")


if __name__ == "__main__":
    app()
