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
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField

user="godwin"
import socket 
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('192.168.161.10',9999))
client.send("arunguru".encode())

def checkConnection():
    try:
              
        client.connect(('192.168.161.10',9999))
        client.send("arunguru".encode())

    except:
        pass

class replicator(MDApp):
    def removes(self):
        self.groupScreen.remove_widget(self.getGname)
    def adds(self):
        print("hello")
    def refresh(self):
        try:
            checkConnection()
            client.send("grouplist".encode())
            grouplist=client.recv(20000).decode()
            grouplist=grouplist.strip()
            grouplist=grouplist.split('\n')
            self.groupLabelAdd(grouplist)
            print(grouplist)
        except:
            print("no server")

    def creategroup(self):
        groupname=self.nameField.text
        print(groupname)
        client.send(f"creategroup {groupname}".encode())
        self.removes()

    def creategroupWin(self):
        self.getGname=MDCard(size_hint=(.8,.5),pos_hint={'center_x':0.5,'center_y':.5},elevation=2)
        self.layout=MDBoxLayout(orientation="vertical")
        self.closeBut=MDIconButton(icon='close',pos_hint={'center_x':.95},on_press= lambda x: self.removes())
        self.nameField=MDTextField(mode="round",pos_hint={'center_x':0.5,'center_y':.5})
        self.GetLabel=MDLabel(text="Enter the group name or Group link:")
        self.button=MDRaisedButton(text="create group",on_press=lambda x:self.creategroup(),pos_hint={'center_x':0.5,'center_y':.5})
        self.layout.add_widget(self.closeBut)
        self.layout.add_widget(self.GetLabel)
        self.layout.add_widget(self.nameField)
        self.layout.add_widget(self.button)
        self.getGname.add_widget(self.layout)
        self.groupScreen.add_widget(self.getGname)

         
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
            i=i.split(',')[1]
            self.groupLabels(i)

    def build(self):
        self.screenManager=MDScreenManager()
        self.MainScreen=MDScreen()
        self.banner=MDTopAppBar(title="Exam Replicator",pos_hint={'top':1},size_hint=(1,.1),md_bg_color=(1,0,0,9),elevation=0,
                                right_action_items= [["plus",lambda x:self.creategroupWin()],["refresh", lambda x: self.refresh()]])
        self.groupScreen=MDScreen(size_hint=(1,.89))
       
        self.gridView=MDBoxLayout(orientation='vertical',spacing=10,size_hint_y=None)
        


        self.MainScreen.add_widget(self.banner)
        self.MainScreen.add_widget(self.groupScreen)
        self.groupScreen.add_widget(self.gridView)
        
        self.screenManager.add_widget(self.MainScreen)
        return self.screenManager

replicator().run()