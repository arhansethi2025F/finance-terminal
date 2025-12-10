from textual.widgets import DataTable
import yfinance as yf
import json
import os
from datetime import datetime

class WatchlistTable(DataTable):
    """DataTable for displaying watchlist"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.watchlist_file = "watchlist.json"
        self.price_history = {}  # Track price changes for coloring
    
    def on_mount(self) -> None:
        """Set up the table columns"""
        self.add_columns("Ticker", "Price", "Change", "% Change")
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.load_watchlist()
        print(f"[{datetime.now()}] Watchlist mounted with {len(self.rows)} rows")
    
    def load_watchlist(self):
        """Load watchlist from JSON file"""
        if os.path.exists(self.watchlist_file):
            try:
                with open(self.watchlist_file, 'r') as f:
                    tickers = json.load(f)
                    print(f"Loaded tickers: {tickers}")
                    for ticker in tickers:
                        self.add_ticker(ticker, save=False)
            except Exception as e:
                print(f"Error loading watchlist: {e}")
    
    def save_watchlist(self):
        """Save watchlist to JSON file"""
        tickers = [self.get_row(row_key)[0] for row_key in self.rows]
        try:
            with open(self.watchlist_file, 'w') as f:
                json.dump(tickers, f)
        except Exception as e:
            print(f"Error saving watchlist: {e}")
    
    def add_ticker(self, ticker: str, save=True):
        """Add a ticker to the watchlist"""
        ticker = ticker.upper()
        
        # Check if ticker already exists
        for row_key in self.rows:
            if self.get_row(row_key)[0] == ticker:
                print(f"Ticker {ticker} already exists")
                return  # Already exists
        
        try:
            print(f"Adding ticker: {ticker}")
            stock = yf.Ticker(ticker)
            info = stock.info
            current_price = info.get('currentPrice', 0)
            prev_close = info.get('previousClose', 0)
            
            if current_price and prev_close:
                change = current_price - prev_close
                change_pct = (change / prev_close) * 100
                
                self.add_row(
                    ticker,
                    f"${current_price:.2f}",
                    f"{change:+.2f}",
                    f"{change_pct:+.2f}%"
                )
                
                # Initialize price history
                self.price_history[ticker] = current_price
                
                if save:
                    self.save_watchlist()
                    
                print(f"Successfully added {ticker} at ${current_price:.2f}")
        except Exception as e:
            print(f"Error adding ticker {ticker}: {e}")
    
    def refresh_watchlist(self):
        """Refresh all ticker data in the watchlist"""
        print(f"[{datetime.now()}] Refreshing watchlist... Rows: {len(self.rows)}")
        
        if not self.rows:
            print("No rows to refresh")
            return  # No rows to update
        
        for row_key in list(self.rows.keys()):
            try:
                row_data = self.get_row(row_key)
                ticker = row_data[0]
                
                print(f"Refreshing {ticker}...")
                
                stock = yf.Ticker(ticker)
                info = stock.info
                current_price = info.get('currentPrice', 0)
                prev_close = info.get('previousClose', 0)
                
                if current_price and prev_close:
                    change = current_price - prev_close
                    change_pct = (change / prev_close) * 100
                    
                    # Determine color based on price movement
                    old_price = self.price_history.get(ticker, current_price)
                    
                    print(f"{ticker}: ${current_price:.2f} (was ${old_price:.2f})")
                    
                    # Update cells
                    self.update_cell(row_key, "Price", f"${current_price:.2f}", update_width=False)
                    self.update_cell(row_key, "Change", f"{change:+.2f}", update_width=False)
                    self.update_cell(row_key, "% Change", f"{change_pct:+.2f}%", update_width=False)
                    
                    # Update price history
                    self.price_history[ticker] = current_price
                    
            except Exception as e:
                # If there's an error, skip this ticker
                print(f"Error refreshing {ticker}: {e}")
                continue
        
        print(f"[{datetime.now()}] Refresh complete")