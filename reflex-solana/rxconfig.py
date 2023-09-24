import reflex as rx

class ReflexsolanaConfig(rx.Config):
    pass

config = ReflexsolanaConfig(
    app_name="reflex_solana",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)