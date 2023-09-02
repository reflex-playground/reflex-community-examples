import reflex as rx

class IotmqttConfig(rx.Config):
    pass

config = IotmqttConfig(
    app_name="iot_mqtt",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)