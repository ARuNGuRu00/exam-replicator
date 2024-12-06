from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard

class example(MDApp):
    def build(self):
        self.screen=MDScreen()
        self.scroll=MDScrollView(size_hint=(1,1))
        
        self.box=MDBoxLayout(orientation="vertical",size_hint=(1,None),pos_hint={'top':1},spacing=20)
        self.box.bind(minimum_height=self.box.setter('height'))
        for i in range(10):
            self.but=MDCard(md_bg_color=(1,1,0,1),size_hint=(1,None),height="400dp")
            self.box.add_widget(self.but)
        self.scroll.add_widget(self.box)
        self.screen.add_widget(self.scroll)
        return self.screen
example().run()