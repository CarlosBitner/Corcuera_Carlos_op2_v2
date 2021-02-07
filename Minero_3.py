from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import ListProperty,NumericProperty,ObjectProperty,StringProperty,DictProperty
from kivy.uix.screenmanager import ScreenManager,FadeTransition,Screen
from kivy.core.window import Window
from kivy.clock import Clock
import random


class MineroWindow(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition=FadeTransition()
        Window.size=(800,800)

class Pantalla_de_inicio(Screen):
    pass

class Pantalla_de_usuario(Screen):
    pass

class Pantalla_de_dificultad(Screen):
    dificultad=StringProperty('f')
    pass

class Pantalla_de_juego(Screen):
    pass

class Leaderboard(Screen):
    pass

class Flotante_de_juego(FloatLayout):
    diccionario=DictProperty({'f':[10,10],'i':[15,20],'d':[15,30]})
    coordenada_pj=ListProperty([5,770])
    coor_diamantes=ListProperty([])
    coor_bombas=ListProperty([])
    num_diam=NumericProperty(0)
    num_bombas=NumericProperty(0)
    vidas=NumericProperty(5)
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)

    def Empezar_juego(self):
        global fuenteb
        self.coordenada_pj=[5,770]
        self.select_dificultad()
        self.generar_posiciones_diamantes()
        self.generar_posiciones_bombas()
        self.generar_diamantes()
        self.generar_bombas()
        self.evento=Clock.schedule_interval(self.verificar_num_diam,0.1)
        Clock.schedule_once(self.desaparecer_bombas,5)
        
    def reinicializar_valores(self):
        self.coordenada_pj=[5,770]
        self.coor_diamantes=[]
        self.coor_bombas=[]
        self.num_diam=0
        self.num_bombas=0
        self.vidas=5
        App.get_running_app().root.get_screen('sc_game').ids.float_juego.ids.layout_diamantes.clear_widgets()
        App.get_running_app().root.get_screen('sc_game').ids.float_juego.ids.layout_bombas.clear_widgets()

    def generar_posiciones_diamantes(self):
        i=0
        while i < self.num_diam:
            val_x=random.randint(0,19)
            val_y=random.randint(0,19)
            cor_x=40*val_x+5
            cor_y=200+30*val_y
            coordenada_diamante=(cor_x,cor_y)
            if coordenada_diamante not in self.coor_diamantes:
                self.coor_diamantes.append(coordenada_diamante)
                i+=1
        # print(self.coor_diamantes)
    
    def generar_posiciones_bombas(self):
        i=0
        while i < self.num_bombas:
            val_x=random.randint(0,19)
            val_y=random.randint(0,19)
            cor_x=40*val_x+5
            cor_y=200+30*val_y
            coordenada_bomba=(cor_x,cor_y)
            if coordenada_bomba not in self.coor_diamantes and coordenada_bomba not in self.coor_bombas:
                self.coor_bombas.append(coordenada_bomba)
                i+=1
        # print(self.coor_bombas)

    def select_dificultad(self):
        x=App.get_running_app().root.get_screen('sc_dif').dificultad
        # print(x)
        self.num_diam=self.diccionario[x][0]
        self.num_bombas=self.diccionario[x][1]

    def generar_diamantes(self):
        for i in range(self.num_diam):
            d=Diamante()
            d.pos=self.coor_diamantes[i]
            App.get_running_app().root.get_screen('sc_game').ids.float_juego.ids.layout_diamantes.add_widget(d)
            # print(d.pos)

    def generar_bombas(self):
        for i in range(self.num_bombas):
            f=Bomba()
            f.pos=self.coor_bombas[i]
            App.get_running_app().root.get_screen('sc_game').ids.float_juego.ids.layout_bombas.add_widget(f)
            # print(f.pos)

    def mover_pj(self,adicion_x,adicion_y):
        
        indice=0
        esta_en_diamantes=(self.coordenada_pj[0]+adicion_x,self.coordenada_pj[1]+adicion_y) in self.coor_diamantes
        esta_en_bombas=(self.coordenada_pj[0]+adicion_x,self.coordenada_pj[1]+adicion_y) in self.coor_bombas
        if  esta_en_diamantes or esta_en_bombas:
            
            if esta_en_diamantes:
                b=Blanco()
                b.pos=(self.coordenada_pj[0]+adicion_x,self.coordenada_pj[1]+adicion_y)
                App.get_running_app().root.get_screen('sc_game').ids.float_juego.ids.layout_diamantes.add_widget(b)
                self.num_diam-=1
                indice=self.coor_diamantes.index((self.coordenada_pj[0]+adicion_x,self.coordenada_pj[1]+adicion_y))
                self.coor_diamantes.pop(indice)
            elif esta_en_bombas:
                b=Explosion()
                b.pos=(self.coordenada_pj[0]+adicion_x,self.coordenada_pj[1]+adicion_y)
                App.get_running_app().root.get_screen('sc_game').ids.float_juego.ids.layout_bombas.add_widget(b)
                self.num_bombas-=1
                self.vidas-=1
                indice=self.coor_bombas.index((self.coordenada_pj[0]+adicion_x,self.coordenada_pj[1]+adicion_y))
                self.coor_bombas.pop(indice)
            # print(self.num_diam)
            # print(self.num_bombas)
        if self.coordenada_pj[0]+adicion_x>0 and self.coordenada_pj[0]+adicion_x<805:
            self.coordenada_pj[0]=self.coordenada_pj[0]+adicion_x
        if self.coordenada_pj[1]+adicion_y>170 and self.coordenada_pj[1]+adicion_y<800:
            self.coordenada_pj[1]=self.coordenada_pj[1]+adicion_y
        # print(self.coordenada_pj)
    
    def desaparecer_bombas(self,*args):
        App.get_running_app().root.get_screen('sc_game').ids.float_juego.ids.layout_bombas.clear_widgets()

    def verificar_num_diam(self,*args):
        if self.num_diam>0 and self.vidas>0:
            pass
        elif self.num_diam==0 and self.vidas>0:
            App.get_running_app().root.current='sc_victoria'
            self.evento.cancel()
            self.reinicializar_valores()
        elif self.num_diam>0 and self.vidas==0:
            App.get_running_app().root.current='sc_derrota'
            self.evento.cancel()
            self.reinicializar_valores()



class Diamante(Image):
    pass

class Bomba(Image):
    pass

class Explosion(Image):
    pass

class Vida(Image):
    pass

class Blanco(Image):
    pass

class Pantalla_victoria(Screen):
    pass

class Pantalla_derrota(Screen):
    pass

class MineroApp(App):
    screen_manager=ObjectProperty()
    def build(self):
        self.screen_manager = MineroWindow()
        return self.screen_manager

if __name__=='__main__':
    MineroApp().run()