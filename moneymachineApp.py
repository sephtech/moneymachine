import matplotlib.pyplot as plt
import numpy as np
import kivy
from kivy.app import App

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window

import system_interaction.database_interaction as dbi
import mathematics.calculations as calculations




Window.minimum_width = 960
Window.minimum_height = 540
# conf = ['', 'btc', 'eth', 'ltc', 'bat', 'link', 'xlm', 'bch', 'dash']
#        [Blau,       Grün       Rot]
colors = ['#1C86EE', '#00CD00', '#CD2626']
color =  ['1C86EE', '00CD00', 'CD2626']


class mainFrame(FloatLayout):

    def __init__ (self, **kwargs):

        super(mainFrame, self).__init__(**kwargs)
        
        self.coin1_read = False
        self.coin2_read = False
        self.coin3_read = False

        self.closePopup(1)
        # self.closePopup(2)
        self.closePopup(3)
        
        # self.openPopup(1)
        # self.openPopup(2)
        self.openPopup(3)
        self.updateGraph()
        self.ti_blocker = True
        db = dbi.DatabaseInteraction()
        self.conf = db.getSavedCoins()
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
            self.pred_coin1_day = calc.predictValue(self.ids.coin1.text, 60, 72)
            self.pred_coin1_week = calc.predictValue(self.ids.coin1.text, 60, 288)
            # self.pred_coin1_day = 10000
            # self.pred_coin1_week = 20000
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
            self.pred_coin2_day = calc.predictValue(self.ids.coin2.text, 60, 72)
            self.pred_coin2_week = calc.predictValue(self.ids.coin2.text, 60, 288)
            # self.pred_coin2_day = 10000
            # self.pred_coin2_week = 20000
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
            self.pred_coin3_day = calc.predictValue(self.ids.coin3.text, 60, 72)
            self.pred_coin3_week = calc.predictValue(self.ids.coin3.text, 60, 288)
            # self.pred_coin3_day = 10000
            # self.pred_coin3_week = 20000
            self.coin3_read = True
            self.counter_coins += 1
        else:
            self.coin3_read = False

    def updateGraph(self):
        graphGrid = self.ids.graphGrid
        coinValues = [0,0,0]
        coinRels = [0,0,0]
        coinMins = [0,0,0]
        coinMaxs = [0,0,0]
        predValues = [0,0,0]
        timeframe =''
        time_graph = []
        if(self.ids.toggle_time_tag.state == 'down'):
            timeframe = 'Tag'
            data_graph = []
            if self.coin1_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin1_day)
                else: data_graph.append(self.data_coin1_day)
                time_graph.append(self.time_coin1_day)
                coinValues[0] = self.data_coin1_day[-1]
                coinRels[0] = self.rel_coin1_day[-1]
                coinMins[0] = min(self.data_coin1_day)
                coinMaxs[0] = max(self.data_coin1_day)
                predValues[0] = self.pred_coin1_day
            if self.coin2_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin2_day)
                else: data_graph.append(self.data_coin2_day)
                time_graph.append(self.time_coin2_day)
                coinValues[1] = self.data_coin2_day[-1]
                coinRels[1] = self.rel_coin2_day[-1]
                coinMins[1] = min(self.data_coin2_day)
                coinMaxs[1] = max(self.data_coin2_day)
                predValues[1] = self.pred_coin2_day
            if self.coin3_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin3_day)
                else: data_graph.append(self.data_coin3_day)
                time_graph.append(self.time_coin3_day)
                coinValues[2] = self.data_coin3_day[-1]
                coinRels[2] = self.rel_coin3_day[-1]
                coinMins[2] = min(self.data_coin3_day)
                coinMaxs[2] = max(self.data_coin3_day)
                predValues[2] = self.pred_coin3_day
        elif(self.ids.toggle_time_woche.state == 'down'):
            timeframe = 'Woche'
            data_graph = []
            if self.coin1_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin1_week)
                else: data_graph.append(self.data_coin1_week)
                time_graph.append(self.time_coin1_week)
                coinValues[0] = self.data_coin1_day[-1]
                coinRels[0] = self.rel_coin1_day[-1]
                coinMins[0] = min(self.data_coin1_day)
                coinMaxs[0] = max(self.data_coin1_day)
                predValues[0] = self.pred_coin1_week
            if self.coin2_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin2_week)
                else: data_graph.append(self.data_coin2_week)
                time_graph.append(self.time_coin2_week)
                coinValues[1] = self.data_coin2_day[-1]
                coinRels[1] = self.rel_coin2_day[-1]
                coinMins[1] = min(self.data_coin2_day)
                coinMaxs[1] = max(self.data_coin2_day)
                predValues[1] = self.pred_coin2_week
            if self.coin3_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin3_week)
                else: data_graph.append(self.data_coin3_week)
                time_graph.append(self.time_coin3_week)
                coinValues[2] = self.data_coin3_day[-1]
                coinRels[2] = self.rel_coin3_day[-1]
                coinMins[2] = min(self.data_coin3_day)
                coinMaxs[2] = max(self.data_coin3_day)
                predValues[2] = self.pred_coin3_week
        elif(self.ids.toggle_time_monat.state == 'down'):
            timeframe = 'Monat'
            data_graph = []
            if self.coin1_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin1_month)
                else: data_graph.append(self.data_coin1_month)
                time_graph.append(self.time_coin1_month)
                coinValues[0] = self.data_coin1_day[-1]
                coinRels[0] = self.rel_coin1_day[-1]
                coinMins[0] = min(self.data_coin1_day)
                coinMaxs[0] = max(self.data_coin1_day)
                predValues[0] = self.pred_coin1_week
            if self.coin2_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin2_month)
                else: data_graph.append(self.data_coin2_month)
                time_graph.append(self.time_coin2_month)
                coinValues[1] = self.data_coin2_day[-1]
                coinRels[1] = self.rel_coin2_day[-1]
                coinMins[1] = min(self.data_coin2_day)
                coinMaxs[1] = max(self.data_coin2_day)
                predValues[1] = self.pred_coin2_week
            if self.coin3_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin3_month)
                else: data_graph.append(self.data_coin3_month)
                time_graph.append(self.time_coin3_month)
                coinValues[2] = self.data_coin3_day[-1]
                coinRels[2] = self.rel_coin3_day[-1]
                coinMins[2] = min(self.data_coin3_day)
                coinMaxs[2] = max(self.data_coin3_day)
                predValues[2] = self.pred_coin3_week
        elif(self.ids.toggle_time_jahr.state == 'down'):
            timeframe = 'Jahr'
            data_graph = []
            if self.coin1_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin1_year)
                else: data_graph.append(self.data_coin1_year)
                time_graph.append(self.time_coin1_year)
                coinValues[0] = self.data_coin1_day[-1]
                coinRels[0] = self.rel_coin1_day[-1]
                coinMins[0] = min(self.data_coin1_day)
                coinMaxs[0] = max(self.data_coin1_day)
                predValues[0] = self.pred_coin1_week
            if self.coin2_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin2_year)
                else: data_graph.append(self.data_coin2_year)
                time_graph.append(self.time_coin2_year)
                coinValues[1] = self.data_coin2_day[-1]
                coinRels[1] = self.rel_coin2_day[-1]
                coinMins[1] = min(self.data_coin2_day)
                coinMaxs[1] = max(self.data_coin2_day)
                predValues[1] = self.pred_coin2_week
            if self.coin3_read:
                if self.counter_coins > 1: data_graph.append(self.rel_coin3_year)
                else: data_graph.append(self.data_coin3_year)
                time_graph.append(self.time_coin3_year)
                coinValues[2] = self.data_coin3_day[-1]
                coinRels[2] = self.rel_coin3_day[-1]
                coinMins[2] = min(self.data_coin3_day)
                coinMaxs[2] = max(self.data_coin3_day)
                predValues[2] = self.pred_coin3_week
        else:
            self.ids.toggle_time_tag.state = 'down'
            return
        plt.clf()
        plt.plot()
        plt.grid()
        plt.figure().patch.set_facecolor('#F7F7F7')
        plt.axes().set_facecolor('#F7F7F7')
        runner = 0
        for c in range(0,3):
            # create data
            if (c == 0 and self.coin1_read) or (c == 1 and self.coin2_read) or (c == 2 and self.coin3_read):
                print("coin ", c)
                
                # use the plot function
                plt.plot(time_graph[c], data_graph[c], color=colors[c])
                ti1 = self.ids.coin1.text
                ti2 = self.ids.coin2.text
                ti3 = self.ids.coin3.text
                coinName = (ti1 if c == 0 else (ti2 if c == 1 else (ti3 if c == 2 else '')))
                coinValue = coinValues[c]
                coinRel = coinRels[c]
                coinMin = coinMins[c]
                coinMax = coinMaxs[c]
                predValue = predValues[c]
                predRel = (predValue - coinValue) / coinValue * 100
                preTime = '6h' if timeframe == 'Tag' else '1d'
                infobox = (self.ids.legendenBox1 if runner == 0 else (self.ids.legendenBox2 if runner == 1 else (self.ids.legendenBox3 if runner == 2 else None)))
                
                relsignData = ''
                relsignPred = ''

                if coinRel > 0: relsignData = '+'
                if predRel > 0: relsignPred = '+'
                
                s = '[b][size=18][color=%s]%s:\n[/color][/size][/b]'%(color[c],coinName.upper())
                s += '[b][color=000000]Value:[/b] %.2f$ %s%.2f%%\n'%(coinValue, relsignData, coinRel)
                s += '[b]Min:[/b] %.2f$\n'%(coinMin)
                s += '[b]Max:[/b] %.2f$\n'%(coinMax)
                s += '[b]Prediction for %s[/b]:\n%.2f$ %s%.2f%%[/color]'%(preTime, predValue, relsignPred, predRel)
                print(s)

                infobox.clear_widgets()
                infobox.add_widget(Label(text=(s),
                                         size_hint = (1, 1), markup=True))

                runner += 1
            


        graphGrid.clear_widgets()
        graphGrid.add_widget(FigureCanvasKivyAgg(plt.gcf()))


        print(timeframe)

        print('Finished')


    def closePopup(self, num):
        #print('close')
        if num == 1:
            p = self.ids.popup_one
        # if num == 2:
            # p = self.ids.popup_two
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
            self.closePopup(3)
        if num == 2:
            p = self.ids.popup_two
            self.closePopup(1)
            self.closePopup(3)
        if num == 3:
            p = self.ids.popup_three
            self.closePopup(1)
        
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
