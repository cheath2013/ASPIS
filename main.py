from kivy.app import App
from kivy.lang import Builder 
from kivy.uix.screenmanager import ScreenManager, Screen 
# Create both screens. Please note the root.manager.current: this is how 
# you can control the ScreenManager from kv. Each screen has by default a 
# property manager that gives you the instance of the ScreenManager used. 
Builder.load_string(""" 
<MenuScreen>:
    AnchorLayout: 
        anchor_x: 'center' 
        anchor_y: 'center'
        Image: 
            size_hint: None, None 
            size: 400, 400
            source: 'aspis.png'
    AnchorLayout: 
        anchor_x: 'center' 
        anchor_y: 'top'   
        Label:  
            text_size: self.size
            text: 'ASPIS'
            color: (1, 0.5, 0.5, 1)
            font_size: 100
            halign: 'center'
            valign: 'top'
    AnchorLayout: 
        anchor_x: 'center' 
        anchor_y: 'bottom'
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .1
            Button:
                text: 'About'
            Button:
                text: 'New User'
                on_press: root.manager.current = 'reg'
            Button:
                name: 'exisBtn'
                text: 'Existing User'
                disabled: True


            

<SettingsScreen>: 
    GridLayout:  
        cols: 2 
        padding: 50 
        Label: 
            text: 'ASPIS'
            color: (1, 0.5, 0.5, 1)
            
        Label: 
            text: 'Registration'
            color: (1, 0.5, 0.5, 1)
            
        Label: 
            text: "First Name" 
        TextInput:
            id:'fName' 
            text: "Jermaine" 
        Label: 
            text: "Last Name" 
        TextInput:
            id:'lName' 
            text: "Cole" 
        Label: 
            text: "DOB (MM/DD/YY)" 
        TextInput:
            id:'dob' 
            text: "01/28/1985" 
        Label: 
            text: "Blood Type" 
        TextInput:
            id:'bType' 
            text: "A Negative" 
        Label: 
            text: "Insurance Company" 
        TextInput:
            id: 'iComp' 
            text: "Consolidated Health Plans" 
        Label:
            text:'Policy Number'
        TextInput:
            id:'pNumb'
            text: '#'

    AnchorLayout: 
        anchor_x: 'center' 
        anchor_y: 'bottom'
        padding: 30
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .1
            Button:
                text: 'Home'
                on_press: root.manager.current = 'menu'
            Button
                text: 'Submit'

    
""") 

# Declare both screens 
class MenuScreen(Screen): 
    pass 

class SettingsScreen(Screen): 
    pass 

# Create the screen manager 
sm = ScreenManager() 
sm.add_widget(MenuScreen(name='menu')) 
sm.add_widget(SettingsScreen(name='reg'))
 
class TestApp(App): 

    def build(self):
        return sm


if __name__ == '__main__':
    TestApp().run()




