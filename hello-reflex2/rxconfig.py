import reflex as rx

class HelloreflexConfig(rx.Config):
    pass

config = HelloreflexConfig(
    app_name="hello_reflex2",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)