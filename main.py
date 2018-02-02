from kivy.app import App
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

class Screen1(Screen):
    pass

class Screen2(Screen):
    pass

class Screen3(Screen):
    pass

class Screen4(Screen):
    pass

class Screen5(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("screens.kv")

class main(App):
    def build(self):
        return presentation

main().run()