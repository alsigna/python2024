import asyncio

from scrapli_replay.server.server import start


async def main() -> None:
    await start(
        port=2022,
        collect_data="collector_session_dump_192.168.122.101.yaml",
    )


if __name__ == "__main__":
    asyncio.run(main())
    # loop = asyncio.new_event_loop()
    # try:
    #     loop.run_until_complete(main())
    #     loop.run_forever()
    # finally:
    #     loop.close()
