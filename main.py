# settings
from kivy.config import Config
Config.set('graphics','multisamples','0')
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
import threading
import requests
import socket
import webbrowser
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
import logging
logging.basicConfig(level=logging.DEBUG,
format="%(asctime)s - %(levelname)s - %(message)s"
)

kv = """
ScreenManager:
	Control:
	Setting:
	
<Control>:
	name:"home"
	MDBoxLayout:
		orientation:"vertical"
		canvas.before:
			Color:
				rgba:1,1,1,1
			Rectangle:
				pos:self.pos
				size:self.size
				source:"my_tkinter_images/Rc.png"
	MDTopAppBar:
    	title: "RC Controller"
    	md_bg_color:0,0,1,1
    	pos_hint: {"top": 1}
    	elevation: 4
    	right_action_items: [["cog", lambda x: app.setting_screen()]]
	MDFloatLayout:
		MDCard:
			size_hint:0.5,0.3
			pos_hint:{"center_x":0.4,"center_y":0.5}
			md_bg_color:(0,0,1,1)
		
		MDIconButton:
			icon:"arrow-left-box"
			icon_size:"70sp"
			pos_hint:{"center_x":0.230,"center_y":0.5}
			on_release:app.send("Backward")
		MDIconButton:
			icon:"arrow-right-box"
			icon_size:"70sp"
			pos_hint:{"center_x":0.570,"center_y":0.5}
			on_release:app.send("Forward")
		MDIconButton:
			icon:"arrow-up-box"
			theme_text_color:"Custom"
			icon_color:0,1,0,1
			icon_size:"70sp"
			pos_hint:{"center_x":0.410,"center_y":0.6}
			on_release:app.send("Left")
		MDIconButton:
			icon:"arrow-down-box"
			theme_text_color:"Custom"
			icon_color:0,1,0,1
			icon_size:"70sp"
			pos_hint:{"center_x":0.410,"center_y":0.4}
			on_release:app.send("Right")
		MDIconButton:
			icon:"stop-circle-outline"
			icon_size:"70sp"
			theme_text_color:"Custom"
			icon_color:1,0,0,1
			pos_hint:{"center_x":0.40,"center_y":0.5}
			on_release:app.send("Stop")
		MDLabel:
			id:home_status
			font_style:"H4"
			theme_text_color:"Custom"
			text_color:1,0,0,1
			pos_hint:{"center_x":0.760,"center_y":0.7}
			
		MDBoxLayout:
			orientation:"vertical"
			size_hint:0.8,0.2
			pos_hint:{"center_x":0.5,"center_y":0.25}
			MDLabel:
				text:"Speed"
				font_style:"H5"
				theme_text_color:"Custom"
				text_color:0,0,0.8,1
				pos_hint:{"x":0.3,"center_y":0.3}
        	MDSlider:
				min:1
				max:100
				size_hint_x:0.7
				pos_hint:{"center_x":0.4,"center_y":0.250}
				thumb_color_active:1,0,0,1
				track_color_active:0,1,0,1
				track_color_inactive:1,1,1,1
				on_touch_up:app.change_speed(self.value)
	MDBoxLayout:
		orientation:"horizontal"
		spacing:dp(20)
		size_hint:0.8,0.2
		pos_hint:{"center_x":0.640,"center_y":0.870}
		MDIconButton:
			id:toggle_light
			icon:"lightbulb-off-outline"
			theme_text_color:"Custom"
			icon_color:1,1,1,1
			icon_size:"60sp"
			on_release:app.light_control()
		MDIconButton:
			id:toggle_buzzer
			icon:"volume-off"
			theme_text_color:"Custom"
			icon_color:1,0,0,1
			icon_size:"60sp"
			on_release:app.toggle_horn()
	
<Setting>:
	name:"setting"
	MDBoxLayout:
		canvas.before:
			Color:
				rgba:1,1,1,1
			Rectangle:
				pos:self.pos
				size:self.size
				source:"my_tkinter_images/RCsetting.png"
		MDTopAppBar:
    		title: "RC Controller"
    		md_bg_color:0,0,1,1
    		pos_hint: {"top": 1}
    		elevation: 4
    		left_action_items: [["arrow-left", lambda x: app.Home_screen()]]
	MDFloatLayout:
		MDLabel:
			text:"DEVICE CONNECTION"
			font_style:"H4"
			pos_hint:{"center_x":0.7,"center_y":0.850}
			theme_text_color:"Custom"
			text_color:1,1,1,1
		MDCard:
			size_hint:0.7,0.2
			pos_hint:{"center_x":0.5250,"center_y":0.7}
		MDTextField:
			id:ip_input
			hint_text:"Enter IP address"
			icon_right:"ip"
			pos_hint:{"center_x":0.520,"center_y":0.770}
			size_hint_x:0.670
			mode:"rectangle"
		MDRaisedButton:
			text:"CONNECT"
			pos_hint:{"center_x":0.5,"center_y":0.670}
			on_release:app.connect()
		MDLabel:
			id:setting_status
			font_style:"H5"
			pos_hint:{"center_x":.8,"center_y":0.5}
			theme_text_color:"Custom"
			text_color:0,1,0,1
		MDLabel:
			text:"View Source Code on GitHub"
			halign:"center"
			font_style:"H6"
			theme_text_color:"Custom"
			text_color:1,1,1,1
			pos_hint:{"center_x":0.5,"center_y":0.450}
		MDIconButton:
			icon:"github"
			theme_text_color:"Custom"
			icon_color:1,1,1,1
			icon_size:"70sp"
			pos_hint:{"center_x":0.5,"center_y":0.4}
			on_release:app.open_github()	
			
				
			
		


"""

