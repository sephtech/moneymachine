import matplotlib.pyplot as plt
import numpy as np
import kivy
from kivy.app import App

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window

from activate_coins import __getDefindedCoins__
import mathematics.calculations as calculations




Window.minimum_width = 960
Window.minimum_height = 540
# conf = ['', 'btc', 'eth', 'ltc', 'bat', 'link', 'xlm', 'bch', 'dash']
colors = ['green', 'red', 'orange']


class mainFrame(FloatLayout):

    def __init__ (self, **kwargs):

        super(mainFrame, self).__init__(**kwargs)
        
        self.coin1_read = False
        self.coin2_read = False
        self.coin3_read = False

        self.closePopup(1)
        self.closePopup(2)
        self.closePopup(3)
        
        # self.openPopup(1)
        # self.openPopup(2)
        self.openPopup(3)
        self.updateGraph()
        self.ti_blocker = True
        self.conf = __getDefindedCoins__()
        self.conf.insert(0, '')
        print(self.conf)
        



    def autocomplete(self, num):
        #print("Complete %d %s" % (num, self.ti_blocker))
        if self.ti_blocker:
            if num == 1:
                ti = self.ids.coin1
                text = ti.text
                suggestion = next((s for s in self.conf if text in s), None)
                ti.suggestion_text = ""
                if suggestion != None and not suggestion==text:
                    ti.suggestion_text = suggestion
                else:
                    ti.suggestion_text = ""
                ti.text = text
            if num == 2:
                ti = self.ids.coin2
                text = ti.text
                suggestion = next((s for s in self.conf if text in s), None)
                ti.suggestion_text = ""
                if suggestion != None and not suggestion==text:
                    ti.suggestion_text = suggestion
                else:
                    ti.suggestion_text = ""
                ti.text = text
            if num == 3:
                ti = self.ids.coin3
                text = ti.text
                suggestion = next((s for s in self.conf if text in s), None)
                ti.suggestion_text = ""
                if suggestion != None and not suggestion==text:
                    ti.suggestion_text = suggestion
                else:
                    ti.suggestion_text = ""
                ti.text = text

    def coinConfirm(self, num):
        #print("Confirm %d %s" % (num, self.ti_blocker))
        if num == 1:
            ti = self.ids.coin1
            if ti.focus == False and ti.suggestion_text != '':
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
            if ti.focus == False and ti.suggestion_text != '':
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
            if ti.focus == False and ti.suggestion_text != '':
                text = ti.suggestion_text
                ti.suggestion_text = ''
                if ti.suggestion_text != ti.text: self.ti_blocker = False
                ti.text = ''
                ti.text = text
                self.ti_blocker = True
            else:
                self.autocomplete(3)

    def confirmPopup(self):
        self.getData()
        self.closePopup(3)

    def getData(self):
        self.counter_coins = 0
        calc = calculations.Calculations()
        if self.ids.coin1.text in self.conf and self.ids.coin1.text != '':
            data_coin1 = calc.getGraphAbsoluteData(self.ids.coin1.text)
            self.time_coin1_day=data_coin1[0]
            self.time_coin1_week=data_coin1[2]
            self.time_coin1_month=data_coin1[4]
            self.time_coin1_year=data_coin1[6]
            self.data_coin1_day=data_coin1[1]
            self.rel_coin1_day = calc.calculateRelativeChanges(self.data_coin1_day)
            self.data_coin1_week=data_coin1[3]
            self.rel_coin1_week = calc.calculateRelativeChanges(self.data_coin1_week)
            self.data_coin1_month=data_coin1[5]
            self.rel_coin1_month = calc.calculateRelativeChanges(self.data_coin1_month)
            self.data_coin1_year=data_coin1[7]
            self.rel_coin1_year = calc.calculateRelativeChanges(self.data_coin1_year)
            self.coin1_read = True
            self.counter_coins += 1
        else:
            self.coin1_read = False

        if self.ids.coin2.text in self.conf and self.ids.coin2.text != '':
            data_coin2 = calc.getGraphAbsoluteData(self.ids.coin2.text)
            self.time_coin2_day=data_coin2[0]
            self.time_coin2_week=data_coin2[2]
            self.time_coin2_month=data_coin2[4]
            self.time_coin2_year=data_coin2[6]
            self.data_coin2_day=data_coin2[1]
            self.rel_coin2_day = calc.calculateRelativeChanges(self.data_coin2_day)
            self.data_coin2_week=data_coin2[3]
            self.rel_coin2_week = calc.calculateRelativeChanges(self.data_coin2_week)
            self.data_coin2_month=data_coin2[5]
            self.rel_coin2_month = calc.calculateRelativeChanges(self.data_coin2_month)
            self.data_coin2_year=data_coin2[7]
            self.rel_coin2_year = calc.calculateRelativeChanges(self.data_coin2_year)
            self.coin2_read = True
            self.counter_coins += 1
        else:
            self.coin2_read = False

        if self.ids.coin3.text in self.conf and self.ids.coin3.text != '':
            data_coin3 = calc.getGraphAbsoluteData(self.ids.coin3.text)
            self.time_coin3_day=data_coin3[0]
            self.time_coin3_week=data_coin3[2]
            self.time_coin3_month=data_coin3[4]
            self.time_coin3_year=data_coin3[6]
            self.data_coin3_day=data_coin3[1]
            self.rel_coin3_day = calc.calculateRelativeChanges(self.data_coin3_day)
            self.data_coin3_week=data_coin3[3]
            self.rel_coin3_week = calc.calculateRelativeChanges(self.data_coin3_week)
            self.data_coin3_month=data_coin3[5]
            self.rel_coin3_month = calc.calculateRelativeChanges(self.data_coin3_month)
            self.data_coin3_year=data_coin3[7]
            self.rel_coin3_year = calc.calculateRelativeChanges(self.data_coin3_year)
            self.coin3_read = True
            self.counter_coins += 1
        else:
            self.coin3_read = False

    def updateGraph(self):
        graphGrid = self.ids.graphGrid
        timeframe =''
        time_graph = []
        if(self.ids.toggle_time_tag.state == 'down'):
            timeframe = 'Tag'
            data_graph = []
            if self.coin1_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin1_day)
                else: data_graph.append(self.data_coin1_day)
                time_graph.append(self.time_coin1_day)
            if self.coin2_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin2_day)
                else: data_graph.append(self.data_coin2_day)
                time_graph.append(self.time_coin2_day)
            if self.coin3_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin3_day)
                else: data_graph.append(self.data_coin3_day)
                time_graph.append(self.time_coin3_day)
        elif(self.ids.toggle_time_woche.state == 'down'):
            timeframe = 'Woche'
            data_graph = []
            if self.coin1_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin1_week)
                else: data_graph.append(self.data_coin1_week)
                time_graph.append(self.time_coin1_week)
            if self.coin2_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin2_week)
                else: data_graph.append(self.data_coin2_week)
                time_graph.append(self.time_coin2_week)
            if self.coin3_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin3_week)
                else: data_graph.append(self.data_coin3_week)
                time_graph.append(self.time_coin3_week)
        elif(self.ids.toggle_time_monat.state == 'down'):
            timeframe = 'Monat'
            data_graph = []
            if self.coin1_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin1_month)
                else: data_graph.append(self.data_coin1_month)
                time_graph.append(self.time_coin1_month)
            if self.coin2_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin2_month)
                else: data_graph.append(self.data_coin2_month)
                time_graph.append(self.time_coin2_month)
            if self.coin3_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin3_month)
                else: data_graph.append(self.data_coin3_month)
                time_graph.append(self.time_coin3_month)
        elif(self.ids.toggle_time_jahr.state == 'down'):
            timeframe = 'Jahr'
            data_graph = []
            if self.coin1_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin1_year)
                else: data_graph.append(self.data_coin1_year)
                time_graph.append(self.time_coin1_year)
            if self.coin2_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin2_year)
                else: data_graph.append(self.data_coin2_year)
                time_graph.append(self.time_coin2_year)
            if self.coin3_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin3_year)
                else: data_graph.append(self.data_coin3_year)
                time_graph.append(self.time_coin3_year)
        else:
            self.ids.toggle_time_tag.state = 'down'
            return
        plt.clf()
        plt.plot()
        plt.grid()
        plt.figure().patch.set_facecolor('grey')
        plt.axes().set_facecolor('grey')
        for c in range(0,3):
            # create data
            if (c == 0 and self.coin1_read) or (c == 1 and self.coin2_read) or (c == 2 and self.coin3_read):
                print("coin ", c)
                
                # use the plot function
                plt.plot(time_graph[c], data_graph[c], color=colors[c])



        graphGrid.clear_widgets()
        graphGrid.add_widget(FigureCanvasKivyAgg(plt.gcf()))


        print(timeframe)

        print('Finished')

    def closePopup(self, num):
        #print('close')
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
        #print('open')
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
# def startApp():
    Window.minimum_width = 960
    Window.minimum_height = 540
    Window.size = (960, 540)
    mainApp().run()
