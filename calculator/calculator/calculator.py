import reflex as rx
import math

class State(rx.State):
    """The calculator state."""
    input = "" 
    result = ""
    error = "" 

    def append(self, char):
        """Append a character to the input."""
        self.input += char

    def backspace(self):
        """Delete the last character of the input."""
        if self.input:
            self.input = self.input[:-1]

    def clear(self):
        """Clear the input and the result."""
        self.input = ""
        self.result = ""
        self.error = ""

    def evaluate(self):
        """Evaluate the input and show the result."""
        try:
            self.result = str(eval(self.input))
            self.error = ""
        except Exception as e:
            self.result = ""
            self.error = str(e)

def index():
    return rx.center(
        rx.vstack(
            rx.heading("Calculator"),
            rx.text(State.error, color="red"),
            rx.text(State.result, font_size="2em"),
            rx.text(State.input, font_size="2em"),
            rx.hstack(
                rx.button("7", on_click=lambda: State.append("7")),
                rx.button("8", on_click=lambda: State.append("8")),
                rx.button("9", on_click=lambda: State.append("9")),
                rx.button("+", on_click=lambda: State.append("+")),
                spacing="0.5em"
            ),
            rx.hstack(
                rx.button("4", on_click=lambda: State.append("4")),
                rx.button("5", on_click=lambda: State.append("5")),
                rx.button("6", on_click=lambda: State.append("6")),
                rx.button("-", on_click=lambda: State.append("-")),
                spacing="0.5em"
            ),
            rx.hstack(
                rx.button("1", on_click=lambda: State.append("1")),
                rx.button("2", on_click=lambda: State.append("2")),
                rx.button("3", on_click=lambda: State.append("3")),
                rx.button("*", on_click=lambda: State.append("*")),
                spacing="0.5em"
            ),
            rx.hstack(
                rx.button(".", on_click=lambda: State.append(".")),
                rx.button("0", on_click=lambda: State.append("0")),
                rx.button("<-", on_click=State.backspace),
                rx.button("/", on_click=lambda: State.append("/")),
                spacing="0.5em"
            ),
            rx.hstack(
                rx.button("C", on_click=State.clear, color="red"),
                rx.button("=", on_click=State.evaluate, color="green"),
                spacing="0.5em"
            ),
            spacing="1em"
        ),
        width="100%",
        height="100vh"
    )

app = rx.App()
app.add_page(index)
app.compile()
