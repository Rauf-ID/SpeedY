# -*- coding: utf-8 -*-
#Rauf Agaguliyev and Vsevolod Batyrov present: SpeedY
#All rights reserved!

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooser
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.config import Config
from time import sleep
from threading import Thread
import pdfminer.high_level
import os
import sys
import pickle

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '600')

Builder.load_string("""
<Started>:
    BoxLayout:
        # padding: 100, 100, 100, 100
        Button:
            on_press:
                root.manager.transition.duration = 1.4
                root.manager.current = 'root'
            background_normal: '\Image\speedynormal.png'
            background_down: '\Image\speedydown.png'

# <MenuScreen>:
#     BoxLayout:
#         canvas.before:
#             Color:
#                 rgb: 0.94,0.94,0.94
#             Rectangle: 
#                 pos: self.pos 
#                 size: self.size 
#         orientation: 'vertical'
#         Button:
#             text: 'Go'
#             on_press:
#                 root.manager.transition.duration = .78
#                 root.manager.current = 'root'
#                 root.manager.transition.direction = 'left'
<Root>:
    FloatLayout:
        canvas.before:
            Color:
                rgb: 0.94,0.94,0.94
            Rectangle: 
                pos: self.pos 
                size: self.size 
        size: 900, 600
        orientation: 'vertical'
        # Button:
        #     # text: 'Back to menu'
        #     background_normal: 'arrow.png'
        #     background_down: 'arrow.png'
        #     size_hint: .13, .10
        #     pos: 35, 500
        #     on_press: 
        #         root.manager.current = 'menu'
        #         root.manager.transition.direction = 'right'
        Button:
            # color: 0,1,0,1
            # text: 'Play'
            background_normal: 'play1.png'
            background_down: 'play2.png'
            size_hint: .15, .066
            pos: 390, 107
            on_release: root.upd_ltxt()
        Image:
            source: 'line.png'
            pos: 35, 35
        Label:
            id: texts
            color: 0,0,0,1
            text: 'Loo[color=ff3333]k[/color] Here!'
            halign: 'center'
            markup: True
            font_size: 35
            pos: -36, 35
        Label:
            id: speed
            color: 0,0,0,1
            text: '120 wpm'
            halign: "center"
            font_size: 20
            pos: 240, -65
        Button:
            # text: '+'
            background_normal: 'plus.png'
            background_down: 'downplus.png'          
            size_hint: .105, .15
            pos: 720, 43
            on_release: root.upd_count_plus()
        Button:
            # text: '-'
            background_normal: 'minus.png'
            background_down: 'downminus.png'
            size_hint: .105, .15
            pos: 80, 43 
            on_release: root.upd_count_minus()
        Button:
            # text: 'Stop/Start'
            background_normal: 'stop1.png'
            background_down: 'stop2.png'
            size_hint: .22, .095
            pos: 358, 36
            on_press: root.stop()
        Button:
            text: 'Choose File'
            color: 0.94,0.94,0.94,1
            size_hint: .15, .08
            pos: 35, 530
            on_release: root.show_load()
        Button:
            text: 'Save File'
            color: 0.94,0.94,0.94,1
            size_hint: .15, .08
            pos: 730, 530
            on_release: root.save()

<LoadDialog>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: filechooser

        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                on_release: root.cancel()
            Button:
                text: "Load"
                on_release: root.load(filechooser.path, filechooser.selection)
""")

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Started(Screen):
	pass

