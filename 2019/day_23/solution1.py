import asyncio
from os import path
from typing import AsyncGenerator
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from ..intcode.executor import run
from ..intcode.io import Reader
from ..intcode.io import Writer
from ..intcode.utils import load
from ..intcode.utils import Program


async def run_network(prog: Program) -> int:
    input_buffers: Dict[int, List[Tuple[int, int]]] = {}

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
                    await asyncio.sleep(0.1)

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
                input_buffers[addr].append((x, val))
                addr = None
                x = None

        return _writer

    async def monitor() -> None:
        # Just watch for address 255 to be written
        # Execution of the network will stop when this monitor terminates
        while len(input_buffers[255]) == 0:
            await asyncio.sleep(0.1)

    programs = [monitor()]
    input_buffers[255] = []
    for net_id in range(50):
        input_buffers[net_id] = []
        programs.append(run(prog.copy(), reader=reader(net_id), writer=writer()))

    await asyncio.wait([asyncio.create_task(p) for p in programs], return_when=asyncio.FIRST_COMPLETED)

    return input_buffers[255][0][1]


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile, 'r') as input_file:
        prog = load(input_file.read())
        result = await run_network(prog)
        print(f'Solution: {result}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
