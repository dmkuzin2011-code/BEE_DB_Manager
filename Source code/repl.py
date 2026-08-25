from __future__ import annotations

import shlex
from typing import Any, Optional

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.history import InMemoryHistory
from rich.console import Console
from rich.table import Table

from db_adapters import ADAPTERS, DBAdapter

console = Console()


def show_logo() -> None:
    console.print(
        r"""[yellow]
            ⠐⠂⣄⣠⠐⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⢀⣀ ⠘⠛⠛⠃⠀⣀⡀⠀⠀ ⣀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠓⢄⣀⣀⣀⡠⠌⠀⢾⡷⠀⠡⢄⣀⣀⣀⡠⠚⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠯⠤⠒⣡⠆⠀⠀⠰⣌⠒⠤⠽⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠸⠿⠿⠇⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠸⠿⠿⠇⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⠟⠀ Bee Db Manager⠀
                [/yellow]"""
    )


class DBRepl:
    def __init__(self) -> None:
        self.adapter: Optional[DBAdapter] = None
        self.kind: Optional[str] = None
        completer = NestedCompleter.from_nested_dict(
            {
                "connect": {k: None for k in ADAPTERS},
                "disconnect": None,
                "help": None,
                "exit": None,
                "quit": None,
            }
        )
        self.session = PromptSession(history=InMemoryHistory(), completer=completer)

    def print_result(self, result: Any) -> None:
        if isinstance(result, list) and result and isinstance(result[0], dict):
            table = Table(show_header=True, header_style="bold cyan")
            for key in result[0].keys():
                table.add_column(str(key))
            for row in result:
                table.add_row(*[str(v) for v in row.values()])
            console.print(table)
        elif isinstance(result, dict):
            console.print(result)
        else:
            console.print(result)

    async def handle(self, line: str) -> bool:
        is_json = line.strip().startswith("{")
        parts = [line] if is_json else shlex.split(line, posix=True)
        if not parts:
            return True

        first = parts[0]

        if first in ("exit", "quit"):
            return False

        if first == "help":
            table = Table(
                title="Bee DB Manager - Command Reference",
                show_header=True,
                header_style="bold magenta",
            )
            table.add_column("Command", style="bold cyan", no_wrap=True)
            table.add_column("Description", style="green")
            table.add_column("Syntax / Example", style="yellow")
            table.add_row(
                "connect",
                "Establish a connection to a database",
                "connect <postgres|mysql|mongo> <url>",
            )
            table.add_row("disconnect", "Close the active database connection", "disconnect")
            table.add_row("help", "Display available commands and usage guide", "help")
            table.add_row("exit / quit", "Close the session and exit the application", "exit")
            table.add_row(
                "<SQL Command>",
                "Execute raw SQL queries (PostgreSQL / MySQL)",
                "SELECT * FROM users;\nCREATE TABLE test (id INT);",
            )
            table.add_row(
                "<JSON Command>",
                "Execute MongoDB commands formatted as JSON",
                '{"ping": 1}\n{"find": "users", "filter": {}}',
            )
            console.print(table)
            return True

        if first == "connect":
            if len(parts) < 3:
                console.print("[red]Usage: connect <postgres|mysql|mongo> <url>[/red]")
                return True
            kind, url = parts[1], parts[2]
            if kind not in ADAPTERS:
                console.print(f"[red]Unknown type: {kind}[/red]")
                return True
            adapter = ADAPTERS[kind]()
            try:
                await adapter.connect(url)
            except Exception as e:
                console.print(f"[red]Connection error: {e}[/red]")
                return True
            # close previous connection if any
            if self.adapter is not None:
                await self.adapter.close()
            self.adapter = adapter
            self.kind = kind
            console.print(f"[green]Connected: {kind}[/green]")
            return True

        if first == "disconnect":
            if self.adapter is not None:
                await self.adapter.close()
                self.adapter = None
                self.kind = None
                console.print("[yellow]Disconnected[/yellow]")
            else:
                console.print("[yellow]Not connected[/yellow]")
            return True

        if self.adapter is None:
            console.print("[red]Connect first[/red]")
            return True

        try:
            result = await self.adapter.execute(line)
            self.print_result(result)
        except Exception as e:
            console.print(f"[red]{e}[/red]")

        return True

    async def run(self) -> None:
        while True:
            prompt_label = f"{self.kind or 'db'}> "
            try:
                line = await self.session.prompt_async(prompt_label)
            except (KeyboardInterrupt, EOFError):
                break
            line = line.strip()
            if not line:
                continue
            keep_going = await self.handle(line)
            if not keep_going:
                break
        if self.adapter is not None:
            await self.adapter.close()
