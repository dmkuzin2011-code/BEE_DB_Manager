import asyncio

from repl import DBRepl, show_logo


async def main() -> None:
    show_logo()
    await DBRepl().run()


if __name__ == "__main__":
    asyncio.run(main())
