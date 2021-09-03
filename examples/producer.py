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
