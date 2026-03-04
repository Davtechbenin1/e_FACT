#Coding:utf-8
"""
	Modèle de l'accueil de chaque partie
"""

from lib.davbuild import *
from General_surf import *

class Model_acc(float_l):
	def __init__(self,mother,**kwargs):
		kwargs['bg_color'] = mother.sc.aff_col1
		kwargs["radius"] = dp(10)
		float_l.__init__(self,mother,**kwargs)
	@Cache_error
	def initialisation(self):
		self.size_pos()
		self.but_dic = dict()
		self.icon_dic = dict()
		self.my_info_dict = dict()
		self.titre = str()
		self.y_label = list()
		self.data_dict = dict()
		self.cols = list()
		self.th_padd = 1
		
		#self.add_image('media/accueil.png',keep_ratio = False,
		#	size_hint = (.97,.97),pos_hint = (.015,.015))
		self.All_surf = stack(self,
			size_hint = (1,.92),pos_hint = (0,.08),
			padding = dp(20),spacing = dp(20))
		self.th_but_surf = box(self,size_hint = (1,.3),
			orientation = 'horizontal',padding = dp(30),
			spacing = dp(30))

		self.histo_part = box(self,size_hint = (.5,.69))
		
		self.All_surf.add_surf(self.th_but_surf)
		self.All_surf.add_padd((.25,.69))
		self.All_surf.add_surf(self.histo_part)
		self.add_surf(self.All_surf)
		
		self.mult = 0

	def Set_but_icon_info(self):
		...

	def size_pos(self):
		self.part_size = (.33,.15)

	def Set_histo_surf(self):
		self.histo_part.clear_widgets()
		self.histo_part.add_text(self.titre,font_size = '20sp',
			text_color = self.sc.green,halign = 'center',
			size_hint = (1,None),height = dp(30))

		data_liste = [(date,mont) for date,mont in self.data_dict.items()]

		if self.data_dict:
			max_y = max(self.data_dict.values())
		else:
			max_y = 0

		col = self.cols
		col_set = True
		if self.cols:
			col_set = False
		his_obj = box(self)
		self.histo_part.add_surf(his_obj)


	@Cache_error
	def Foreign_surf(self,*args):
		self.Set_but_icon_info()
		self.add_part_button()
		self.Set_histo_surf()

	def add_part_button(self):
		self.th_but_surf.clear_widgets()

		h = 1
		th_l = [i for i in self.but_dic.keys()]

		if len(th_l)%2:
			real_l = 5
		else:
			real_l = 6
		padd = int(abs(len(th_l) - real_l)/2)
		re_al = list()
		for i in range(padd):
			re_al.append(str())
		re_al.extend(th_l)
		for i in range(padd):
			re_al.append(str())

		self.th_but_surf.add_text("")
		for k in re_al:
			self._add_part_of(k,h)
		self.th_but_surf.add_text("")

	def _add_part_of(self,key,h):
		if key:
			icon = self.icon_dic.get(key)
			lenf = self.my_info_dict.get(key)
			th_b =box(self,bg_color = self.sc.green,
				size_hint = (None,h),padding = dp(1),
				radius = dp(20),width = dp(190))
			b_col = self.sc.aff_col1
			txt_col = self.sc.text_col1
			B = box(self,bg_color = b_col,
				padding = dp(20),
				radius = dp(20))
			th_b.add_surf(B)
			B.add_icon_but(icon = icon,size_hint = (1,.35),
				text_color = txt_col,
				font_size = "25sp",info = key,
				on_press = self.set_foreign_screen)
			B.add_button(key,size_hint = (1,.35),
				text_color = txt_col
				,on_press = self.set_foreign_screen,
				font_size = "18sp",bg_color = None,
				info = key,valign = "top")
			if lenf:
				B.add_button(self.format_val(lenf),size_hint = (1,.3),
					text_color = self.sc.orange, bold = True	,
					on_press = self.set_foreign_screen,
					font_size = "18sp",bg_color = None,
					info = key,valign = "top")
			self.th_but_surf.add_surf(th_b)
		

	@Cache_error
	def set_foreign_screen(self,wid):
		info = wid.info
		surf = self.but_dic.get(info)
		ret = self.sc.DB.Get_access_of(info)
		if ret == False :
			self.sc.add_refused_error(f"Accèss non autorisé! Veillez informer votre supérieur!!")
		if ret == None:
			...
		else:
			surf = surf(self,bg_color = self.sc.aff_col2)
			surf.add_all()
			self.add_modal_surf(surf,size_hint = (.96,.97),
				titre = wid.info)

