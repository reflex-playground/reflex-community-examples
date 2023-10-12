import reflex as rx
import asyncio
class CommonState(rx.Model, table=True):
    sCounter:int
    sString:str
    def __init__(self,sCounter:int, sString:str):
        self.sCounter = sCounter
        self.sString = sString
    def __prep__(self):
        return f"[{self.sCounter} {self.sString}]"
def commonState_row(commonState:CommonState):
    return rx.tr(
        rx.td(commonState.id),
        rx.td(commonState.sCounter),
        rx.td(commonState.sString),
    )
class User(rx.Model, table=True):
    user_name: str
    user_email: str

def user_row(user:User):
    return rx.tr(
        rx.td(user.id),
        rx.td(user.user_name),
        rx.td(user.user_email),
    )
    
class State(rx.State):
    """The app state."""
    # member variable for implement a common state
    commonStates:list[CommonState] = [] # just support one row for the table
    defaultState:CommonState = CommonState(sCounter=0, sString="a")
    currentState:CommonState = CommonState(
        sCounter=defaultState.sCounter,
        sString=defaultState.sString
    )
    def getStates(self) -> list[CommonState]:
        with rx.session() as sess:
            self.commonStates = (
                sess.query(CommonState)
                .all()
            )
            if(len(self.commonStates)>0):
                self.currentState.sCounter = self.commonStates[0].sCounter
                self.currentState.sString = self.commonStates[0].sString
            else:
                self.currentState.sCounter = self.defaultState.sCounter
                self.currentState.sString = self.defaultState.sString
            return
    def setState(self, state:CommonState):
        if( len(self.commonStates) == 0):
            # Add to DB
            with rx.session() as sess:
                sess.expire_on_commit = False
                sess.add(
                    CommonState(
                        sCounter=state.sCounter,
                        sString=state.sString,
                    )
                )
                sess.commit()
                return self.getStates()
        else:
            # Update in DB
            with rx.session() as sess:
                sess.expire_on_commit = False
                last_state:CommonState = sess.query(CommonState).order_by(CommonState.id.desc()).first()
                if last_state:
                    last_state.sCounter = state.sCounter
                    last_state.sString = state.sString
                    sess.commit()
                    pass
                return self.getStates()
    def prepareCommonState(self) -> CommonState:
        return self.currentState
    def counterAdd(self):
        updatedState:CommonState = self.prepareCommonState()
        updatedState.sCounter = updatedState.sCounter + 1
        self.setState(updatedState)
        pass
    def counterSub(self):
        updatedState:CommonState = self.prepareCommonState()
        updatedState.sCounter = updatedState.sCounter - 1
        self.setState(updatedState)
        pass
    def stringAppend(self):
        updatedState:CommonState = self.prepareCommonState()
        updatedState.sString = updatedState.sString + "a"
        self.setState(updatedState)
        pass

    # member variable for normal database
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
        self.getStates()
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
            rx.button("Counter++", on_click=State.counterAdd),
            rx.button("Counter--", on_click=State.counterSub),
            rx.button("String+='a'", on_click=State.stringAppend),

            rx.table_container(
                rx.table(
                    rx.thead(
                        rx.tr(
                            rx.th("ID"),
                            rx.th("sCounter"),
                            rx.th("sString"),
                        )
                    ),
                    rx.tbody(
                        rx.foreach(State.commonStates, commonState_row)
                    ),
                    variant="striped",
                ),
                margin_top="1rem",
            ),

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
