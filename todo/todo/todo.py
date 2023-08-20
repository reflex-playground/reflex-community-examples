import reflex as rx
from typing import List


class State(rx.State):
    """The app state."""

    # The current items in the todo list.
    # items: List[str] = [
    #     {
    #         "finished": "true",
    #         "content": "Write Code",
    #     },
    #     {
    #         "finished": "false",
    #         "content": "Sleep",
    #     },
    #     {
    #         "finished": "false",
    #         "content": "Have Fun",
    #     },
    # ]
    items: List[str] = ['Write Code', 'Sleep', 'Have fun']
    finished = [False, False, False]
    # The new item to add to the todo list.
    new_item: str

    def get_index(self, item: str):
        print(self.items.index(item))
        return self.items.index(item)

    def add_item(self, form_data: str):
        """Add a new item to the todo list.

        Args:
            form_data: The data from the form.
        """
        # Add the new item to the list.
        self.items.append(form_data["new_item"])
        self.finished.append(False)

        # Clear the value of the input.
        return rx.set_value("new_item", "")

    def remove_item(self, item: str):
        """Finish an item in the todo list.

        Args:
            item: The item to finish.
        """
        idx = self.items.index(item)
        self.items.pop(idx)
        self.finished.pop(idx)

    def toggle_item(self, item: str):
        """Finish an item in the todo list.

        Args:
            item: The item to finish.
        """
        idx = self.items.index(item)
        #self.items[self.items.index(item)]['finished'] = 'true'
        self.finished[idx] = not self.finished[idx]


def todo_item(item: rx.Var[str], idx: int) -> rx.Component:
    """Render an item in the todo list.

    NOTE: When using `rx.foreach`, the item will be a Var[str] rather than a str.

    Args:
        item: The todo list item.

    Returns:
        A single rendered todo list item.
    """
    return rx.list_item(
        rx.hstack(
            # A button to finish the item.
            # rx.checkbox(
            #     # on_click=lambda: State.toggle_item(item),
            #     height="1em",
            #     on_click=lambda: State.toggle_item(item),
            #     # on_chenged=lambda: State.toggle_item(item)
            # ),
            rx.button(
                rx.icon(tag="check"),
                on_click=lambda: State.toggle_item(item), 
            ),
            # The item text.
            rx.cond(
                State.finished[idx],
                rx.text(
                    item,
                    font_size="1.25em",
                    text_decoration = "line-through",
                    on_click=lambda: State.toggle_item(item),
                ),
                rx.text(
                    item,
                    font_size="1.25em",
                    on_click=lambda: State.toggle_item(item),
                )
            ),
            
            rx.button(
                rx.icon(tag="delete"),
                font_size="1em",
                color="white",
                on_click=lambda: State.remove_item(item),
                class_name="bg-red-400",
            ),
        )
    )


def todo_list() -> rx.Component:
    """Render the todo list.

    Returns:
        The rendered todo list.
    """
    return rx.ordered_list(
        # rx.foreach is necessary to iterate over state vars.
        # see: https://reflex.dev/docs/library/layout/foreach
        rx.foreach(State.items, lambda item, index: todo_item(item, index)),
    )


def new_item() -> rx.Component:
    """Render the new item form.

    See: https://reflex.dev/docs/library/forms/form

    Returns:
        A form to add a new item to the todo list.
    """
    return rx.form(
        # Pressing enter will submit the form.
        rx.input(
            id="new_item",
            placeholder="Add a todo...",
            bg="white",
        ),
        # Clicking the button will also submit the form.
        rx.center(
            rx.button("Add", type_="submit", bg="white"),
        ),
        on_submit=State.add_item,
    )


def index() -> rx.Component:
    """A view of the todo list.

    Returns:
        The index page of the todo app.
    """
    return rx.container(
        rx.vstack(
            rx.heading("Todos"),
            new_item(),
            rx.divider(),
            todo_list(),
            bg="#ededed",
            margin="5em",
            padding="1em",
            border_radius="0.5em",
            shadow="lg",
        )
    )


# Create the app and add the state.
app = rx.App(state=State)

# Add the index page and set the title.
app.add_page(index, title="Todo App")

# Compile the app.
app.compile()
