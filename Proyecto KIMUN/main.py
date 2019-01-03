# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 14:00:36 2018

@author: Marcela Catrian
"""

import numpy as np
import cv2
from time import time
from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty  
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from kivy.config import Config
Config.set('graphics','width',500)
Config.set('graphics','hight',500)

class ShowcaseScreen(Screen):
    fullscreen = BooleanProperty(False)
      
    

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(ShowcaseScreen,self).add_widget(*args)

        
    


class ShowcaseApp(App):
    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(1),BooleanProperty
    show_sourcecode = BooleanProperty(False)
    sourcecode = StringProperty() 
    screen_names = ListProperty([])
    hierarchy = ListProperty([]) 
    
    
    
    


    def build(self):
        self.title = 'Kimun'
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        self.screens = {}
        self.available_screens = sorted([
            'Login', 'Pantalla Principal','Camera','Pictures'
            
            ])
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'data', 'screens',
            '{}.kv'.format(fn).lower()) for fn in self.available_screens]
        self.go_next_screen()
        
       
    def img(self, pictures):
    
        original = cv2.imread("sillas.jpg")
        cv2.imshow("original", original)
 
# Convertimos a escala de grises
        gris = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
 
# Aplicar suavizado Gaussiano
        gauss = cv2.GaussianBlur(gris, (5,5), 0)
 
# Detectamos los bordes con Canny
        canny = cv2.Canny(gauss, 50, 150)
 
# Buscamos los contornos
        (contornos,_) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
# Mostramos el número de monedas por consola
        print("He encontrado {} objetos".format(len(contornos)))
 
        cv2.drawContours(original,contornos,-1,(0,0,255), 2)
        
        
        
        

    def on_pause(self):
        return True

    def on_resume(self):
        pass
    
    def on_current_title(self, instance, value):
        self.root.ids.spnr.text = value

    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_screen(self, idx):
        self.index = idx
        self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')
        self.update_sourcecode()

    def go_hierarchy_previous(self):
        ahr = self.hierarchy
        if len(ahr) == 1:
            return
        if ahr:
            ahr.pop()
        if ahr:
            idx = ahr.pop()
            self.go_screen(idx)

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index])
        self.screens[index] = screen
        return screen
    
    def read_sourcecode(self):
        fn = self.available_screens[self.index]
        with open(fn) as fd:
            return fd.read()

    def toggle_source_code(self):
        self.show_sourcecode = not self.show_sourcecode
        if self.show_sourcecode:
            height = self.root.height * .3
        else:
            height = 0

        Animation(height=height, d=.3, t='out_quart').start(
                self.root.ids.sv)

        self.update_sourcecode()

    def update_sourcecode(self):
        if not self.show_sourcecode:
            self.root.ids.sourcecode.focus = False
            return
        self.root.ids.sourcecode.text = self.read_sourcecode()
        self.root.ids.sv.scroll_y = 1

    

    def showcase_anchorlayout(self, layout):

        def change_anchor(self, *l):
            if not layout.get_parent_window():
                return
            anchor_x = ('left', 'center', 'right')
            anchor_y = ('top', 'center', 'bottom')
            if layout.anchor_x == 'left':
                layout.anchor_y = anchor_y[anchor_y.index(layout.anchor_y) - 1]
            layout.anchor_x = anchor_x[anchor_x.index(layout.anchor_x) - 1]

            Clock.schedule_once(change_anchor, 1)
        Clock.schedule_once(change_anchor, 1)

    def _update_clock(self, dt):
        self.time = time()


if __name__ == '__main__':
    ShowcaseApp().run()
    

