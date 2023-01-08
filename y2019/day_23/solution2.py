import asyncio
from collections import Counter
from collections.abc import AsyncGenerator
from os import path
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

from ..intcode.executor import run
from ..intcode.io import Reader
from ..intcode.io import Writer
from ..intcode.utils import load
from ..intcode.utils import Program


async def run_network(prog: Program) -> int:
    input_buffers: dict[int, list[tuple[int, int]]] = {}

    def reader(address: int) -> Reader:
        async def _reader() -> AsyncGenerator[int, None]:
            yield address
            while True:
                if len(input_buffers[address]) != 0:
                    data = input_buffers[address].pop(0)
                    yield data[0]
                    yield data[1]
                else:
                    yield -1
                    # Toss a sleep in here to actually give another program a chance to run
                    await asyncio.sleep(0)

        return _reader

    def writer() -> Writer:
        addr: Optional[int] = None
        x: Optional[int] = None

        async def _writer(val: int) -> None:
            nonlocal addr
            nonlocal x
            if addr is None:
                addr = val
            elif x is None:
                x = val
            else:
                if addr == 255:
                    input_buffers[addr] = [(x, val)]
                else:
                    input_buffers[addr].append((x, val))
                addr = None
                x = None

        return _writer

    async def nat_monitor() -> None:
        y_hist: set[int] = set()

        while True:
            if len(input_buffers[255]) != 0:
                if sum(1 for k, v in input_buffers.items() if k != 255 and len(v) != 0) == 0:
                    # All input buffers are empty - Network is idle
                    data = input_buffers[255][0]
                    if data[1] in y_hist:
                        return
                    y_hist.add(data[1])
                    input_buffers[0].append(data)

            await asyncio.sleep(0)

    programs = [nat_monitor()]
    input_buffers[255] = []
    for net_id in range(50):
        input_buffers[net_id] = []
        programs.append(run(prog.copy(), reader=reader(net_id), writer=writer()))

    await asyncio.wait([asyncio.create_task(p) for p in programs], return_when=asyncio.FIRST_COMPLETED)

    return input_buffers[255][0][1]


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        prog = load(input_file.read())
        result = await run_network(prog)
        print(f"Solution: {result}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
