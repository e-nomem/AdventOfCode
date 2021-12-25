from collections.abc import Callable
from os import getenv
from statistics import mean
from statistics import stdev
from time import perf_counter_ns
from typing import Optional

UNITS = (("ns", 1000), ("μs", 1000), ("ms", 1000), ("s", 60), ("m", 60), ("h", 24), ("d", None))


def _format_time(time: int) -> str:
    reduced_time: float = time
    for unit, factor in UNITS:
        if factor is None or not reduced_time / factor > 1:
            break

        reduced_time /= factor

    return f"{reduced_time:.2f} {unit}"


def benchmark(n: int, cleanup: Optional[Callable[[], None]] = None):
    if not getenv("ENABLE_BENCHMARK"):
        n = 1

    def _benchmark(f):
        def _helper(*args, **kwargs):
            timing = []
            for _ in range(n):
                if cleanup is not None:
                    cleanup()

                start = perf_counter_ns()
                f(*args, **kwargs)
                end = perf_counter_ns()
                timing.append(end - start)

            print()
            print("Statistics:")
            if len(timing) == 1:
                print(f"-> Elapsed: {_format_time(timing[0])}")
            else:
                average = mean(timing)
                deviation = stdev(timing, xbar=average)
                print(f"-> Average: {_format_time(average)}")
                print(f"-> StdDev: {_format_time(deviation)}")

        return _helper

    return _benchmark
