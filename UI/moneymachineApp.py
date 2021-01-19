from kivy.app import App

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window

Window.minimum_width = 960
Window.minimum_height = 540
class mainFrame(FloatLayout):
    def __init__ (self, **kwargs):

        super(mainFrame, self).__init__(**kwargs)
        
        self.closePopup(1)
        self.closePopup(2)
        self.closePopup(3)
        
        # self.openPopup(1)
        # self.openPopup(2)
        self.openPopup(3)

    def updateGraph(self):
        if(self.ids.toggle_time_tag.state == 'down'):
            print('Tag')
        elif(self.ids.toggle_time_woche.state == 'down'):
            print('Woche')
        elif(self.ids.toggle_time_monat.state == 'down'):
            print('Monat')
        elif(self.ids.toggle_time_jahr.state == 'down'):
            print('Jahr')
        else:
            self.ids.toggle_time_tag.state = 'down'
            self.updateGraph()
            return
        print('Finished')

    def closePopup(self, num):
        print('close')
        if num == 1:
            p = self.ids.popup_one
        if num == 2:
            p = self.ids.popup_two
        if num == 3:
            p = self.ids.popup_three

        p.size_hint= (None, None)
        p.size = (0,0)
        for child in p.children:
            child.opacity = 0



    def openPopup(self, num):
        print('open')
        if num == 1:
            p = self.ids.popup_one
            self.closePopup(2)
        if num == 2:
            p = self.ids.popup_two
            self.closePopup(1)
            self.closePopup(3)
        if num == 3:
            p = self.ids.popup_three
            self.closePopup(2)
        
        p.pos_hint= {'center_x':0.5,'center_y':0.5}
        p.size_hint= (None, 0.5)
        p.size= (self.height, self.height)
        for child in p.children:
            child.opacity = 1
        
            

        

class mainApp(App):
    def build(self):
        self.load_kv('moneymachine.kv')
        return mainFrame()


if __name__ == '__main__':
    Window.minimum_width = 960
    Window.minimum_height = 540
    Window.size = (960, 540)
    mainApp().run()
