from asyncio import Queue
from typing import Self

import pytest_asyncio
from pykit.fcode import FcodeCore

from rxcat import Conn, ConnArgs, ServerBus


@pytest_asyncio.fixture(autouse=True)
async def auto():
    yield

    FcodeCore.deflock = False
    FcodeCore.clean_non_decorator_codes()
    await ServerBus.destroy()

@pytest_asyncio.fixture
async def server_bus() -> ServerBus:
    bus = ServerBus.ie()
    await bus.init()
    return bus

class MockConn(Conn[None]):
    def __init__(self, args: ConnArgs[None]) -> None:
        super().__init__(args)
        self.inp_queue: Queue[dict] = Queue()
        self.out_queue: Queue[dict] = Queue()

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> dict:
        return await self.recv()

    async def recv(self) -> dict:
        return await self.inp_queue.get()

    async def send(self, data: dict):
        await self.out_queue.put(data)

    async def close(self):
        return

    async def client__send(self, data: dict):
        await self.inp_queue.put(data)

    async def client__recv(self) -> dict:
        return await self.out_queue.get()
