from os import getenv
from statistics import mean
from statistics import stdev
from time import perf_counter_ns


def benchmark(n: int):
    if not getenv('ENABLE_BENCHMARK'):
        n = 1

    def _benchmark(f):
        def _helper(*args, **kwargs):
            timing = []
            for _ in range(n):
                start = perf_counter_ns()
                f(*args, **kwargs)
                end = perf_counter_ns()
                timing.append((end - start) // 1000000)

            print()
            print('Statistics:')
            if len(timing) == 1:
                print(f'-> Elapsed: {timing[0]}ms')
            else:
                average = mean(timing)
                deviation = stdev(timing, xbar=average)
                print(f'-> Average: {average}ms')
                print(f'-> StdDev: {deviation}ms')

        return _helper

    return _benchmark
