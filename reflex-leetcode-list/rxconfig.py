import reflex as rx

class ReflexleetcodelistConfig(rx.Config):
    pass

config = ReflexleetcodelistConfig(
    app_name="reflex_leetcode_list",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)