from asyncio import get_event_loop, sleep
from typing import List, Dict, Union, Optional

from aio_pika import Connection, Channel, Message, connect_robust
from aio_pika.exceptions import QueueEmpty
from orjson import dumps, loads


JSON = Union[List["JSON"], Dict["str", "JSON"], int, float, str, bool, None]


class JSONMessageIterator:
    def __init__(self, channel: Channel, type: str) -> None:
        self._channel = channel
        self._type = type

    async def setup(self) -> None:
        self._queue = await self._channel.declare_queue(self._type, auto_delete=True)

    def __aiter__(self) -> "JSONMessageIterator":
        return self

    async def __anext__(self) -> JSON:
        backoff = 0.011

        while True:
            try:
                message = await self._queue.get(no_ack=True)
                return loads(message.body)  # type: ignore
            except QueueEmpty:
                backoff = min(backoff * 2, 0.25)
                await sleep(backoff)


class RabbitClient:
    def __init__(self, uri: str, type: str) -> None:
        self.uri = uri
        self.type = type

        self._loop = get_event_loop()
        self._connection: Optional[Connection] = None
        self._channel: Optional[Channel] = None

    async def _connect(self) -> None:
        self._connection = await connect_robust(self.uri)
        self._channel = await self._connection.channel()

    async def send(self, data: JSON) -> None:
        if not self._connection:
            await self._connect()

        await self._channel.default_exchange.publish(  # type: ignore
            Message(
                body=dumps(data),
                content_type="application/json",
            ),
            self.type,
        )

    async def iter_json(self) -> JSONMessageIterator:
        if not self._connection:
            await self._connect()

        it = JSONMessageIterator(self._channel, self.type)  # type: ignore
        await it.setup()
        return it
