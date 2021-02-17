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

import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import system_interaction.database_interaction as dbi
import mathematics.calculations as calculations

#set window size
Window.minimum_width = 960
Window.minimum_height = 540

#set colors for graphs
colors = ['#1C86EE', '#00CD00', '#CD2626']
color =  ['1C86EE', '00CD00', 'CD2626']

class mainFrame(FloatLayout):
    '''
    Initializes main Frame of the application
    '''

    def __init__ (self, **kwargs):
        '''
        Constructor of main Frame
        Opens the start popup window
        '''

        self.coin1_read = False
        self.coin2_read = False
        self.coin3_read = False

        super(mainFrame, self).__init__(**kwargs)

        #closes all popups
        self.closePopup(1)
        self.closePopup(2)
        
        #opens the popup and draws the empty graph
        self.openPopup(1)
        self.updateGraph()

        #gets all coines stored in the database
        db = dbi.DatabaseInteraction()
        self.conf = db.getSavedCoins()
        self.conf.insert(0, '')

    def autocomplete(self, num):
        '''
        Performs the autocompletion of the text inputs in the popup

        param num -> number of text input to perform autocomplete
        '''

        #checks which text input is used
        if num == 1:
            ti = self.ids.coin1
        elif num == 2:
            ti = self.ids.coin2
        elif num == 3:
            ti = self.ids.coin3
        
        #outputs the suggestion
        text = ti.text
        suggestion = next((s for s in self.conf if text in s), None)
        ti.suggestion_text = ""
        if suggestion != None and not suggestion==text:
            ti.suggestion_text = suggestion
        else:
            ti.suggestion_text = ""
        ti.text = text
        
    def tiFocusChange(self, num):
        '''
        Called if focus on given text input changes

        param num -> number of called text input
        '''

        #checks which text input is used
        if num == 1:
            ti = self.ids.coin1
        elif num == 2:
            ti = self.ids.coin2
        elif num == 3:
            ti = self.ids.coin3

        #sets text to suggestion if there is one and focus changes
        if ti.focus == False and ti.suggestion_text != '':
            text = ti.suggestion_text
            ti.suggestion_text = ''
            ti.text = ''
            ti.text = text

    def confirmPopup(self):
        '''
        If Popup is confirmed the method is called to gather data
        '''

        #gets data from database and closes popup
        self.getData()
        self.closePopup(2)

    def getData(self):
        '''
        Gets data from database and transforms it to the needed shapes
        '''
        self.counter_coins = 0
        calc = calculations.Calculations()

        #checks if coins are active
        self.coin1_read = self.ids.coin1.text in self.conf and self.ids.coin1.text != ''
        self.coin2_read = self.ids.coin1.text in self.conf and self.ids.coin2.text != ''
        self.coin3_read = self.ids.coin1.text in self.conf and self.ids.coin3.text != ''
        coin_read = (self.coin1_read, self.coin2_read, self.coin3_read)
        coin_text = (self.ids.coin1.text, self.ids.coin2.text, self.ids.coin3.text)

        #runs through every coin
        self.coinnum_coin_data = []
        for i in range(0, len(coin_read)):
            if coin_read[i]:

                data_coin = calc.getGraphAbsoluteData(coin_text[i])
                
                #creates empty arrays for different time intervals
                day_data = []
                week_data = []
                month_data = []
                year_data = []

                #appends teh data to the arrays
                day_data.append(data_coin[0])
                week_data.append(data_coin[2])
                month_data.append(data_coin[4])
                year_data.append(data_coin[6])
                day_data.append(data_coin[1])
                day_data.append(calc.calculateRelativeChanges(day_data[1]))
                week_data.append(data_coin[3])
                week_data.append(calc.calculateRelativeChanges(week_data[1]))
                month_data.append(data_coin[5])
                month_data.append(calc.calculateRelativeChanges(month_data[1]))
                year_data.append(data_coin[7])
                year_data.append(calc.calculateRelativeChanges(year_data[1]))
                day_data.append(calc.predictValue(coin_text[i], 60, 72))
                week_data.append(calc.predictValue(coin_text[i], 60, 288))
                month_data.append(week_data[3])
                year_data.append(week_data[3])
                timestamp_data = [day_data, week_data, month_data, year_data]
                self.coinnum_coin_data.append(timestamp_data)
                self.counter_coins += 1

    def updateGraph(self):
        '''
        Updates the graph on the main view
        '''
        graphGrid = self.ids.graphGrid
        coinValues = [0,0,0]
        coinRels = [0,0,0]
        coinMins = [0,0,0]
        coinMaxs = [0,0,0]
        predValues = [0,0,0]
        timeframe =''
        time_graph = []

        #checks which timeseries button is pressed
        toggle_states = [self.ids.toggle_time_day.state == 'down', self.ids.toggle_time_week.state == 'down', self.ids.toggle_time_month.state == 'down', self.ids.toggle_time_year.state == 'down']
        timeframes = ["day", "week", "month", "year"]
        
        #checks if nothing is pressed
        nothing_pressed = True
        for toggle_state in toggle_states:
            if toggle_state:
                nothing_pressed = False

        #select day if nothing is pressed
        if nothing_pressed:
            toggle_states[0] = True

        #walk through the different timeseries
        for j in range(0, len(toggle_states)):
            if toggle_states[j]:

                timeframe = timeframes[j]
                data_graph = []

                #walk through the different coins
                reads = (self.coin1_read, self.coin2_read, self.coin3_read)
                for i in range(0, len(reads)):
                    if reads[i]:

                        #sets the needed data
                        if self.counter_coins > 1: data_graph.append(self.coinnum_coin_data[i][j][2])
                        else: data_graph.append(self.coinnum_coin_data[i][j][1])
                        time_graph.append(self.coinnum_coin_data[i][j][0])
                        coinValues[i] = self.coinnum_coin_data[i][j][1][-1]
                        coinRels[i] = self.coinnum_coin_data[i][j][2][-1]
                        coinMins[i] = min(self.coinnum_coin_data[i][j][1])
                        coinMaxs[i] = max(self.coinnum_coin_data[i][j][1])
                        predValues[i] = self.coinnum_coin_data[i][j][3]

        #generates the plot
        plt.clf()
        plt.plot()
        plt.grid()
        plt.figure().patch.set_facecolor('#F7F7F7')
        plt.axes().set_facecolor('#F7F7F7')

        runner = 0
    
        #set axes and colors
        plt.tight_layout()
        fig, ax = plt.subplots()
        ax.set_facecolor('#F5F5F5')
        fig.patch.set_facecolor('#F5F5F5')
        for c in range(0,3):

            # create data
            if (c == 0 and self.coin1_read) or (c == 1 and self.coin2_read) or (c == 2 and self.coin3_read):
                
                #sets valaues on the x axis
                if timeframe == 'day':
                    formatstring = '%H:%M'
                    ax.xaxis.set_major_locator(ticker.MultipleLocator(25))
                    ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
                if timeframe == 'week':
                    formatstring = '%d.%m. %H:%M'
                    ax.xaxis.set_major_locator(ticker.MultipleLocator(60))
                    ax.xaxis.set_minor_locator(ticker.MultipleLocator(10))
                if timeframe == 'month':
                    formatstring = '%d.%m. %Hh'
                    ax.xaxis.set_major_locator(ticker.MultipleLocator(60))
                    ax.xaxis.set_minor_locator(ticker.MultipleLocator(10))
                if timeframe == 'year':
                    formatstring = '%d.%m.%Y'
                    ax.xaxis.set_major_locator(ticker.MultipleLocator(60))
                    ax.xaxis.set_minor_locator(ticker.MultipleLocator(25))

                #converts time from unix seconds  
                timeconvert = []
                for t in time_graph[c]:
                    timeconvert.append(datetime.datetime.fromtimestamp(t).strftime(formatstring))

                #adds the data to the plot
                ax.plot(timeconvert, data_graph[c], color=colors[c])
                if runner > 1: ax.set(xlabel='time', ylabel='price change [%]')
                else: ax.set(xlabel='time', ylabel='price [$]')
                ax.grid()

                #prepares content for the info box
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
                preTime = '6h' if timeframe == 'day' else '1d'
                infobox = (self.ids.legendenBox1 if runner == 0 else (self.ids.legendenBox2 if runner == 1 else (self.ids.legendenBox3 if runner == 2 else None)))
                
                relsignData = ''
                relsignPred = ''

                if coinRel > 0: relsignData = '+'
                if predRel > 0: relsignPred = '+'
                
                #formats the content for the infobox
                s = '[b][size=18][color=%s]%s:\n[/color][/size][/b]'%(color[c],coinName.upper())
                s += '[b][color=000000]Value:[/b] %.2f$ %s%.2f%%\n'%(coinValue, relsignData, coinRel)
                s += '[b]Min:[/b] %.2f$\n'%(coinMin)
                s += '[b]Max:[/b] %.2f$\n'%(coinMax)
                s += '[b]Prediction for %s[/b]:\n%.2f$ %s%.2f%%[/color]'%(preTime, predValue, relsignPred, predRel)

                #sets content for infobox
                infobox.clear_widgets()
                infobox.add_widget(Label(text=(s),
                                         size_hint = (1, 1), markup=True))

                runner += 1
            

        #puts the graph on the main frame
        graphGrid.clear_widgets()
        graphGrid.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def closePopup(self, num):
        '''
        Closes popup with the given number

        param num -> number of the popup to close
        '''

        if num == 1:
            p = self.ids.popup_one
        if num == 2:
            #if popup2 is closed update graph
            p = self.ids.popup_two
            self.updateGraph()

        #foldes popup so it is not clickable
        p.size_hint= (None, None)
        p.size = (0,0)
        for child in p.children:
            child.opacity = 0

    def openPopup(self, num):
        '''
        Opens popup with the given number

        param num -> number of the popup to close
        '''

        #closes other popups
        if num == 1:
            p = self.ids.popup_one
            self.closePopup(2)
        if num == 2:
            p = self.ids.popup_two
            self.closePopup(1)
        
        #brings popup to the front
        p.pos_hint= {'center_x':0.5,'center_y':0.5}
        p.size_hint= (None, 0.5)
        p.size= (self.height, self.height)
        for child in p.children:
            child.opacity = 1

    def updateButton(self):
        '''
        Action method for the update Buttons
        Performs database update and renews graph data
        '''

        db = dbi.DatabaseInteraction()
        if self.ids.coin1.text != '' and self.ids.coin1.text in self.conf: db.updateCoin(self.ids.coin1.text)
        if self.ids.coin2.text != '' and self.ids.coin2.text in self.conf: db.updateCoin(self.ids.coin2.text)
        if self.ids.coin3.text != '' and self.ids.coin3.text in self.conf: db.updateCoin(self.ids.coin3.text)
        self.getData()
        self.updateGraph()

    def updateAll(self):
        '''
        Action method for "update database" button
        Updates only the database
        '''
        db = dbi.DatabaseInteraction()
        db.updateAllCoins()

class mainApp(App):
    '''
    Starts the App
    '''

    def build(self):
        self.load_kv('moneymachine.kv')
        return mainFrame()

if __name__ == '__main__':
# def startApp():
    Window.minimum_width = 960
    Window.minimum_height = 540
    Window.size = (960, 540)
    mainApp().run()
