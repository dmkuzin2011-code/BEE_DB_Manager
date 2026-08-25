import asyncio
from repl import DBRepl


async def main() -> None:
    show_logo()
    await DBRepl().run()
from repl import console,show_logo

if __name__ == "__main__":
    asyncio.run(main())
