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
try:
    client = Client(API_KEY, API_SECRET)
    recent_trades = client.get_recent_trades(symbol='BTCUSDT', limit=10)

    print("最近的 Bitcoin 交易:")
    for trade in recent_trades:
        print(f"交易ID: {trade['id']}, 價格: {trade['price']}, 數量: {trade['qty']}")
except:
    print("Exception")





class State(rx.State):
    """The app state."""
    pass


def index() -> rx.Component:
    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float="right"),
        rx.vstack(
            rx.heading("Welcome to Reflex Binance!", font_size="2em"),
            rx.text(API_KEY),
            rx.text(API_SECRET)
        ),
        spacing="1.5em",
        font_size="2em",
        padding_top="10%",

    )


# Add state and page to the app.
app = rx.App(state=State)
app.add_page(index)
app.compile()
