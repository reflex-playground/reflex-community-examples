import reflex as rx

class TailwindConfig(rx.Config):
    pass

config = rx.Config(
    app_name="todo",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
    tailwind={},
)
