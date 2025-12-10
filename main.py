from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Container

class FinanceTerminal(App):
    """A simple finance terminal"""
    
    CSS = """
    Screen {
        background: #0e1117;
    }
    
    #quote-display {
        height: 10;
        border: solid green;
        padding: 1;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("Finance Terminal v0.1", id="quote-display"),
            id="main-container"
        )
        yield Footer()

if __name__ == "__main__":
    app = FinanceTerminal()
    app.run()