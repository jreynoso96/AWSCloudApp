"""initialize kivy modules"""
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.clock import Clock

""" """
import time as t
import mysql.connector
import random

"""initialize AWS MQTT Connection"""
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient("app")

#myAWSIoTMQTTClient.configureEndpoint("a2rxwu8egpjp5e-ats.iot.us-west-2.amazonaws.com", 8883)   #This is Jon
#myAWSIoTMQTTClient.configureCredentials("certificates/AmazonRootCA1.pem", "certificates/Jon_Certs/a21741307c-private.pem.key", "certificates/Jon_Certs/a21741307c-certificate.pem.crt") #This is Jon

myAWSIoTMQTTClient.configureEndpoint("a1e1oqcxpjzbv6-ats.iot.us-east-1.amazonaws.com", 8883)   #This is Josh's *thing* endpoint on Josh's server
myAWSIoTMQTTClient.configureCredentials("certificates/AmazonRootCA1.pem", "certificates/c09e3c174c-private.pem.key", "certificates/c09e3c174c-certificate.pem.crt") #This is Josh's main certification on Josh's server
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.connect()

mydb = mysql.connector.connect(
        host="testapp.cvtkxvsishwj.us-east-1.rds.amazonaws.com",
        user="jreynoso",
        password="S*0pW!JR",
        database="appUser",
        autocommit=True
    )

#initialize global variables
#global g_user
#global g_id

# Set App Size
#Window.size = (275,500)

class StartScreen(Screen):

    def ext(self):
        myAWSIoTMQTTClient.disconnect()
        App.get_running_app().stop()

class Login(Screen):
    def login_btn(self):
        self.user = self.ids.username_login.text
        self.password = self.ids.password_login.text

        mycursor = mydb.cursor()
        mycursor.execute("SELECT password FROM accounts WHERE username = '" + str(self.user) + "'")
        myresult = mycursor.fetchall()

        if myresult != [] and self.password == myresult[0][0]:
            global g_user
            global g_id
            g_user = self.user

            mycursor.execute("SELECT id FROM accounts WHERE username = '" + str(self.user) + "'")
            myresult = mycursor.fetchall()
            g_id = myresult[0][0]
            print(g_user, g_id)
            self.ids.username_login.text = ""
            self.ids.password_login.text = ""
            return True
        else:
            self.ids.password_login.text = ""
            self.ids.wrong_pass_text.opacity = 1
            Clock.schedule_once(self.hider, 1.5)
            return False

    def hider(self, timer):
        self.anim = Animation(opacity = 0, duration=2)
        self.anim.start(self.ids.wrong_pass_text)

class Register(Screen):

    def reg_btn(self):
        self.mycursor = mydb.cursor()
        self.mycursor.execute("SELECT username FROM accounts")
        self.myresult = self.mycursor.fetchall()

        self.new_user = self.ids.username_register.text
        if self.ids.username_register.text == "":
            self.new_user = " "

        self.new_password = self.ids.password_register.text
        if self.ids.password_register.text == "":
            self.password_register= " "

        self.new_id = random.randint(100000000, 1000000000)

        for existing_username in self.myresult[:]:
            if self.new_user == existing_username[0]:
                self.ids.password_register.text = ""
                self.ids.username_taken.opacity = 1
                Clock.schedule_once(self.hider, 1.5)
                return False
        self.register_account(self.new_id, self.new_user, self.new_password)
        return True

    def register_account(self, id, user, password):
        print("register step")
        self.ids.username_register.text = ""
        self.ids.password_register.text = ""
        self.mycursor = mydb.cursor()
        for existing_id in self.myresult[:]:
            if self.new_id == existing_id[0]:
                self.new_id = random.randint(10000000, 100000000)
                break
        self.new_id, self.new_user, self.new_pass = id, user, password
        self.sql = "INSERT INTO accounts (id,username,password) VALUES (%s, %s, %s)"
        self.val = (self.new_id, self.new_user, self.new_pass)

        self.mycursor.execute(self.sql, self.val)
        mydb.commit()

        self.mycursor.close()

    def hider(self, timer):
        self.anim = Animation(opacity = 0, duration=2)
        self.anim.start(self.ids.username_taken)

class Register_Confirmed(Screen):
    pass

class Devices(Screen):
    #def subscribe(params, args, packet):
    #    #self.ids.receive_mqtt_message.text = str(packet.payload)[2:-1]
    #    print(str(packet.payload))

    #myAWSIoTMQTTClient.subscribe("513654156/thing/tester", 1, subscribe)

    def ext(self):
        myAWSIoTMQTTClient.disconnect()
        App.get_running_app().stop()

class Publish(Screen):
    def message_create(self, message):
        self.msg = message
        return('{\n"message": "' + self.msg + '"\n}')

    def on_press_publish(self):
        print(g_user, g_id)
        #myAWSIoTMQTTClient.publish("test/testing", str(self.ids.send_mqtt_message.text), 1)
        myAWSIoTMQTTClient.publish(str(g_id)+"/"+str(g_user)+"/test", str(self.message_create(self.ids.send_mqtt_message.text)), 1)

        print("Published: '" + str(self.ids.send_mqtt_message.text) + " 'to the topic: " + "/"+str(g_id)+"/"+str(g_user)+"/test")
        self.ids.send_mqtt_message.text = ""
        t.sleep(0.1)

class Colors(Screen):
    pass
"""
class Subscribe(Screen):

    def subscribe(self, params, args, packet):
        self.ids.receive_mqtt_message.text = str(packet.payload)[2:-1]

    def on_press_subscribe(self):

        myAWSIoTMQTTClient.subscribe(str(g_id)+"/"+str(g_user)+"/test", 1, self.subscribe)
        #while True:
        #    t.sleep(5)

    def clear_message(self):
        self.ids.receive_mqtt_message.text = ""
"""
class WindowManager(ScreenManager):
    pass

# Designate our .kv file
kv = Builder.load_file('aws_tester.kv')

class AWS_Test(App):
    def build(self):
        return kv

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    AWS_Test().run()