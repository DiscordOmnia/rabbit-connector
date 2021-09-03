# rabbit-connector

A simple wrapper around RabbitMQ to allow sending and iterating over JSON messages.

## Installation

`pip3 install git+https://github.com/DiscordOmnia/rabbit-connector`

## Basic Usage

Simple Producer:

```py
from asyncio import get_event_loop, sleep

from rabbit_connector import RabbitClient


loop = get_event_loop()

async def main():
    client = RabbitClient("amqp://guest:guest@localhost", "my_routing_key")
    count = 0

    while True:
        await sleep(1)
        count += 1

        await client.send({"count": count})

loop.run_until_complete(main())
```

Simple Consumer:

```py
from asyncio import get_event_loop

from rabbit_connector import RabbitClient


loop = get_event_loop()

async def main():
    client = RabbitClient("amqp://guest:guest@localhost", "my_routing_key")

    iterator = await client.iter_json()

    async for message in iterator:
        print(message)

loop.run_until_complete(main())
```