class Setting(MDScreen):
	pass
class Control(MDScreen):
	pass
class RcApp(MDApp):
	def build(self):
		self.store = JsonStore("settings.json")
		self.base_url = None
		Window.bind(on_keyboard=self.back_button)
		if self.store.exists("connection"):
			ip = self.store.get("connection")["ip"]
			self.base_url = f"http://{ip}"
            

		return Builder.load_string(kv)
	def is_connected(self):
		try:
			socket.create_connection(("8.8.8.8",53),2)
			return True
		except:
			return False		
	def light_control(self):
		btn = self.root.get_screen("home").ids.get("toggle_light")
		if btn:
			if btn.icon == "lightbulb-off-outline":
				btn.icon = "lightbulb-on-outline"
				btn.icon_color=1,1,0,1
				self.send("LightOn")
			else:
				btn.icon = "lightbulb-off-outline"
				btn.icon_color=1, 1, 1, 1
				self.send("LightOff")
	def toggle_horn(self):
		btn = self.root.get_screen("home").ids.get("toggle_buzzer")
		if btn:
			if btn.icon == "volume-off":
				btn.icon = "trumpet"
				btn.icon_color = 1,0,1,1
				self.send("BuzzerOn")
			else:
				btn.icon = "volume-off"
				btn.icon_color = 1,0,0,1
				self.send("BuzzerOff")
			
	def setting_screen(self):
		self.root.current = "setting"
	def Home_screen(self):
		self.root.current = "home"
	def connect(self):
		if not self.is_connected():
			self.root.get_screen("setting").ids.setting_status.text = "No Internet"
			return

		ip = self.root.get_screen("setting").ids.ip_input.text.strip()
		if not ip:
			self.root.get_screen("setting").ids.setting_status.text = "Status: Enter first IP"
			self.root.get_screen("setting").ids.setting_status.text_color = (1,0,0,1)
			return
		self.base_url = f"http://{ip}"
		self.store.put("connection",ip=ip)
		# save IP
  

		threading.Thread(target=self.test_connection,daemon=True).start()

	def test_connection(self):
		try:
			requests.get(self.base_url,timeout=3)
			Clock.schedule_once(lambda dt:self.update_status("Connected"))
		except:
			Clock.schedule_once(lambda dt:self.update_status("Connection Failed"))
	def update_status(self,msg):
		label = self.root.get_screen("setting").ids.setting_status.text = f"Status: {msg}"
		if msg == "Connected":
			self.root.get_screen("home").ids.home_status.text = "Connected"
    
		
	
	def send(self,cmd):
		if not self.base_url:
			self.root.get_screen("home").ids.home_status.text = "Not Connected"
			return
		threading.Thread(target=self.send_request,args=(cmd,),daemon = True).start()
	def send_request(self,cmd):
		try:
			requests.get(f"{self.base_url}/{cmd}",timeout=2)
		except:
			Clock.schedule_once(lambda dt:
				setattr(self.root.get_screen("home").ids.home_status,"text" ,"Error Sending"))
		
	def change_speed(self,value):
		speed = int(value)
		threading.Thread(target=self.speed_request,args=(speed,),daemon=True).start()
		
	def speed_request(self,speed):		
		try:
			requests.get(f"{self.base_url}/speed?value={speed}",timeout=2)
			Clock.schedule_once(lambda dt:
				setattr(self.root.get_screen("home").ids.home_status,"text",f"Speed: {speed}"))
		except:
			self.root.get_screen("home").ids.home_status.text = f"Speed Error"
								
		
	def open_github(self):
		webbrowser.open("https://github.com/ajeet-sahani/RC-Controller-Code")
	def back_button(self,window,key,*args):
		if key==27:
			if self.root.current!="home":
				self.root.current="home"
				return True
		return False
			
               


    	 												
		
if __name__ == "__main__":
 	RcApp().run()