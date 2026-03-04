#Coding:utf-8
"""
	Gestion des fournisseurs
"""
from lib.davbuild import *
from General_surf import *
from .fr_surf1 import *

class Fournisseur(box):
	@Cache_error
	def initialisation(self):
		self.orientation = 'horizontal'
		self.padding = [dp(2),dp(2),dp(2),0]
		self.spacing = dp(2)
		self.this_fourn = str()
		self.size_pos()
		self.Init()

	def Init(self):
		self.th_type = str()
		self.th_sect = str()
		self.th_name = str()
		self.th_sect_list = list()
		self.New_fourn = False
		self.New_dic = {
			"nom":str(),
			"IFU":str(),
			"RCCM":str(),
			"addresse":str(),
			"email":str(),
			"téléphone":str(),
			"whatsapp":str(),
			"nom directeur":str(),
			"tél directeur":str(),
			"solde":'0',
		}
		self.perso_cont = dict()
#
	def size_pos(self):
		w,h = self.liste_f_size = (.34,1)
		self.aff_fourn_size = 1-w,h

		self.liste_f_surf = stack(self,size_hint = self.liste_f_size,
			padding = dp(10),radius = dp(10),spacing = dp(5),
			bg_color = self.sc.aff_col1)
		self.aff_fourn_surf = box(self,size_hint = self.aff_fourn_size,
			radius = dp(10),
			bg_color = self.sc.aff_col1)

		self.add_surf(self.liste_f_surf)

	@Cache_error
	def Foreign_surf(self):
		fourn_l = self.sc.DB.Get_fournisseur_list()
		self.all_fournisseur = {i:self.sc.DB.Get_fourn_by_name(i)
			for i in fourn_l}
		self.add_liste_f_surf()

	@Cache_error
	def add_liste_f_surf(self):
		h = .045
		self.liste_f_surf.clear_widgets()
		"""
		self.liste_f_surf.add_text('Liste des Fournisseurs',
			text_color = self.sc.text_col1,halign = "center",
			font_size = "17sp",underline = True,size_hint = (.95,h))
		self.liste_f_surf.add_icon_but(icon = 'printer',
			text_color = self.sc.black,on_press = self.Impression,
			size_hint = (.05,.035))
		self.liste_f_surf.add_text('Types :',text_color = self.sc.text_col1,
			size_hint = (.1,h))
		self.liste_f_surf.add_surf(liste_set(self,self.th_type, 
			self.sc.DB.Get_all_f_types(),size_hint = (.2,h),mult = 1,
			mother_fonc = self.set_type))
		self.liste_f_surf.add_text('Secteurs :',text_color = self.sc.text_col1,
			size_hint = (.1,h))
		self.liste_f_surf.add_surf(liste_set(self,self.th_sect, 
			self.sc.DB.Get_Secteurs(),size_hint = (.2,h),mult = 1,
			mother_fonc = self.set_sect))
		"""
		self.liste_f_surf.add_padd((.35,h))
		self.liste_f_surf.add_input("nom",on_text = self.set_name,
			default_text = self.th_name,size_hint = (.3,h),
			placeholder = 'Trier par nom',bg_color = self.sc.aff_col3)
		#if "écritures" in self.sc.DB.Get_access_of('Fournisseur'):
		#	self.liste_f_surf.add_icon_but(icon = "plus",
		#		size_hint = (.05,h),on_press = self.add_fourn,
		#		text_color = self.sc.green)
		self.ths_tab = Table(self,size_hint = (1,.9),padding = dp(10),
			radius = dp(10),exec_fonc = self.show_fourn,
			exec_key = 'N°',bg_color = self.sc.aff_col3)
		self.liste_f_surf.add_surf(self.ths_tab)
		self.Up_tab()

	@Cache_error
	def Up_tab(self):
		entete = ["nom","IFU","RCCM","type de fournisseur",
			"Secteur d'activité","solde","téléphone"]
		wid_l = [.22,.13,.13,.13,.13,.13,.13]
		liste = self.Trie_fournisseur()
		self.ths_tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.05))

	def Trie_fournisseur(self):
		liste = [i for i in map(self.Trie,
			self.all_fournisseur.values()) if i]
		
		return liste

	def Trie(self,dic):
		if dic:
			if self.th_type:
				if self.th_type.lower() != dic.get('type de fournisseur').lower():
					return None
			if self.th_sect:
				if self.th_sect not in dic.get("secteur d'activité"):
					return None
			if self.th_name.lower() not in dic.get('nom').lower():
				return None
			sect_l = dic.get("secteur d'activité")
			esct = ', '.join(sect_l)
			dic["Secteur d'activité"] = esct
			return dic

	@Cache_error
	def add_New_fourn(self):
		h = .035
		th_box_info = stack(self,bg_color = self.sc.aff_col1,
			padding = dp(10),spacing = dp(10))
		self.add_modal_surf(th_box_info,titre = 'Nouveau fournisseur',
			size_hint = (.5,.95))
		
		th_box_info.add_text('Types :',text_color = self.sc.text_col1,
			size_hint = (.2,h))
		th_box_info.add_surf(liste_set(self,self.th_type, 
			self.sc.DB.Get_all_f_types(),size_hint = (.8,h),mult = 1,
			mother_fonc = self.set_type))

		th_box_info.add_text('Secteurs :',text_color = self.sc.text_col1,
			size_hint = (.2,h))
		th_box_info.add_input('nom',default_text = self.th_sect,
			on_text = self.set_th_sect,placeholder = 'Nouvel secteur',
			size_hint = (.6,h),text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3)
		th_box_info.add_button('add',size_hint = (.1,h),
			bg_color = self.sc.aff_col2,text_color = self.sc.text_col3,
			on_press = self.add_secteur)
		th_box_info.add_surf(liste_choice(self,self.th_sect_list,
			self.sc.DB.Get_Secteurs_list(),mother_fonc = self.set_sect_list,
			size_hint = (1,h*6)))
		for k,v in self.New_dic.items():
			th_box_info.add_text_input(k,(.2,h),(.3,h),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				default_text = str(v),placeholder = k,on_text = self.set_new_dict)
		th_box_info.add_text('Personnes à contacter',text_color = self.sc.text_col1,
			halign = 'center', size_hint = (1,h))
		tabs = dynamique_tab(self,size_hint = (1,h*8))
		wid_l = [.7,.3]
		entete = 'Nom',"Contact"
		tabs.Creat_Table(wid_l,entete,mother_fonc = self.set_person)
		th_box_info.add_surf(tabs)
		th_box_info.add_padd((.25,h))
		th_box_info.add_button('Valider',size_hint = (.5,h*1.3),
			bg_color = self.sc.aff_col2,text_color = self.sc.text_col3,
			on_press = self.Add_fournisseur)

