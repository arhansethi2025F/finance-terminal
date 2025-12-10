from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, TabbedContent, TabPane
from textual.containers import Vertical
from quote_widget import QuoteDisplay
from watchlist_widget import WatchlistTable

class FinanceTerminal(App):
    """A simple finance terminal"""
    
    CSS = """
    Screen {
        background: #0e1117;
    }
    
    #quote-display {
        height: 12;
        border: solid green;
        padding: 1;
        margin: 1;
    }
    
    .input-container {
        margin: 1;
    }
    
    DataTable {
        height: 100%;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with TabbedContent():
            with TabPane("Quote", id="quote-tab"):
                yield Vertical(
                    Input(placeholder="Enter ticker symbol (e.g., AAPL)", id="ticker-input", classes="input-container"),
                    QuoteDisplay("Enter a ticker symbol to get started", id="quote-display"),
                )
            
            with TabPane("Watchlist", id="watchlist-tab"):
                yield Vertical(
                    Input(placeholder="Enter ticker to add to watchlist", id="watchlist-input", classes="input-container"),
                    WatchlistTable(id="watchlist-table"),
                )
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Set up auto-refresh timer when app starts"""
        # Update every 2 seconds
        self.set_interval(2, self.auto_refresh)
    
    def auto_refresh(self) -> None:
        """Automatically refresh the quote and watchlist"""
        try:
            # Refresh single quote
            quote_display = self.query_one("#quote-display", QuoteDisplay)
            quote_display.refresh_current_ticker()
            
            # Refresh watchlist
            watchlist_table = self.query_one("#watchlist-table", WatchlistTable)
            watchlist_table.refresh_watchlist()
        except Exception as e:
            # Handle any errors gracefully
            pass
    
    def action_refresh(self) -> None:
        """Manual refresh action (when user presses 'r')"""
        self.auto_refresh()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle ticker input"""
        ticker = event.value.strip().upper()
        
        if not ticker:
            return
        
        if event.input.id == "ticker-input":
            # Single quote view
            quote_display = self.query_one("#quote-display", QuoteDisplay)
            quote_display.update_quote(ticker)
        
        elif event.input.id == "watchlist-input":
            # Watchlist view
            watchlist_table = self.query_one("#watchlist-table", WatchlistTable)
            watchlist_table.add_ticker(ticker)
            event.input.value = ""  # Clear input after adding

if __name__ == "__main__":
    app = FinanceTerminal()
    app.run()
