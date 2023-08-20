import reflex as rx



class State(rx.State):
    hero:int = int(0)
    monster:int = int(20)
    health :int = int(10)

    def go (self):
        self.hero += 1
        self.monster -= 1
        if  State.monster ==0:
            health -= 1
            State.monster+=20
        #if State.health ==0:
            #return rx.text("about Page")    
    def back (self):
        self.hero -=1
        self.monster += 1
    #def health_up (self):
        #self.health +=10
        #return rx.text("index Page")
    




def index ():
    return rx.vstack(
        rx.button(
            "前進",
            color_scheme ="blue",
			border_radius="1em",
            style={"weight":"150","hight":"150"},
            on_click=State.go,
        ),
        rx.button(
            "後退",
            color_scheme ="red",
			border_radius="1em",
            style={"weight":"150","hight":"150"},
            on_click=State.back,
        ),
        rx.heading("勇者走了",State.hero,"步"),
        rx.heading("勇者離怪獸",State.monster,"步"),
        rx.heading("勇者剩下的血量",State.health),
        rx.link(
            rx.button("動漫妹子福利"),
                href="https://youtu.be/dQw4w9WgXcQ",
                button=True,
            
        ),

    )
#def about():

    #return rx.hstack(
        #rx.heading("遊戲結束"),
        #rx.button(
            #"返回遊戲",
            #on_click =State.health_up  ,
        #)
    #)


app = rx.App()
app.add_page(index)
#app.add_page(about)
app.compile()