# Gestions des actions des méthodes
	@Cache_error
	def Impression(self,wid):
		obj = self.sc.imp_part_dic('Résumé')(self)
		liste = self.Trie_fournisseur()
		entete = ["nom","type de fournisseur","Secteur d'activité",
			"solde","téléphone"]
		wid_l = .2,.2,.2,.2,.2
		titre = "Liste des fournisseurs"
		info = str()
		if self.th_type:
			info += f"Type de fournisseur : {self.th_type}<br/>"
		if self.th_sect:
			info += f"Secteur d'activité : {self.th_sect}<br/>"
		info += 'Agence TOKPOTA1'
		obj.Create_fact(wid_l,entete,liste,titre,info)

	@Cache_error
	def show_fourn(self,wid):
		if wid.info:
			self.this_fourn = wid.info
			four_info = self.sc.DB.Get_this_fournisseur(self.this_fourn)
			surf = Gestion_cmds(self,four_info,bg_color = self.sc.aff_col1)
			surf.add_all()
			self.add_modal_surf(surf,size_hint = (.8,.95),
				titre = f"Gestion du fournisseur N° {wid.info}")
		else:
			self.sc.add_refused_error('Erreur pas de N° connu !')

	def set_new_dict(self,wid,val):
		if wid.info == 'solde':
			wid.text = self.regul_input(wid.text)
			self.New_dic["solde"] = wid.text
		else:
			self.New_dic[wid.info] = val

	def add_fourn(self,wid):
		self.add_New_fourn()

	@Cache_error
	def add_secteur(self,wid):
		if self.th_sect and self.th_sect not in self.sc.DB.Get_Secteurs_list():
			self.excecute(self.sc.DB.Save_secteurs,self.th_sect)
			#self.sc.DB.Save_secteurs(self.th_sect)
			self.sc.add_refused_error('Secteur Bien ajouter !')
			self.th_sect = str()
			self.add_New_fourn()
		else:
			self.sc.add_refused_error('Secteur existe déjà')

	def set_person(self,liste):
		dic = dict()
		for d in liste:
			dic[d.get('Nom')] = d.get('Contact')
		self.perso_cont = dic

	def set_th_sect(self,wid,val):
		self.th_sect = val

	def set_sect_list(self,liste):
		self.th_sect_list = liste

	def set_type(self,info):
		self.th_type = info
		self.Up_tab()

	def set_sect(self,info):
		self.th_sect = info
		self.Up_tab()

	def set_name(self,wid,val):
		self.th_name = val
		self.Up_tab()
#
	@Cache_error
	def Add_fournisseur(self,wid):
		if self.New_dic.get('nom'):
			#if self.th_type and self.th_sect_list:
			dic = self.sc.DB.Get_fournisseur_info()
			dic.update(self.New_dic)
			dic['personnes à contacter'] = self.perso_cont
			dic["type de fournisseur"] = self.th_type
			dic["secteur d'activité"] = self.th_sect_list
			dic['solde'] = int(self.New_dic['solde'])
			self.excecute(self.sc.DB.Save_fournisseur,dic)
			self.sc.add_refused_error('Fournisseurs sauvegardé avec succès!')
			self.Init()
			self.Back(wid)
		else:
			self.sc.add_refused_error('Il faut renseigner au moin le nom')

	def Back(self,wid):
		self.New_fourn = False
		self.add_all()
