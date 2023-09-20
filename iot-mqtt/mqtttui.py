import npyscreen
import json
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

# MQTT broker 
BROKER_ADDRESS = "broker.emqx.io"
PORT = 1883  # MQTT broker default port
MYTOPIC = "MiloTopic"
COUNTERTOPIC = "MiloCounter"


# === Start of MQTT Subscribe process === 
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        #print("connect to MQTT broker done")
        client.subscribe(MYTOPIC)  # the topic your want to subscribe
        client.subscribe(COUNTERTOPIC)  # the topic your want to subscribe
        #print("subscribe the topic " + MYTOPIC)
        pass
    else:
        #print("connect MQTT broker failed")
        pass
def on_message(client, userdata, msg):
    global gForm
    text_message = msg.payload.decode('utf-8')
    if msg.topic == MYTOPIC:
        gForm.display_message(text_message, MYTOPIC)
        pass
    elif msg.topic == COUNTERTOPIC:
        gForm.display_message(text_message, COUNTERTOPIC)
        pass
    #print(f"Subscribed Topic '{msg.topic}' Message：{text_message}")
    pass
# === Finish of MQTT Subscribe process === 

# Publish the message on the topic
def mqtt_publish(message:str, topic:str=MYTOPIC):
    try:
        publish.single(topic, message, hostname=BROKER_ADDRESS, port=PORT)
        #print(f"Done to publish the message to the topic '{topic}': {message}")
        pass
    except Exception as e:
        #print(f"failed to publish: {e}")
        pass

def is_valid_json(s):
    try:
        json.loads(s)
        return True
    except json.JSONDecodeError:
        return False

class MyApp(npyscreen.NPSAppManaged):
    def onStart(self):
        global gForm
        npyscreen.setTheme(npyscreen.Themes.DefaultTheme)
        gForm = self.addForm('MAIN', MainMenuForm, name="Reflex IoT TUI Tool")
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(BROKER_ADDRESS, PORT, keepalive=60)
        # Start MQTT client
        client.loop_start()

class MainMenuForm(npyscreen.ActionFormMinimal):
    def mqtt_publish_txbuf(self):
        pass

    def display_message(self, msg:str, topic:str=MYTOPIC):
        if(False == is_valid_json(msg)):
            self.subcomp[topic].value = msg
            self.display()
            pass
        else:
            mydata = json.loads(msg)
            mypretty_json_str = json.dumps(mydata, indent=4) #Convert python dictionary into json string 
            self.subcomp[topic].value = mypretty_json_str
            self.display()
            pass
            
    def create(self):
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application
        self.add(npyscreen.ButtonPress, name="Exit", when_pressed_function=self.exit_application)
        self.add(npyscreen.TitleText, name="MQTT:", value= "command")
        self.add(npyscreen.ButtonPress, name="Count up one ", when_pressed_function=lambda: mqtt_publish("add", MYTOPIC))
        self.add(npyscreen.ButtonPress, name="Count down one", when_pressed_function=lambda: mqtt_publish("sub", MYTOPIC))
        self.add(npyscreen.ButtonPress, name="Send json of counter", when_pressed_function=lambda: mqtt_publish('{"count":33}',COUNTERTOPIC))
        
        self.add(npyscreen.TitleText, name="Operate Text :", value= "")
        self.subscribe_operation_text = self.add(npyscreen.MultiLineEdit, value="(null)", max_height=1)
        self.subscribe_operation_text.editable = False 
        
        self.add(npyscreen.TitleText, name="Counter JSON :", value= "")
        self.subscribe_counter_text = self.add(npyscreen.MultiLineEdit, value="(null)")
        self.subscribe_counter_text.editable = False 
        
        self.subcomp={MYTOPIC:self.subscribe_operation_text, COUNTERTOPIC:self.subscribe_counter_text}

    def on_ok(self):
        npyscreen.notify_confirm("You pressed OK.", "OK Pressed")

    def exit_application(self):
        self.parentApp.switchForm(None)

if __name__ == '__main__':
    app = MyApp()
    app.run()