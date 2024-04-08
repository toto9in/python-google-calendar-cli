from typing import Optional
import typer
from typing_extensions import Annotated
from rich import print, box
from calendar_utils import get_events, create_events
from rich.console import Console
from rich.table import Table, Column


app = typer.Typer(no_args_is_help=True, help="This is a python CLI integrated with Google Calendar.", rich_markup_mode="rich")
events_app = typer.Typer(no_args_is_help=True,help="Create events google calendar or show events google calendar",)
app.add_typer(events_app, name="events")

console = Console()

@events_app.command("create", no_args_is_help=True)
def events_create(event_name: Annotated[str, typer.Argument(help="Name of the event")],
                  start_date_time: Annotated[str, typer.Argument(help="Start date of the event")],
                  end_date_time: Annotated[str, typer.Argument(help="End date of the event")],
                  description: Annotated[str, typer.Option(help="Description of the event")] = ""):
    """
    [bold green]Create[/bold green] a new event in Google Calendar

    start_date and end_date must be in the format: yyyy-mm-ddThh:mm:ss
    end_date must be greater than start_date (format: yyyy-mm-ddThh:mm:ss)
    example of start_date and end_date: 2024-04-08T12:30:00
    """
    create_events(event_name=event_name, start_date_time=start_date_time, end_date_time=end_date_time, description=description)

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
        table = Table("Summary", Column(header="Status", style="green"), "Description", "Date", title="Events of today", show_lines=True, box=box.HEAVY_HEAD) 
        for event in events:
            if 'description' not in event:
                event['description'] = "No description"
            table.add_row(event['summary'], event['status'], event['description'], event['start']['dateTime'])
        console.print(table)
    else:
        events = get_events("week")
        if not events:
            print("No events at the week.")
            return
        table = Table("Summary", Column(header="Status", style="green"), "Description", "Date", title="Events of the week", show_lines=True, box=box.HEAVY_HEAD)
        for event in events:
            if 'description' not in event:
                event['description'] = "No description"
            table.add_row(event['summary'], event['status'], event['description'],  event['start']['dateTime'])
        console.print(table)

@events_app.command("user-data")
def user_data():
    """
    [bold green]Show[/bold green] user data
    """

    


if __name__ == "__main__":
    app()