from textual.widgets import Static
import yfinance as yf

class QuoteDisplay(Static):
    """Widget to display stock quotes"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_ticker = None
        self.last_price = None  # Track previous price
    
    def update_quote(self, ticker: str):
        self.current_ticker = ticker
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            current_price = info.get('currentPrice', 'N/A')
            prev_close = info.get('previousClose', 'N/A')
            
            if current_price != 'N/A' and prev_close != 'N/A':
                change = current_price - prev_close
                change_pct = (change / prev_close) * 100
                change_color = "green" if change >= 0 else "red"
                
                # Determine price color based on movement
                if self.last_price is not None:
                    if current_price > self.last_price:
                        price_color = "green"
                    elif current_price < self.last_price:
                        price_color = "red"
                    else:
                        price_color = "white"
                else:
                    price_color = "white"
                
                # Store current price for next comparison
                self.last_price = current_price
                
                quote_text = f"""
[bold]{ticker.upper()}[/bold]
Price: [bold {price_color}]${current_price:.2f}[/bold {price_color}]
Change: [{change_color}]{change:+.2f} ({change_pct:+.2f}%)[/{change_color}]
Previous Close: ${prev_close:.2f}
                """
            else:
                quote_text = f"Could not fetch data for {ticker}"
                
            self.update(quote_text)
        except Exception as e:
            self.update(f"Error: {str(e)}")
    
    def refresh_current_ticker(self):
        """Refresh the current ticker's data"""
        if self.current_ticker:
            self.update_quote(self.current_ticker)