"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config
import reflex as rx


class User(rx.Model, table=True):
    user_name: str
    user_email: str
    


def user_row(user:User):
    return rx.tr(
        rx.td(str(1)),
        rx.td(user.user_name),
        rx.td(user.user_email),
    )
    

class State(rx.State):
    """The app state."""
    users:list[User] = []
    user_name:str=""
    user_email:str=""
    def getUsers(self):        
        print("click to call getUsers")
        try:
            for user in self.users:
                print(user)
        except:
            print("Exception")
    def addUser(self):
        strnum:str = str(len(self.users))
        #self.commitUser(strnum, "Name"+strnum, f"my_{strnum}_email@mail.com")
        self.users.append( User(strnum, "Name"+strnum, f"my_{strnum}_email@mail.com"))
      
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
            self.user_name = "myUserName"
            self.user_email = "myUserEmail"
            sess.add(
                User(
                    #user_email=self.user.email, contact_name=self.name, email=self.email
                    
                    user_name=self.user_name, user_email=self.user_email
                )
            )
            sess.commit()
            return self.db_getUsers()
        
    def commitUser(self, userId:str, userName:str, userEmail:str):
        with rx.session() as session:
            session.add(
                User(
                    userId=int(userId),
                    userName=userName,
                    userEmail=userEmail
                )
            )
            session.commit()
        self.queryUser()
                
    def queryUser(self):
        with rx.session() as session:
            self.users = (
                session.query(User)
                .filter(User.username.contains(self.name))
                .all()
            )            
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
