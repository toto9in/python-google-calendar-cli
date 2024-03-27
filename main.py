from typing import Optional
import typer
from typing_extensions import Annotated
from rich import print, box
from calendar_utils import get_events
from rich.console import Console
from rich.table import Table, Column


app = typer.Typer(no_args_is_help=True, help="This is a python CLI integrated with Google Calendar.", rich_markup_mode="rich")
events_app = typer.Typer(no_args_is_help=True,help="Create events google calendar or show events google calendar",)
app.add_typer(events_app, name="events")

console = Console()

@events_app.command("create", no_args_is_help=True)
def events_create(event_name: Annotated[str, typer.Argument(help="Name of the event")],
                  description: Annotated[str, typer.Argument(help="Description of the event")]):
    """
    [bold green]Create[/bold green] a new event in Google Calendar
    """
    print(f"Create event {event_name} with description {description}")

@events_app.command("show")
def events_show(filter: Annotated[str, typer.Option(help="Filter to show events that occurs at the actual day or at the week.")] = "today"):
    """
    [bold green]Show[/bold green] events of google calendar
    """
    if filter == "today":
        events = get_events("today")
        if not events:
            print("No events today.")
            return
        table = Table("Summary", Column(header="Status", style="green"), "Date", title="Events of today", show_lines=True, box=box.HEAVY_HEAD) 
        for event in events:
            table.add_row(event['summary'], event['status'], event['start']['dateTime'])
        console.print(table)
    else:
        events = get_events("week")
        if not events:
            print("No events at the week.")
            return
        table = Table("Summary", Column(header="Status", style="green"), "Date", title="Events of the week", show_lines=True, box=box.HEAVY_HEAD) 
        for event in events:
            table.add_row(event['summary'], event['status'], event['start']['dateTime'])
        console.print(table)

if __name__ == "__main__":
    app()