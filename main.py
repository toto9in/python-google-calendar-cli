from typing import Optional
import typer
from typing_extensions import Annotated
from rich import print

app = typer.Typer(no_args_is_help=True, help="This is a python CLI integrated with Google Calendar.")
events_app = typer.Typer(no_args_is_help=True,help="Create events google calendar or show events google calendar")
app.add_typer(events_app, name="events")


@events_app.command("create")
def items_create(name: str, description: str):
    """
    Create a new event in Google Calendar
    
    Args:
        name (str): Name of the event
        description (str): Description of the event
        
    mudar para usar os types para no terminal ficar bonitinho

    """
    print(f"Create event {name} with description {description}")

@events_app.command("show")


def items_show(filter: Optional[str] = None):
    """
    Show events of google calendar
    """
    if Optional:
        print("Show events google calendar with filter")
    print("Show events google calendar")


if __name__ == "__main__":
    app()