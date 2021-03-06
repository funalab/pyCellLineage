"""
Author: Joel Nakatani
Overview:
GUI format for Analysis Selection
Creates GUI window

Parameters:
"""
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from functools import partial
from .modeIO import modeIO

class IndiCheckBox(CheckBox):
    modeTitle = list()
    root = object()
    Label = str()
    
    def __init__(self,modeTitle,Label,root,**kwargs):
        super(IndiCheckBox,self).__init__(**kwargs)
        self.modeTitle = modeTitle
        self.root = root
        self.Label = Label
        self.bind(active=partial(self.nested_set))

    def nested_set(self,instance, value):
        dic = self.root.getMode()
        keys = self.Label.split()
        keys.append(self.modeTitle)
        for key in keys[:-1]:
            dic = dic.setdefault(key, {})
            dic[keys[-1]] = value
        self.root.setMode(dic)
        

class makeButtons(GridLayout):
    mode = dict()
    modeNames = list()
    Labels = list()
    Label = str()
    sm = object()
    modeTitle = str()
    
    def __init__(self,mode,modeNames,Labels,Label,sm,**kwargs):
        super(makeButtons,self).__init__(**kwargs)
        self.mode = mode
        self.modeNames = modeNames
        self.cols = 3
        self.Labels = Labels
        self.Label = Label
        self.makeBtn(sm)
        

    def makeBtn(self,sm):
        for modeTitle in self.modeNames:
            if self.modeNames.index(modeTitle) == 0:
                textTitle = "Choose Modes for\n" + str(self.Label)
                #make label and button
                self.add_widget(Label(text=textTitle))
            else:
                self.add_widget(Label(text=""))

            self.add_widget(Label(text=modeTitle))
            instance = self
            cb = IndiCheckBox(modeTitle,self.Label,instance)
            self.add_widget(cb)
            cb = None

        backbtn = Button(text = 'back')
        backbtn.bind(on_press=partial(self.back,sm=sm))
        self.add_widget(backbtn)

        self.add_widget(Label(text=""))
        
        gobtn = Button(text = 'next')
        gobtn.bind(on_press=partial(self.go,sm=sm))
        self.add_widget(gobtn)
   
    def go(self,instance,sm):
        idx = self.Labels.index(self.Label)
        if idx < len(self.Labels)-1:
            sm.current = self.Labels[idx+1]
        else:
            sm.current = 'end_screen'

    def back(self,instance,sm):
        idx = self.Labels.index(self.Label)
        if idx - 1 >= 0:
            sm.current = self.Labels[idx-1]
        else:
            sm.current = 'Sample Choice'

    def getMode(self):
        return self.mode

    def setMode(self,mode):
        self.mode = mode

