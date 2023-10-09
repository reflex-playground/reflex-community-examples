"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config
import reflex as rx

class User(rx.Model, table=True):
    user_name: str
    user_email: str

def user_row(user:User):
    return rx.tr(
        rx.td(str(user.id)),
        rx.td(user.user_name),
        rx.td(user.user_email),
    )
    
class State(rx.State):
    """The app state."""
    users:list[User] = []
    user_name:str=""
    user_email:str=""
    def getUsers(self):
        self.db_getUsers()
        print("click to call getUsers")
        try:
            for user in self.users:
                print(user)
        except:
            print("Exception")
      
    def db_getUsers(self) -> list[User]:
        with rx.session() as sess:
            self.users = (
                sess.query(User)
                .all()
            )
            return
  
    def db_addUser(self):
        with rx.session() as sess:
            sess.expire_on_commit = False
            strnum:str = str(len(self.users))
            user_name:str= f"my_{strnum}_UserName"
            user_email:str = f"my_{strnum}_UserEmail"

            sess.add(
                User(user_name=user_name, user_email=user_email)
            )
            sess.commit()
            return self.db_getUsers()
    pass


def index() -> rx.Component:
    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float="right"),
        rx.vstack(
            rx.heading("Hello Database CRUD of the Reflex!", font_size="2em"),
            rx.button("Add User", on_click=State.db_addUser),
            rx.button("Get User", on_click=State.getUsers),
            rx.table_container(
                rx.table(
                    rx.thead(
                        rx.tr(
                            rx.th("ID"),
                            rx.th("Name"),
                            rx.th("Email"),
                        )
                    ),
                    rx.tbody(
                        rx.foreach(State.users, user_row)
                    ),
                    variant="striped",
                ),
                margin_top="1rem",
            ),
        ),
        spacing="1.5em",
        font_size="2em",
        padding_top="10%",
    )


# Add state and page to the app.
app = rx.App(state=State)
app.add_page(index)
app.compile()
