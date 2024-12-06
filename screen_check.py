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
    def accountTemp(self,member):
        self.cTemplate=MDCard(
                MDLabel(text=f"{member}",padding="30dp",font_style="H6",id="texts"),
                MDIconButton(icon="dots-vertical",pos_hint={'center_x':1,"center_y":.7}),
                size_hint=(1,None),height="100dp",elevation=2,pos_hint={'center_x':.5,"center_y":.5},
                id="temp",
                )
        #self.cTemplate.bind(on_press= self.testlink)
        self.cbox.add_widget(self.cTemplate)
    def community(self,groupid):
        client.send(f'community {groupid}'.encode())
        print("sent community requiest")
        self.accessControl=client.recv(60000).decode()
        self.accessControl=self.accessControl.split("\n")
        print(self.accessControl)
        self.manager.current="contactsScreen"
        for i in self.accessControl[1:]:
            if i!="":
                self.accountTemp(i)

    def writeTest(self,Qpaper):
        
        self.manager.add_widget(self.WriteScreen)
        self.manager.current='WriteScreen'
        self.TestLabel=MDLabel()
        self.wbox.add_widget(self.TestLabel)
        self.Question=MDLabel()
        self.wbox.add_widget(self.Question)
        self.getOptions=MDTextField(id="option",mode='rectangle',hint_text="Answer")
        self.wbox.add_widget(self.getOptions)
        self.sumit=MDRaisedButton(id="submit",text="post",on_press=lambda x:self.answerpost())
        self.wbox.add_widget(self.sumit)
    def testlink(self,instance):
        self.testName=instance.ids.texts.text
        print(self.testName)
        
    
    def parallel(self,instance):
        self.i=instance
        self.create(instance)
        self.prin(instance)
       
    def create(self,instance):
        self.admin=instance.ids.texts.text
        self.admin=self.admin.split(" ")
        print(self.admin)
        if self.admin[1]=="(group)":
            self.tTemplate=MDCard(
                MDRaisedButton(text="createTest",pos_hint={'right':.5,'center_y':.5},on_press=lambda x:self.createTest()),
                size_hint=(1,None),height="100dp",elevation=2,
                id="temp",
                )
            self.tTemplate.bind(on_press= self.testlink)
            self.gbox.add_widget(self.tTemplate)
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
                    self.testTemp(i,)
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
        self.gTemplate.bind(on_press = self.parallel)

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
    def backg(self):
        self.manager.current='groupScreen'
        self.cbox.clear_widgets()
    def post(self):
        self.paper="paper "
        nameTest=self.getTestName.text
        question=self.getQuestion.text
        options=self.getOptions.text
        answer=self.getAnswer.text
        for i in [nameTest,question,options,answer,self.groupLink]:
            self.paper+=f"{i},"
        print(self.paper)
        client.send(self.paper.encode())
        self.ttbox.clear_widgets()
        self.gbox.clear_widgets()
        self.parallel(self.i)
        self.manager.current="groupScreen"
        self.manager.remove_widget(self.testTemplateScreen)
        
    def createTest(self):
        self.manager.add_widget(self.testTemplateScreen)
        self.manager.current='testTemplate'
        self.getTestName=MDTextField(id='testname',mode='rectangle',hint_text="Enter the test name")
        self.ttbox.add_widget(self.getTestName)
        self.getQuestion=MDTextField(id="question",mode='rectangle',hint_text="Question: ex:Mobile App contest conducted in?")
        self.ttbox.add_widget(self.getQuestion)
        self.getOptions=MDTextField(id="option",mode='rectangle',hint_text="Options: ex:mec,mit,miet")
        self.ttbox.add_widget(self.getOptions)
        self.getAnswer=MDTextField(id="answer",mode='rectangle',hint_text="Answer : ex:mec")
        self.ttbox.add_widget(self.getAnswer)
        self.sumit=MDRaisedButton(id="submit",text="post",on_press=lambda x:self.post())
        self.ttbox.add_widget(self.sumit)
    def draft(self):
        self.manager.current='groupScreen'
        self.manager.remove_widget(self.testTemplateScreen)
    #main
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
                        right_action_items= [["link",lambda x:self.linkCopy()],["contacts",lambda x:self.community(self.groupLink)],["refresh"]],
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
                        left_action_items= [["backburger",lambda x:self.backg()]]),
            MDScrollView(id="scroll",size_hint=(1,0.87),),
            name="contactsScreen",
        )
        self.cbox=MDBoxLayout(orientation='vertical',id="layout2",size_hint=(1,None),spacing=10)
        self.cbox.bind(minimum_height=self.cbox.setter('height'))

        self.contactsScreen.ids.scroll.add_widget(self.cbox)
        #testcreate template
        self.testTemplateScreen = MDScreen(
            MDTopAppBar(id="navbar",title="Replicator",pos_hint={'top':1},
                        left_action_items=[['close',lambda x:self.draft()]]),

            MDScrollView(id="scroll",size_hint=(1,0.87),),
            name="testTemplate",
        )
        self.ttbox=MDBoxLayout(orientation='vertical',id="layout3",size_hint=(1,None),spacing=30)
        self.ttbox.bind(minimum_height=self.ttbox.setter('height'))

        self.testTemplateScreen.ids.scroll.add_widget(self.ttbox)
        
        self.manager.add_widget(self.mainScreen)
        self.manager.add_widget(self.groupScreen)
        self.manager.add_widget(self.contactsScreen)
        self.getGroupDetails()
        return self.manager

replicator().run()