class Root(Screen):

    def __init__(self,*args,**kwargs):
        super(Root,self).__init__(*args,**kwargs)
        
        self.gtre=0 
        self.jen=0 
        self.parts=[] 
        self.count=0.500 
        self.words=[]
        self.wordsss=[]
        self.fpath=''
        self.fname=''
        self.wpm=120

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        fill = filename[0]
        self.fpath=path     
        try:
            if 'pdf' in fill:  
                self.fname = fill.replace(self.fpath,'')
                self.fname = self.fname.replace('.pdf','') 
            if 'pickle' in fill:
                self.fname = fill.replace(self.fpath,'')
                self.fname = self.fname.replace('.pickle','')
            else:
                with open(fill, 'rb') as file:
                    if fill[-3::] == 'pdf': 
                        with open(self.fpath+self.fname+'_speedy'+'.txt','w') as ff:
                            pdfminer.high_level.extract_text_to_fp(file,ff)
                            
                    elif fill[-3::] == 'txt': 
                        with open(fill,'r') as file:
                            with open(self.fpath+self.fname+'_speedy'+'.txt','w') as ff:
                                for line in file:
                                    ff.write(line)        

                with open(self.fpath+self.fname+'_speedy'+'.txt','r') as file:
                    self.words=[]
                    word=''
                    for line in file:       
                        for i in line:           
                            if i == '.' or  i==' ' or i==',' or i =='?' or i=='!' or i=='-' or i=='_' or i=='—':
                                if word!='':
                                    self.words+=[word]
                                word=''
                            elif i.isupper():
                                self.words+=[word]
                                word=''
                                word+=i
                            else:
                                word+=i
                for i in self.words:
                    if i!='':
                        self.wordsss+=[i]
                with open(self.fpath+self.fname+'.pickle','wb') as file:
                    pickle.dump(self.wordsss,file)
                os.remove(self.fpath+self.fname+'_speedy'+'.txt')

        except UnicodeEncodeError: 
            pass

        self.dismiss_popup()

    def upd_ltxt(self):
        self.gtre=0
        self.jen=0
        self.parts=[]
        Thread(target=self.update_label).start()

    def stop(self):
        if self.gtre==0:
            self.gtre=1
        elif self.gtre==1:
            self.gtre=0
            Thread(target=self.update_label).start()

    def save(self):
        with open(self.fpath+self.fname+'.pickle','wb') as file:
            pickle.dump(self.parts,file)
        self.jen=0

    def upd_count_plus(self):
        if self.count-0.05555>0.05:
            self.count-=0.05
            self.wpm+=10
            self.ids.speed.text=str(self.wpm)+' wpm'

    def upd_count_minus(self):
        if self.count+0.05555<1.1:
            self.count+=0.05
            self.wpm-=10
            self.ids.speed.text=str(self.wpm)+' wpm'

    def update_label(self):
        with open(self.fpath+self.fname+'.pickle','rb') as myfile:
            self.parts = pickle.load(myfile)
        for i in range(self.jen):
            self.parts.pop(0)

        for i in self.parts:    
            color=i
            if len(color)==1 or len(color)==2:
                self.ids.texts.text='[color=FF0000]'+color[0:1]+'[/color]'+color[1:]
            elif len(color)==3 or len(color)==4:
                self.ids.texts.text=color[0:1]+'[color=FF0000]'+color[1:2]+'[/color]'+color[2:]
            elif len(color)==5 or len(color)==6:
                self.ids.texts.text=color[0:2]+'[color=FF0000]'+color[2:3]+'[/color]'+color[3:]
            elif len(color)==7 or len(color)==8:
                self.ids.texts.text=color[0:3]+'[color=FF0000]'+color[3:4]+'[/color]'+color[4:]
            elif len(color)==9 or len(color)==10:
                self.ids.texts.text=color[0:4]+'[color=FF0000]'+color[4:5]+'[/color]'+color[5:]
            elif len(color)==11 or len(color)==12:
                self.ids.texts.text=color[0:5]+'[color=FF0000]'+color[5:6]+'[/color]'+color[6:]
            elif len(color)==13 or len(color)==14:
                self.ids.texts.text=color[0:6]+'[color=FF0000]'+color[6:7]+'[/color]'+color[7:]
            elif len(color)==15 or len(color)==16:
                self.ids.texts.text=color[0:7]+'[color=FF0000]'+color[7:8]+'[/color]'+color[8:]
            elif len(color)==17 or len(color)==18:
                self.ids.texts.text=color[0:8]+'[color=FF0000]'+color[8:9]+'[/color]'+color[9:]
            self.jen+=1
            print(self.jen)                   
            sleep(self.count)
            if self.gtre==1:
                raise TypeError
            self.parts=self.parts[1:]

sm = ScreenManager()
sm.add_widget(Started(name='started'))
# sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(Root(name='root'))

class SpeedYApp(App):
    def build(self):
        return sm
if __name__ == '__main__':
    SpeedYApp().run()