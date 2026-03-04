#Coding:utf-8
"""
	Surface de défintion de la surface de la gestion de stock
	Les fonctionnalités suivants sont à prendre à compte:
		- Gestion des articles
		- Achat d'arrivage
		- Perte de produit
		- Statistiques
		- Invesntaire
"""
from .stk_surf2 import *

class stock(float_l):
	def __init__(self,mother,**kwargs):
		kwargs['bg_color'] = mother.sc.aff_col1
		kwargs['radius'] = dp(10)
		float_l.__init__(self,mother,**kwargs)

	def initialisation(self):
		self.button_dic = self.This_infos_parts()
		self.size_pos()

	def size_pos(self):
		self.histo_part = box(self,size_hint = (.99,.45),
			pos_hint = (0.005,.545))
		self.button_part = stack(self,size_hint = (.99,.55),
			pos_hint = (0.005,.005),padding = dp(30),
			spacing = dp(30))
		self.add_surf(self.histo_part)
		self.add_surf(self.button_part)

	def Foreign_surf(self):
		self.add_button_part()

	def add_button_part(self):
		self.button_part.clear_widgets()
		icon_dic = {
			"Liste des articles": "format-list-bulleted",
			"Valider un arrivage": "truck-check",
			"Enrégistrement des pertes": "alert-circle-outline",
			"Inventaires de stock": "clipboard-list-outline",
			"Gestion des magasins virtuels": "store-outline",
			"Comptabilité des articles": "calculator-variant-outline",
			"Ajout d'un nouvel article":"plus-box-outline",
			"Historique":"history"
		}
		color_dic = {
			"Liste des articles": get_color_from_hex("#2196F3"),
			"Valider un arrivage":get_color_from_hex("#4CAF50"),
			"Enrégistrement des pertes": get_color_from_hex("#F44336"),
			"Inventaires de stock": get_color_from_hex("#FF9800"),
			"Gestion des magasins virtuels": get_color_from_hex("#3F51B5"),
			"Comptabilité des articles": get_color_from_hex("#009688"),
			"Ajout d'un nouvel article": get_color_from_hex("#1C6F00"),
			"Historique":self.sc.green
		}
		
		for key in self.button_dic.keys():
			b = float_l(self,size_hint = (.2,.25),
				)
			b1 = box(self,bg_color = self.sc.aff_col3,
				radius = dp(20),padding = dp(10),
				orientation = "horizontal")
			Get_border_surf(b,b1,self.sc.aff_col3)
			b1.add_icon_but(icon = icon_dic.get(key) or '',
				size_hint = (None,1),size = (dp(30),dp(1)),
				text_color = color_dic.get(key),font_size = '24sp')
			b1.add_text(key,italic = True, bold = True,
				font_size = "17sp")
			
			b.add_button("",bg_color = None,
				on_press = self.change_screen, 
				info = key)
			self.button_part.add_surf(b)
		for i in range(0,4):
			self.button_part.add_text('',size_hint = (.2,.25))

	def This_infos_parts(self):
		dic = {
			"Liste des articles":art_list,
			"Ajout d'un nouvel article": New_article,
			"Valider un arrivage":Appro_surf,
			"Enrégistrement des pertes":Perte_hand,
			"Historique":Historique_part,
			#"Inventaires de stock":Invent_hand,
			#"Gestion des magasins virtuels":Magasin_hand,
			
		}
		return dic

# Gestion des actions des buttons
	def change_screen(self,wid):
		info = wid.info
		ret = self.sc.DB.Get_access_of(info)
		if ret:
			srf = self.button_dic.get(wid.info)
			srf = srf(self,bg_color = self.sc.aff_col1)
			srf.add_all()
			self.add_modal_surf(srf,size_hint = (.8,.85),
				titre = wid.info)
		elif ret == False:
			self.sc.add_refused_error('Accès refusé !')

			Get_magasin_list

class Historique_part(stack):
	def initialisation(self):
		h = .05
		self.spacing = dp(5)
		self.padding = dp(10)
		self.history_part = "arrivages"
		self.history_list = ["arrivages","pertes"]
		
		self.add_text('historique des :',size_hint = (.1,h),)
		self.add_surf(liste_set(self,self.history_part,
			self.history_list,size_hint = (.2,h),
			mother_fonc = self.set_hist_part))

		self.add_surf(Periode_set(self,size_hint = (.4,h),
			info = 'Période :',info_w = .3,
			exc_fonc = self.add_all))
		self.histo_tab = Table(self,size_hint = (1,.9),
			exec_key = "N°")
		self.add_surf(self.histo_tab)

	def Foreign_surf(self):		
		if self.history_part == "arrivages":
			self.add_arrivage_hist()
		else:
			self.add_perte_hist()

	def add_arrivage_hist(self):
		self.histo_tab.exec_fonc = self.show_arrivage
		date_liste = self.get_date_list(self.day1,self.day2)
		arrive_lis = [self.sc.DB.Get_this_arrivage(id)
		for id in self.sc.DB.get_arrivages_ofs(date_liste)]
		wid_l = [.2]*5
		entete = ["date","nom fournisseur","nombre d'articles","magasin","montant HT"]
		self.histo_tab.Creat_Table(wid_l,entete,arrive_lis,
			ent_size = (1,.07))

	def add_perte_hist(self):
		self.histo_tab.exec_fonc = self.show_perte
		date_liste = self.get_date_list(self.day1,self.day2)
		arrive_lis = [self.sc.DB.Get_this_perte(id)
		for id in self.sc.DB.get_pertes_ofs(date_liste)]
		wid_l = [.2]*5
		entete = ["date","nombre d'articles","magasin","motif","montant HT"]
		self.histo_tab.Creat_Table(wid_l,entete,arrive_lis,
			ent_size = (1,.07))


# Gestion des actions des bouttons
	def show_arrivage(self,wid):
		...

	def show_perte(self,wid):
		...

	def set_hist_part(self,info):
		self.history_part = info
		self.add_all()


