import reflex as rx

class ReflexbinanceConfig(rx.Config):
    pass

config = ReflexbinanceConfig(
    app_name="reflex_binance",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)