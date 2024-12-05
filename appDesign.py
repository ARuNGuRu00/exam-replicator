from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window

user="arunguru"
import socket 
try:
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(('localhost',9999))
    client.send("arunguru".encode())
except:
    pass
class replicator(MDApp):
    def adds(self):
        print("hello")
    def refresh(self):
        try:
            client.send("grouplist".encode())
            grouplist=client.recv(20000).decode()
            grouplist=grouplist.strip()
            grouplist=grouplist.split('\n')
            self.groupLabelAdd(grouplist)
            print(grouplist)
        except:
            print("no server")
    def creategroup(self,groupname):
        try:
            groupname=input()
            client.send(f"creategroup {groupname}".encode())
            print("create group..")
        except:
            print("no server")
    def groupLabels(self,listTitle):
        self.groupLabel=MDCard(size_hint=(None,None),size=(Window.width,Window.height/4),md_bg_color=(1,0,0,.2),padding="2dp")
        self.label=MDLabel(text=f"{listTitle}",size=(.5,.7),padding="20dp",font_style='H6')
        self.gMenu=MDIconButton(icon='dots-vertical',pos_hint={'top':1})
        self.groupLabel.bind(on_press=lambda x:self.adds())

        self.groupLabel.add_widget(self.label)
        self.groupLabel.add_widget(self.gMenu)
        self.gridView.add_widget(self.groupLabel)
    def groupLabelAdd(self,lists):
        for i in lists:
            i=i[len(user)+1:]
            self.groupLabels(i)

    def build(self):
        self.screenManager=MDScreenManager()
        self.MainScreen=MDScreen()
        self.banner=MDTopAppBar(title="Exam similator",pos_hint={'top':1},size_hint=(1,.1),md_bg_color=(1,0,0,9),elevation=0,
                                right_action_items= [["plus",lambda x:self.creategroup("au")],["refresh", lambda x: self.refresh()]])
        self.groupScreen=MDScreen(size_hint=(1,.89))
       
        self.gridView=MDBoxLayout(orientation='vertical',spacing=10,size_hint_y=None)
        


        self.MainScreen.add_widget(self.banner)
        self.MainScreen.add_widget(self.groupScreen)
        self.groupScreen.add_widget(self.gridView)
        
        self.screenManager.add_widget(self.MainScreen)
        return self.screenManager

replicator().run()