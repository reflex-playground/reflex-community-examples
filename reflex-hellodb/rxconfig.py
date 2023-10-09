import reflex as rx

class ReflexhellodbConfig(rx.Config):
    pass

config = ReflexhellodbConfig(
    app_name="reflex_hellodb",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)