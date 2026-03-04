#Coding:utf-8
"""
	Gestion de l'interface d'aide
"""
from lib.davbuild import *
from General_surf import *
from kivy.uix.videoplayer import VideoPlayer
from .Info_aide import dic

class Aide(box):
	@Cache_error
	def initialisation(self):
		self.spacing = dp(10)
		self.orientation = 'horizontal'
		self.Info_dic = dic
		self.curent_menu = "Présentation"
		self.Curent_vid = 'Introduction'
		self.size_pos()
		self.add_menu_part()

	def size_pos(self):
		self.menu_part = stack(self,bg_color = self.sc.aff_col1,
			size_hint = (.3,1),padding = dp(10),spacing = (10),
			radius = dp(10))

		self.video_part = box(self,bg_color = self.sc.aff_col1,
			size_hint = (.7,1),radius = dp(10))

		self.add_surf(self.menu_part)
		self.add_surf(self.video_part)

	def add_menu_part(self):
		h = .035
		self.menu_part.clear_widgets()
		self.menu_part.add_text("Liste des Vidéos d'aide",
			text_color = self.sc.text_col1,size_hint = (1,h),
			halign = 'center', font_size = "20sp",underline = True)
		index = 0
		for titre in self.Info_dic:
			index += 1
			titre_dic = self.Info_dic[titre]
			ti = f"{index} ->    {titre}"
			tex_col = self.sc.text_col1
			font_s = "15sp"
			if self.curent_menu == titre:
				tex_col = self.sc.green
				font_s = "17sp"
			self.menu_part.add_button(ti,size_hint = (1,h),
				bg_color = None,text_color = tex_col,
				font_size = font_s,padding_left = dp(30),
				halign = "left",on_press = self.change_menu,
				info = titre,)
			ht_ind = 0
			if self.curent_menu == titre:
				self.menu_part.add_padd((1,.001))
				for menu in titre_dic:
					ht_ind += 1
					inf = f"{index}.{ht_ind} ->    {menu}"
					tex_col = self.sc.text_col1
					font_s = "15sp"
					if self.Curent_vid == menu:
						tex_col = self.sc.orange
						font_s = "17sp"
						self.add_vid()
					self.menu_part.add_button(inf,size_hint = (1,h),
						bg_color = None,text_color = tex_col,
						font_size = font_s,padding_left = dp(50),
						halign = "left",info = menu,on_press = self.change_vid)
				self.menu_part.add_padd((1,.001))

	@Cache_error
	def add_vid(self):
		self.video_part.clear_widgets()
		src = self.Info_dic.get(self.curent_menu,dict()).get(self.Curent_vid)
		if src:
			vid = VideoPlayer(
					src = src
				)
			vid.layout = False
			self.video_part.add_surf(vid)
		self.video_part.add_text("Vidéo non disponible pour l'instant",
			text_color = self.sc.text_col1,
			halign = 'center', font_size = "20sp")

# Gestion des menus
	def change_menu(self,wid):
		self.curent_menu = wid.info
		self.Curent_vid = [i for i in self.Info_dic.get(self.curent_menu)][0]
		self.add_menu_part()

	def change_vid(self,wid):
		self.Curent_vid = wid.info
		self.add_menu_part()



