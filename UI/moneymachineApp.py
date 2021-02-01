import matplotlib.pyplot as plt
import numpy as np
import kivy
from kivy.app import App

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window



Window.minimum_width = 960
Window.minimum_height = 540
conf = {'coins': ['', 'btc', 'eth', 'ltc', 'bat', 'link', 'xlm', 'bch', 'dash']}
colors = ['green', 'red', 'orange']

class mainFrame(FloatLayout):

    def __init__ (self, **kwargs):

        super(mainFrame, self).__init__(**kwargs)
        
        self.closePopup(1)
        self.closePopup(2)
        self.closePopup(3)
        
        # self.openPopup(1)
        # self.openPopup(2)
        self.openPopup(3)

        self.ti_blocker = True
        



    def autocomplete(self, num):
        print("Complete %d %s" % (num, self.ti_blocker))
        if self.ti_blocker:
            if num == 1:
                ti = self.ids.coin1
                text = ti.text
                suggestion = next((s for s in conf['coins'] if text in s), None)
                ti.suggestion_text = ""
                if suggestion != None:
                    ti.suggestion_text = suggestion
                else:
                    ti.suggestion_text = ""
                ti.text = text
            if num == 2:
                ti = self.ids.coin2
                text = ti.text
                suggestion = next((s for s in conf['coins'] if text in s), None)
                ti.suggestion_text = ""
                if suggestion != None:
                    ti.suggestion_text = suggestion
                else:
                    ti.suggestion_text = ""
                ti.text = text
            if num == 3:
                ti = self.ids.coin3
                text = ti.text
                suggestion = next((s for s in conf['coins'] if text in s), None)
                ti.suggestion_text = ""
                if suggestion != None:
                    ti.suggestion_text = suggestion
                else:
                    ti.suggestion_text = ""
                ti.text = text

    def coinConfirm(self, num):
        print("Confirm %d %s" % (num, self.ti_blocker))
        if num == 1:
            ti = self.ids.coin1
            if ti.focus == False:
                text = ti.suggestion_text
                ti.suggestion_text = ''
                if ti.suggestion_text != ti.text: self.ti_blocker = False
                ti.text = ''
                ti.text = text
                self.ti_blocker = True
            else:
                self.autocomplete(1)
        elif num == 2:
            ti = self.ids.coin2
            if ti.focus == False:
                text = ti.suggestion_text
                ti.suggestion_text = ''
                if ti.suggestion_text != ti.text: self.ti_blocker = False
                ti.text = ''
                ti.text = text
                self.ti_blocker = True
            else:
                self.autocomplete(2)
        elif num == 3:
            ti = self.ids.coin3
            if ti.focus == False:
                text = ti.suggestion_text
                ti.suggestion_text = ''
                if ti.suggestion_text != ti.text: self.ti_blocker = False
                ti.text = ''
                ti.text = text
                self.ti_blocker = True
            else:
                self.autocomplete(3)

    def updateGraph(self):
        graphGrid = self.ids.graphGrid
        timeframe =''
        if(self.ids.toggle_time_tag.state == 'down'):
            timeframe = 'Tag'
        elif(self.ids.toggle_time_woche.state == 'down'):
            timeframe = 'Woche'
        elif(self.ids.toggle_time_monat.state == 'down'):
            timeframe = 'Monat'
        elif(self.ids.toggle_time_jahr.state == 'down'):
            timeframe = 'Jahr'
        else:
            self.ids.toggle_time_tag.state = 'down'
            return
        plt.clf()
        plt.plot()    
        plt.figure().patch.set_facecolor('grey')
        plt.axes().set_facecolor('grey')
        coin1 = self.ids.coin1.text
        coin2 = self.ids.coin2.text
        coin3 = self.ids.coin3.text
        for c in range(0,2):
            # create data
            if (c == 1 and coin1 != '') or (c == 2 and coin2 != '') or (c == 3 and coin3 != ''):
                print("coin %d", c)
                values= 1
                        
                # use the plot function
                plt.plot(values, color=colors[c])


                graphGrid.clear_widgets()
                graphGrid.add_widget(FigureCanvasKivyAgg(plt.gcf()))


        print(timeframe)

        print('Finished')

    def closePopup(self, num):
        print('close')
        if num == 1:
            p = self.ids.popup_one
        if num == 2:
            p = self.ids.popup_two
        if num == 3:
            p = self.ids.popup_three
            self.updateGraph()

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
