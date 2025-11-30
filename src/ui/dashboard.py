"""Terminal dashboard using Textual."""

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Footer, Header, Static

from ..core.logger import get_logger

logger = get_logger()


class Dashboard(App):
    """A simple Textual dashboard for the data platform."""

    CSS_PATH = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(Static("Data Platform Dashboard", id="title"))


if __name__ == "__main__":
    Dashboard().run()
