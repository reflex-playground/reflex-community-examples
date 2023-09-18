"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config
import os
import reflex as rx
from dotenv import load_dotenv
from binance.client import Client
load_dotenv()  
API_KEY = os.environ.get('BINANCE_API_KEY')
API_SECRET = os.environ.get('BINANCE_API_SECRET')
if not API_KEY or not API_SECRET:
    raise ValueError("Please set the BINANCE_API_KEY and BINANCE_API_SECRET environment variables.")

# Demonstrate binance api work for get bitcoin trade here
print("API_KEY = " + API_KEY)
print("API_SECRET = " + API_SECRET)
try:
    client = Client(API_KEY, API_SECRET)
    recent_trades = client.get_recent_trades(symbol='BTCUSDT', limit=10)
    print("最近的 Bitcoin 交易:")
    for trade in recent_trades:
        print(f"交易ID: {trade['id']}, 價格: {trade['price']}, 數量: {trade['qty']}")
except:
    print("Exception")

# Start to do reflex web app for this api.
class Trade(rx.Model, table=True):
    """A table for trades in the database."""
    tradeId: str
    tradePrice: str
    tradeQty: str
    def __init__(self, id, price, qty):
        self.tradeId = id
        self.tradePrice = price
        self.tradeQty = qty
    def __repr__(self):
        return "("+self.tradeId+","+self.tradePrice+","+self.tradeQty+")"

class State(rx.State):
    """The app state."""
    trades:list[Trade] = []
    def getTrades(self):
        print("click to call getTrades")
        try:
            client = Client(API_KEY, API_SECRET)
            recent_trades = client.get_recent_trades(symbol='BTCUSDT', limit=10)
            self.trades = [ Trade(t['id'], t['price'], t['qty'])  for t in recent_trades]
        except:
            print("Exception")

def trade_row(trade:Trade):
    return rx.tr(
        rx.td(trade.tradeId),
        rx.td(trade.tradePrice),
        rx.td(trade.tradeQty),
    )

def index() -> rx.Component:
    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float="right"),
        rx.vstack(
            rx.heading("Welcome to Reflex Binance!", font_size="2em"),
            rx.button("Get BitCoin Trades", on_click=State.getTrades),
            rx.table_container(
                rx.table(
                    rx.thead(
                        rx.tr(
                            rx.th("ID"),
                            rx.th("Price"),
                            rx.th("QTY"),
                        )
                    ),
                    rx.tbody(
                        rx.foreach(State.trades, trade_row)
                    ),
                    variant="striped",
                ),
                margin_top="1rem",
            ),
        ),
        spacing="1.5em",
        font_size="2em",
        padding_top="10%",
    )

# Add state and page to the app.
app = rx.App(state=State)
app.add_page(index)
app.compile()
