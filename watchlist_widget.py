from textual.widgets import DataTable
import yfinance as yf
import json
import os

class WatchlistTable(DataTable):
    """DataTable for displaying watchlist"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.watchlist_file = "watchlist.json"
        self.ticker_rows = {}
    
    def on_mount(self) -> None:
        """Set up the table columns"""
        self.add_columns("Ticker", "Price")
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.load_watchlist()
    
    def load_watchlist(self):
        """Load watchlist from JSON file"""
        if os.path.exists(self.watchlist_file):
            try:
                with open(self.watchlist_file, 'r') as f:
                    tickers = json.load(f)
                    for ticker in tickers:
                        self.add_ticker(ticker, save=False)
            except Exception as e:
                pass
    
    def save_watchlist(self):
        """Save watchlist to JSON file"""
        tickers = list(self.ticker_rows.keys())
        try:
            with open(self.watchlist_file, 'w') as f:
                json.dump(tickers, f)
        except Exception as e:
            pass
    
    def add_ticker(self, ticker: str, save=True):
        """Add a ticker to the watchlist"""
        ticker = ticker.upper()
        
        if ticker in self.ticker_rows:
            return
        
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            current_price = info.get('currentPrice', 0)
            
            if current_price:
                row_key = self.add_row(
                    ticker,
                    f"${current_price:.2f}"
                )
                
                self.ticker_rows[ticker] = row_key
                
                if save:
                    self.save_watchlist()
        except Exception as e:
            pass