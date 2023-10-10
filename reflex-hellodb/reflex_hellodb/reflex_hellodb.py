import reflex as rx
import asyncio
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
    is_run_tick: bool = False
    users:list[User] = []
    user_name:str=""
    user_email:str=""
    def getUsers(self):
        self.db_getUsers()
        #print("click to call getUsers")
        try:
            for user in self.users:
                #print(user)
                pass
        except:
            print("Exception")
      
    def db_getUsers(self) -> list[User]:
        with rx.session() as sess:
            self.users = (
                sess.query(User)
                .all()
            )
            return

    def db_updateUser(self):
        with rx.session() as sess:
            sess.expire_on_commit = False
            strnum:str = str(len(self.users))
            last_user:User = sess.query(User).order_by(User.id.desc()).first()
            if last_user:
                last_user.user_name = "EditedName"
                sess.commit()
                pass                
            return self.db_getUsers()

    def db_deleteUser(self):
        with rx.session() as sess:
            sess.expire_on_commit = False
            strnum:str = str(len(self.users))
            last_user:User = sess.query(User).order_by(User.id.desc()).first()
            if last_user:
                sess.delete(last_user)
                sess.commit()
                pass                

            return self.db_getUsers()


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
        
    async def tick(self):
        # run tick for update frontend ui for updating count
        self.getUsers()
        if self.is_run_tick:
            await asyncio.sleep(0.5)
            return self.tick
        
    async def onload(self):
        self.is_run_tick = True
        return self.tick
        
    pass


def index() -> rx.Component:
    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float="right"),
        rx.vstack(
            rx.heading("Hello Database CRUD of the Reflex!", font_size="2em"),
                        
            rx.button("Update Last User", on_click=State.db_updateUser),
            rx.button("Create User", on_click=State.db_addUser),
            rx.button("Read Users", on_click=State.getUsers),
            rx.button("Delete Last User", on_click=State.db_deleteUser),

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
app.add_page(
    index,
    title = "rx.CRUD",
    description = "learn databse from a simple CRUD example",
    on_load = State.onload
)
app.compile()