class AllButtons(Screen):
    Label = str()
    buttonNames = list()
    var = None
    mode = dict()
    modeNames = list()
    Labels = list()

    
    def __init__(self,mode,modeNames,Labels,sm,Label,**kwargs):
        super(AllButtons, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 50
        self.name = str(Label)
        
        self.mode = mode
        self.modeNames = modeNames
        self.Labels = Labels
        
        self.clear_widgets()
        allbtn = makeButtons(self.mode,self.modeNames,self.Labels,self.name,sm)
        self.add_widget(allbtn)
        self.mode = allbtn.getMode()
        return

    def getMode(self):
        return self.mode

class sampleCheckBox(CheckBox):
    cond = str()
    sample = str()
    root = object()
    
    def __init__(self,cond,sample,root,**kwargs):
        super(sampleCheckBox,self).__init__(**kwargs)
        self.cond = cond
        self.sample = sample
        self.root = root
        self.active = True
        self.bind(active=partial(self.setSamples))

    def setSamples(self,instance,value):
        dic = self.root.getSamples()
        dic[self.cond][self.sample] = value
        self.root.setSamples(dic)
        
class sampleButton(GridLayout):
    samples = dict()
    conditions = list()
    screenName = str()
    
    def __init__(self,samples,conditions,screenName,sm,**kwargs):
        super(sampleButton,self).__init__(**kwargs)
        self.cols = 3
        self.conditions = conditions
        self.samples = samples
        self.screenName = screenName

        self.makeBtn(sm)

    def makeBtn(self,sm):
        for cond in self.conditions:
            self.add_widget(Label(text=cond))
            counter = 0
            for sample in sorted(self.samples[cond]):
                if counter != 0:
                    self.add_widget(Label(text=""))
                self.add_widget(Label(text=sample))
                inst = self
                cb = sampleCheckBox(cond,sample,inst)
                self.add_widget(cb)
                cb = None
                counter += 1

        for i in range(2):
            self.add_widget(Label(text=""))
        btn = Button(text = 'Choose Analyses')
        btn.bind(on_press=partial(self.quit,sm=sm))
        self.add_widget(btn)
   
    def quit(self,instance,sm):
        sm.current = self.screenName


    def setSamples(self,samples):
        self.samples = samples

    def getSamples(self):
        return self.samples        
    
class sampleScreen(Screen):
    samples = dict()
    conditions = list()
    screenName = str()
    
    def __init__(self,samples,conditions,screenName,sm,**kwargs):
        self.name = "Sample Choice"
        super(sampleScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 50
        self.clear_widgets()
        self.samples = samples
        self.conditions = conditions
        self.screenName = screenName
        
        btn = sampleButton(self.samples,self.conditions,self.screenName,sm)
        self.add_widget(btn)
        self.samples = btn.getSamples()

    def getSamples(self):
        return self.samples

class endButton(GridLayout):
    screenName = str()
    root = object()
    
    def __init__(self,screenName,sm,root,**kwargs):
        super(endButton,self).__init__(**kwargs)
        self.cols = 3
        self.orientation = 'vertical'
        self.root = root

        self.screenName = screenName

        self.makeBtn(sm)

    def makeBtn(self,sm):
        lbl = Label(text="Done!\n X out of Window or press done")
        self.add_widget(lbl)
        for i in range(2):
            self.add_widget(Label(text=""))
        
        backbtn = Button(text = 'Redo?')
        backbtn.bind(on_press=partial(self.back,sm=sm))
        self.add_widget(backbtn)
        
        self.add_widget(Label(text=""))

        quitbtn = Button(text = 'Finished')
        quitbtn.bind(on_press=partial(self.quit,sm=sm))
        self.add_widget(quitbtn)

    def back(self,instance,sm):
        sm.current = 'Sample Choice'

    def quit(self,instance,sm):
        self.root.root_window.close()
    
class endScreen(Screen):
    screenName = str()
    
    def __init__(self,sm,root,**kwargs):
        self.name = 'end_screen'
        super(endScreen, self).__init__(**kwargs)
        self.screenName = 'end_screen'
        btn = endButton(self.screenName,sm,root)
        self.add_widget(btn)
    
    
class ModeScreens(App):
    title = "Choose Analysis mode"
    modeNames = list()
    modeNum = 0
    dictList = dict()
    mode = dict()
    
    conditions = list()
    samples = dict()

    
    #multiple screens (screen Lineage)
    def build(self):
        #initialize fields(mode)
        default = modeIO()
        self.mode = default.getMode()
        self.samples = default.getSamples()
        self.conditions = default.getConditions()
        modeLabels = default.splitModeNames()
        sm = ScreenManager(transition=NoTransition())
        Labels = list(modeLabels.keys())

        scrn = sampleScreen(self.samples,self.conditions,Labels[0],sm)
        sm.add_widget(scrn)

        for Label in Labels:            
            # make window
            allbtn = AllButtons(self.mode,modeLabels[Label],Labels,sm,Label)
            sm.add_widget(allbtn)
            self.mode = allbtn.getMode()
        endscrn = endScreen(sm,self)
        sm.add_widget(endscrn)

        sm.current = "Sample Choice"
        return sm
    
    def getMode(self):
        return self.mode

    def getSamples(self):
        return self.samples
    
    def getConditions(self):
        return self.conditions
    

