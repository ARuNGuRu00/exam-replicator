from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.core.clipboard import Clipboard

import socket
user="arunguru"
import socket 
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('localhost',9999))
client.send(user.encode())


class replicator(MDApp):
    def testlink(self,instance):
        self.testName=instance.ids.texts.text
        print(self.testName)
    def prin(self,instance):
        self.groupLink=instance.ids.texts.text
        self.groupLink=self.groupLink.split(" ")[0]
        for i in self.group:
            if self.groupLink==i.split(',')[1]:
                self.groupLink=i.split(',')[0]
                break
        client.send(f'retrive {self.groupLink}'.encode())
        print("send request for retrive")

        print(instance.ids.texts.text)
        self.manager.current="groupScreen"
        self.listOfTest=client.recv(3000).decode()
        self.listOfTest=self.listOfTest.split(',')
        print(self.listOfTest)
        if self.listOfTest !="":
            for i in self.listOfTest:
                if i!="":
                    print(i)
                    self.testTemp(i)
    def change(self,s):
        if s==0:
            self.manager.current="groupScreen"
        elif s==1:
            self.manager.current="mainScreen"
        elif s==1.5:
             self.manager.current="contactsScreen"
        elif s==2:
            self.manager.current="groupScreen"
    def createGroup(self):
        groupPort=self.smallCard.ids.box.ids.field.text
        groupPort=f"creategroup {groupPort}"
        print(f"creategroup {groupPort}")
        client.send(groupPort.encode())
        print("sent")
        self.getGroupDetails()
        self.mainScreen.remove_widget(self.smallCard)

    def getGroup(self):
        self.smallCard=MDCard(
            MDBoxLayout(
                MDIconButton(icon="close",pos_hint={"right":1},size_hint=(None,0.3),
                         on_press=lambda x:self.mainScreen.remove_widget(self.smallCard)),
                MDLabel(text="Enter a New Group Name or Enter Group link to join:", font_style="H6"),
                MDTextField(hint_text= "Enter over here",mode='rectangle',id="field"),
                MDRaisedButton(text="Create",on_press=lambda x:self.createGroup(),pos_hint={"right":1}),
                orientation="vertical",spacing=10,padding=20,id="box"),
            size_hint=(.8,None),height="200dp",pos_hint={"center_x":.5,"center_y":.7},)
        self.mainScreen.add_widget(self.smallCard)

    def testTemp(self,testname):
        self.tTemplate=MDCard(
                MDLabel(text=f"{testname}",padding="30dp",font_style="H6",id="texts"),
                MDIconButton(icon="dots-vertical",pos_hint={'center_x':1,"center_y":.7}),
                size_hint=(1,None),height="100dp",elevation=2,pos_hint={'center_x':.5,"center_y":.5},
                id="temp",
                )
        self.tTemplate.bind(on_press= self.testlink)
        self.gbox.add_widget(self.tTemplate)
    def groupCardTemp(self,groupName,status):
        self.gTemplate=MDCard(
                MDLabel(text=f"{groupName} ({status})",padding="30dp",font_style="H6",id="texts"),
                MDIconButton(icon="dots-vertical",pos_hint={'center_x':1,"center_y":.7}),
                size_hint=(1,None),height="100dp",elevation=2,pos_hint={'center_x':.5,"center_y":.5},
                id="temp",
                )
        self.gTemplate.bind(on_press = self.prin)

        self.box.add_widget(self.gTemplate)
    def getGroupDetails(self):
        try:
            client.send("grouplist".encode())
            grouplist=client.recv(20000).decode()
            grouplist=grouplist.strip()
            grouplist=grouplist.split('\n')
            print(grouplist)
            for i in grouplist:
                if i!="empty":
                    if i not in self.group:
                        i=i.split(',')
                        userId=i[0].split('-')
                        if userId[0]!=user:
                            self.groupCardTemp(i[-1],'external')
                        else:
                            self.groupCardTemp(i[-1],'group')
            self.group=grouplist

        except:
            pass
    def linkCopy(self):
        linkToCopy=f"http://examReplicator/{user}/{self.groupLink}"
        Clipboard.copy(linkToCopy)
    def clearG(self):
        self.manager.current='mainScreen'
        self.gbox.clear_widgets()
        
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        self.group=[]
        self.groupLink=""
        self.manager=MDScreenManager() 
        
        #maingroups
        self.mainScreen = MDScreen(
            MDTopAppBar(id="navbar",title="Replicator",pos_hint={'top':1},
                        right_action_items= [["plus",lambda x:self.getGroup()],["refresh",lambda x:self.getGroupDetails()]],
                        left_action_items= [["menu"]]),
            MDScrollView(id="scroll",size_hint=(1,0.87),),
            name="mainScreen",
        )
        self.box=MDBoxLayout(orientation='vertical',id="layout",size_hint=(1,None),spacing=10)
        self.box.bind(minimum_height=self.box.setter('height'))

        self.mainScreen.ids.scroll.add_widget(self.box)
        
        #group
        self.groupScreen = MDScreen(
            MDTopAppBar(id="navbar2",title="Replicator",pos_hint={'top':1},
                        right_action_items= [["link",lambda x:self.linkCopy()],["contacts",lambda x:self.change(1.5)],["refresh"]],
                        left_action_items= [["backburger",lambda x:self.clearG()]]),
            MDScrollView(id="scroll",size_hint=(1,0.87),),
            name="groupScreen",
                   
        )
        self.gbox=MDBoxLayout(orientation='vertical',id="layout2",size_hint=(1,None),spacing=10)
        self.gbox.bind(minimum_height=self.gbox.setter('height'))

        self.groupScreen.ids.scroll.add_widget(self.gbox)

        #contacts
        self.contactsScreen = MDScreen(
            MDTopAppBar(id="conNav",title="Replicator",pos_hint={'top':1},
                        right_action_items= [["refresh"]],
                        left_action_items= [["backburger",lambda x:self.change(2)]]),
            name="contactsScreen",
        )
        self.manager.add_widget(self.mainScreen)
        self.manager.add_widget(self.groupScreen)
        self.manager.add_widget(self.contactsScreen)
        self.getGroupDetails()
        return self.manager

replicator().run()