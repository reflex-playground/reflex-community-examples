import reflex as rx
import asyncio
from .styles import base_style


async def set_state_count(count_val:int):
    keys = list(app.state_manager.states) #convert the keys of dict into the list
    ret_count_val: int = count_val
    for token in keys: # change state.count for all current running frontend
        state = app.state_manager.get_state(token)
        state.count = count_val
        app.state_manager.set_state(token, state)
    return {"state_count":ret_count_val}
async def add_state_count():
    keys = list(app.state_manager.states) #convert the keys of dict into the list
    ret_count_val: int = 0
    for token in keys: # change state.count for all current running frontend
        state = app.state_manager.get_state(token)
        state.count = state.count + 1
        ret_count_val = state.count
        app.state_manager.set_state(token, state)
    return {"state_count":ret_count_val}
async def sub_state_count():
    keys = list(app.state_manager.states) #convert the keys of dict into the list
    ret_count_val: int = 0
    for token in keys: # change state.count for all current running frontend
        state = app.state_manager.get_state(token)
        state.count = state.count - 1
        ret_count_val = state.count
        app.state_manager.set_state(token, state)
    return {"state_count":ret_count_val}



class CommonState(rx.Model, table=True):
    sCounter:int
    sString:str
    sJsonStr:str
    def __init__(self,sCounter:int, sString:str, sJsonStr:str):
        self.sCounter = sCounter
        self.sString = sString
        self.sJsonStr = sJsonStr
    def __prep__(self):
        return f"[{self.sCounter} {self.sString} {self.sJsonStr}]"
def commonState_row(commonState:CommonState):
    return rx.tr(
        rx.td(commonState.id),
        rx.td(commonState.sCounter),
        rx.td(commonState.sString),
        rx.td(commonState.sJsonStr),
    )

class State(rx.State):
    count: int = 0
    is_run_tick: bool = False

    # member variable for implement a common state
    commonStates:list[CommonState] = [] # just support one row for the table
    defaultState:CommonState = CommonState(sCounter=0, sString="a", sJsonStr='{"name":"Milo","age":18}')
    currentState:CommonState = CommonState(
        sCounter=defaultState.sCounter,
        sString=defaultState.sString,
        sJsonStr=defaultState.sJsonStr,
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
                self.currentState.sJsonStr = self.commonStates[0].sJsonStr
            else:
                self.currentState.sCounter = self.defaultState.sCounter
                self.currentState.sString = self.defaultState.sString
                self.currentState.sJsonStr = self.defaultState.sJsonStr
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
                        sJsonStr=state.sJsonStr,
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
                    last_state.sJsonStr = state.sJsonStr
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
    def jsonStrUpdate(self):
        updatedState:CommonState = self.prepareCommonState()
        data = json.loads(updatedState.sJsonStr)
        data['name'] = data['name'] + 'o'
        data['age'] = data['age'] + 1
        updatedState.sJsonStr = json.dumps(data)
        self.setState(updatedState)
        pass

    async def count_up(self):
        self.counterAdd()
        self.count = self.count + 1
        await set_state_count(self.count)

    async def count_down(self):
        self.counterSub()
        self.count = self.count - 1
        await set_state_count(self.count)
        
    async def tick(self):
        self.getStates()
        # run tick for update frontend ui for updating count
        if self.is_run_tick:
            await asyncio.sleep(0.5)
            return self.tick
        
    async def onload(self):
        self.is_run_tick = True
        return self.tick
    
        
def index():
    return rx.center(
        rx.vstack(
            rx.heading("Counter"),
            rx.text("Collaborative IoT Count"),
            rx.hstack(
                rx.button("+", on_click=State.count_up),
                rx.button("-", on_click=State.count_down),
            ),
            rx.link(State.count),

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


            spacing="0.5em",
            font_size="2em",
        ),
        padding_top="10%",
    )

print("Hint:You can open http://localhost:8000/state_count/33 to set count value as 33")
print("Hint:You can open http://localhost:8000/sub_state_count/ to substract one on the count value")
print("Hint:You can open http://localhost:8000/add_state_count/ to add one on the count value")
# Add state and page to the app.

app = rx.App(state=State, style=base_style)
app.api.add_api_route("/state_count/{count_val}", set_state_count)
app.api.add_api_route("/add_state_count/", add_state_count)
app.api.add_api_route("/sub_state_count/", sub_state_count)
app.add_page(
    index,
    title = "IoT MQTT Collaborative Counter App",
    description = "A IoT MQTT collaborative counter app",
    meta = [
        {"name": "theme_color", "content": "#FFFFFF"},
        {"char_set": "UTF-8"},
        {"property": "og:url", "content": "url"},
    ],
    on_load = State.onload,
)



app.compile()
