import reflex as rx

class HelloreflexshuminConfig(rx.Config):
    pass

config = HelloreflexshuminConfig(
    app_name="hello_reflex_shumin",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)