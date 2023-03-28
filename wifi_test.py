from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

#import subprocess


class Read(Screen):
    def get_wifi(self):
        #connected_ssid = subprocess.check_output("powershell.exe (get-netconnectionProfile).Name", shell=True).strip()
        self.ids.wifi_text.text = "hello"

# Designate our .kv file
kv = Builder.load_file('wifi_test.kv')

class wifi_Test(App):
    def build(self):
        return Read()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    wifi_Test().run()
