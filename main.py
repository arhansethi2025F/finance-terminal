from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input
from textual.containers import Container, Vertical
import yfinance as yf

class QuoteDisplay(Static):
    """Widget to display stock quotes"""
    
    def update_quote(self, ticker: str):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            current_price = info.get('currentPrice', 'N/A')
            prev_close = info.get('previousClose', 'N/A')
            
            if current_price != 'N/A' and prev_close != 'N/A':
                change = current_price - prev_close
                change_pct = (change / prev_close) * 100
                color = "green" if change >= 0 else "red"
                
                quote_text = f"""
[bold]{ticker.upper()}[/bold]
Price: ${current_price:.2f}
Change: [{color}]{change:+.2f} ({change_pct:+.2f}%)[/{color}]
Previous Close: ${prev_close:.2f}
                """
            else:
                quote_text = f"Could not fetch data for {ticker}"
                
            self.update(quote_text)
        except Exception as e:
            self.update(f"Error: {str(e)}")

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
    
    #ticker-input {
        margin: 1;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Input(placeholder="Enter ticker symbol (e.g., AAPL)", id="ticker-input"),
            QuoteDisplay("Enter a ticker symbol to get started", id="quote-display"),
        )
        yield Footer()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle ticker input"""
        ticker = event.value.strip().upper()
        if ticker:
            quote_display = self.query_one("#quote-display", QuoteDisplay)
            quote_display.update_quote(ticker)

if __name__ == "__main__":
    app = FinanceTerminal()
    app.run()