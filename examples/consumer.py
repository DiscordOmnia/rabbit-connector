from asyncio import get_event_loop

from rabbit_connector import RabbitClient

loop = get_event_loop()


async def main():
    client = RabbitClient("amqp://guest:guest@localhost", "my_routing_key")

    iterator = await client.iter_json()

    async for message in iterator:
        print(message)


loop.run_until_complete(main())
