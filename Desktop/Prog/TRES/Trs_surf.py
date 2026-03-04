#Coding:utf-8
"""
	Ensemble de surface de trésorerie pour une bonne gestion de la
	partie trésorerie.

	Impossible de continuer à cause d'une restriction système !! Parlez-en à votre supérieur hiérachique
"""
from lib.davbuild import *
from General_surf import *
from ..CMPT.trs_surf2 import *
from ..CMPT.paie_surfs import *
from ..CREAN.cre_all_use import *

class Tresorerie(box):
	@Cache_error
	def initialisation(self):
		self.size_pos()
		self.menu_ico_dic = {
			#"Encaissements":"cash-plus",
			"Décaissement":"cash-minus",
			"Montants accessoires":"cash",
			"Trésorerie interne":"bank-check",
			"Déversement comptable":"archive-outline",
			"Point financier":"cash-multiple",
			"Mouvement financier":'swap-horizontal',
			
		}
		dic = {
			#"Encaissements":encaiss_en_attente,
			"Décaissement":decaissement,
			"Montants accessoires":Mont_Access,
			"Trésorerie interne":show_details,
			"Déversement comptable":N_devers,
			"Point financier":P_finan,
			"Mouvement financier":Mouv_F,
			
		}
		self.menu_surf_dic = dict()
		for i,srf in dic.items():
			self.menu_surf_dic[i] = srf

		self.menu_in_action = str()

	@Cache_error
	def size_pos(self):
		w,h = self.menu_size = 1,.039
		self.aff_size = w,1-h

		self.menu_surf = stack(self,size_hint = self.menu_size,
			bg_color = self.sc.aff_col3,radius = [dp(10),dp(10),0,0])

		self.aff_surf = box(self,size_hint = self.aff_size,
			bg_color = self.sc.aff_col1,radius = [0,0,dp(10),dp(10)])

		self.add_surf(self.menu_surf)
		self.add_text('',size_hint = (1,None),height = dp(1))
		self.add_surf(self.aff_surf)

	@Cache_error
	def Foreign_surf(self):
		self.add_menu_surf()

	def add_menu_surf(self):
		self.menu_surf.clear_widgets()
		self.aff_surf.clear_widgets()
		for menu,surf in self.menu_surf_dic.items():
			txt_col = self.sc.text_col1
			bg_color = None
			if not self.menu_in_action:
				self.menu_in_action = menu
			if menu == self.menu_in_action:
				surf = surf(self)
				surf.add_all()
				self.aff_surf.add_surf(surf)
				txt_col = self.sc.green

			ico = self.menu_ico_dic.get(menu)
			self.menu_surf.add_icon_but(icon = ico,info = menu,
				text_color = txt_col,on_press = self.change_screen,
				size_hint = (None,1),size = (dp(40),dp(20)),font_size = "34sp")
			self.menu_surf.add_button(menu,info = menu,text_color = txt_col,
				on_press = self.change_screen,bg_color = bg_color,size_hint = (None,1),
				width = dp(100),halign = "left")

# Gestion des actions des bouttons
	@Cache_error
	def change_screen(self,wid):
		Window.set_system_cursor('wait')
		info = wid.info
		ret = self.sc.DB.Get_access_of(info)
		if ret:
			self.menu_in_action = wid.info
			self.add_menu_surf()
		elif ret == False:
			self.sc.add_refused_error('Accès refusé !')

		Window.set_system_cursor('arrow')

class Mont_Access(box):
	@Cache_error
	def initialisation(self):
		self.orientation = "horizontal"
		self.padding = dp(1)
		self.spacing = dp(1)
		self.th_part = str()
		self.lib = str()
		self.size_pos()

	@Cache_error
	def Foreign_surf(self):
		self.part_lise = [self.sc.DB.Get_this_part_nom(i) for i in 
			self.sc.DB.Get_all_partenaires().keys()]
		self.add_liste_surf()

	def size_pos(self):
		self.part_lise = [self.sc.DB.Get_this_part_nom(i) for i in 
			self.sc.DB.Get_all_partenaires().keys()]
		w,h = self.liste_size = .4,1
		self.aff_size = 1-w,h

		self.liste_surf = stack(self,size_hint = self.liste_size,
			bg_color = self.sc.aff_col1,radius = [dp(10),0,0,dp(10)],
			padding = dp(10),spacing = dp(10))
		self.aff_surf = show_M_access(self,size_hint = self.aff_size,
			bg_color = self.sc.aff_col1,radius = [0,dp(10),dp(10),0],
			padding = dp(10),spacing = dp(10))

		self.add_surf(self.liste_surf)
		self.add_text("",size_hint = (None,1),width = dp(1),
			bg_color = self.sc.sep)
		self.add_surf(self.aff_surf)

	@Cache_error
	def add_liste_surf(self):
		h = .045
		
		self.liste_surf.clear_widgets()
		self.liste_surf.add_text("Liste des montants accessoires",
			size_hint = (.8,h),halign = "center",underline = True,
			text_color = self.sc.text_col1)
		if "écritures" in self.sc.DB.Get_access_of("Montants accessoires"):
			self.liste_surf.add_icon_but(icon = 'plus',size_hint = (.2,h),
				on_press = self.set_new_mont,text_color = self.sc.green)
		self.liste_surf.add_text('Partenaire associé',text_color = self.sc.text_col1,
			size_hint = (.3,h))
		self.liste_surf.add_surf(liste_set(self,self.th_part,self.part_lise,size_hint = (.6,h),
			mult = 1,mother_fonc = self.set_th_part))
		self.tab = Table(self,size_hint = (1,.89),bg_color = self.sc.aff_col3,
			padding = dp(10),radius = dp(10),exec_key = "N°",
			exec_fonc = self.show_det_acess)
		self.liste_surf.add_surf(self.tab)
		self.Up_tab()

	@Cache_error
	def New_M_access(self):
		h = .045
		self.liste_surf.clear_widgets()
		self.liste_surf.add_text("Nouveau montant accessoire",
			size_hint = (.8,h),halign = "center",underline = True,
			text_color = self.sc.text_col1)
		self.liste_surf.add_icon_but(icon = 'close',size_hint = (.2,h),
			on_press = self.close,text_color = self.sc.red,font_size = '34sp')
		self.liste_surf.add_text('Partenaire associé',text_color = self.sc.text_col1,
			size_hint = (.3,h))
		self.liste_surf.add_surf(liste_set(self,self.th_part,self.part_lise,size_hint = (.6,h),
			mult = 1,mother_fonc = self.set_th_part))
		self.liste_surf.add_text_input("libelé",(.3,h),(.6,h),self.sc.text_col1,
			bg_color = self.sc.aff_col3,text_color = self.sc.text_col1,
			on_text = self.set_lib)

		self.liste_surf.add_button_custom('Ajouter',self.new_mont,size_hint = (.4,h),
			padd = (.3,h),bg_color = self.sc.orange,text_color = self.sc.text_col1)

	@Cache_error
	def Up_tab(self):
		entete = "libelé","partenaire","décaissement","solde actuel"
		wid_l = .3,.25,.22,.23
		liste = self.Trie_info()
		self.tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.06))

	def Trie_info(self):
		liste = self.sc.DB.Get_M_accessoires().keys()
		liste = [i for i in map(self.Trie,liste) if i]
		return liste

	def Trie(self,ident):
		acc_d = self.sc.DB.Get_this_M_accessires(ident)
		if self.th_part:
			part = acc_d.get('partenaire')
			if not isinstance(part,str):
				acc_d['partenaire'] = str()
				self.sc.DB.Save_M_accessoires(acc_d)
			if acc_d.get('partenaire').lower() != self.th_part.lower():
				return None
		return acc_d

# Méthode de gestion des actions
	@Cache_error
	def new_mont(self,wid):
		if self.lib:
			dic = self.sc.DB.Get_M_acess_format()
			dic['libelé'] = self.lib
			dic['partenaire'] = self.th_part
			self.sc.add_refused_error(f'Montant {self.lib} Enregistrer avec succès!')
			self.excecute(self._new_mont,dic)
			self.add_all()
		else:
			self.sc.add_refused_error('les informations ne sont pas complètes')

	def _new_mont(self,dic):
		self.sc.DB.Save_M_accessoires(dic)
		self.sc.DB.Up_this_num(self.sc.DB.montant_acces_fic)
			
	def show_det_acess(self,wid):
		self.aff_surf.access_indent = wid.info
		self.aff_surf.add_all()

	def set_lib(self,wid,val):
		self.lib = val

	def set_new_mont(self,wid):
		self.New_M_access()

	def close(self,wid):
		self.add_all()

	def set_th_part(self,info):
		self.th_part = info
		self.Up_tab()

class P_comptable(box):
	@Cache_error
	def initialisation(self):
		self.orientation = 'horizontal'
		self.padding = dp(2)
		self.spacing = dp(2)
		self.Plan_dict = self.sc.DB.Get_plan_class()

		self.cla = ""
		self.cla_list = [i for i in self.Plan_dict.keys()]
		self.typ = str()
		self.typ_list = self.sc.DB.Get_cmpt_type_list()
		self.nat_cmpt = str()
		self.nat_cmpt_list = "Crédit","Débit"
		self.size_pos()

	@Cache_error
	def Foreign_surf(self):
		self.add_part1_surf()

	def size_pos(self):
		w,h = self.part1_size = .4,1
		self.part2_size = 1-w,h

		self.part1_surf = stack(self,size_hint = self.part1_size,
			padding = dp(10),spacing = dp(10),radius = dp(10),
			bg_color = self.sc.aff_col1)

		self.part2_surf = Show_cmpt(self,size_hint = self.part2_size,
			radius = dp(10),padding = dp(10),bg_color = self.sc.aff_col1)

		self.add_surf(self.part1_surf)
		self.add_surf(self.part2_surf)

	@Cache_error
	def add_part1_surf(self):
		h = .045
		self.part1_surf.clear_widgets()
		self.part1_surf.add_text("Comptes comptables",size_hint = (.8,h),
			text_color = self.sc.text_col1,halign = "center",underline = True)

		self.part1_surf.add_icon_but(icon = 'file-plus',size_hint = (.1,h),
			font_size = "34sp",text_color = self.sc.black,on_press = self.new_compt)

		dic = {
			"Class d'appartenance":(self.cla,self.cla_list,self.set_cla),
			"Type de compte":(self.typ,self.typ_list,self.set_typ),
			"solde normal":(self.nat_cmpt,self.nat_cmpt_list,self.set_nat_cmpt),
		}
		for k,tup in dic.items():
			self.part1_surf.add_text(k + ' :',text_color = self.sc.text_col1,
				size_hint = (.35,h))
			txt,lis,fonc = tup
			self.part1_surf.add_surf(liste_set(self,txt,lis,size_hint = (.6,h),
				mother_fonc = fonc,mult = 1))
		self.Tab = Table(self,size_hint = (1,.75),bg_color = self.sc.aff_col3,
			padding = dp(10),radius = dp(10),exec_key = 'N°',exec_fonc = self.shw_cmpt)
		self.part1_surf.add_surf(self.Tab)
		self.Up_tab()

	@Cache_error
	def Up_tab(self):
		entete = 'Numéro de compte',"class","intitulé","nature comptable","solde"
		wid_l = [round(1/len(entete),2)]*len(entete)
		liste = self.Trie_compt()
		self.Tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.087))

	def Trie_compt(self):
		all_compt = self.sc.DB.Get_all_compts()
		liste = [i for i in map(self.Trie_cmp,all_compt.values()) if i]
		return liste


	def Trie_cmp(self,cmpt):
		if self.cla:
			if cmpt.get("class").lower() != self.cla.lower():
				return None
		if self.typ:
			if cmpt.get("type").lower() != self.typ.lower():
				return None
		if self.nat_cmpt:
			if cmpt.get("solde normal").lower() != self.nat_cmpt.lower():
				return None
		cmpt['Numéro de compte'] = int(cmpt.get('N°',1))
		return cmpt

# Gestion des actions des bouttons
	@Cache_error
	def new_compt(self,wid):
		self.part1_surf.clear_widgets()
		self.part1_surf.add_surf(New_cmpt(self))

	def set_nat_cmpt(self,info):
		self.nat_cmpt = info
		self.Up_tab()

	def set_typ(self,info):
		self.typ = info
		self.Up_tab()

	def set_cla(self,info):
		self.cla = info
		self.Up_tab()

	def shw_cmpt(self,wid):
		info = wid.info
		self.part2_surf.cmpt_num = info
		self.part2_surf.add_all()

class New_cmpt(stack):
	@Cache_error
	def initialisation(self):
		h = .045
		self.padding = dp(10)
		self.spacing = dp(10)
		self.new_compt = self.sc.DB.Get_compt_info()
		self.num = str()
		self.intitule = str()
		self.nat_cmpt = str()
		self.solde = float()
		self.nat_liste = 'passif','actif',"produit"
		self.typ = str()

		self.sold_n_list = 'Crédit',"Débit"
		self.sold_n = str()
		self.typ_list = self.sc.DB.Get_cmpt_type_list()
		self.etat_fi = str()
		self.etat_fi_list = "bilan",'compte de résultat',"aucun"

		self.partie_de_gest = str()
		self.partie_list = self.sc.DB.Get_partie_affect_list()

		self.add_text("Nouveau compte comptable",size_hint = (.8,h),
			text_color = self.sc.text_col1,underline = True,halign = "center")
		self.add_icon_but(icon = "close",text_color = self.sc.red,
			font_size = '34sp',size_hint = (.2,h),on_press = self.close_th)

		self.add_text_input("Numéro de compte :",(.3,h),(.6,h),self.sc.text_col1,
			text_color = self.sc.text_col1, bg_color = self.sc.aff_col3,
			on_text = self.set_num)

		self.class_surf = stack(self,size_hint = (1,h*2),spacing = dp(10))
		self.add_surf(self.class_surf)
		self.up_cals_surf()
		self.add_text_input("Intitulé :",(.3,h),(.6,h),self.sc.text_col1,
			text_color = self.sc.text_col1, bg_color = self.sc.aff_col3,
			on_text = self.set_int)
		self.add_text_input("Solde actuel :",(.3,h),(.6,h),self.sc.text_col1,
			text_color = self.sc.text_col1, bg_color = self.sc.aff_col3,
			on_text = self.set_solde,default_text = str(self.solde))
		th_d = {
			"Nature comptable":(self.nat_cmpt,self.nat_liste,self.set_nat_cmpt),
			"Solde normal":(self.sold_n,self.sold_n_list,self.set_sold_n),
			"Etat financier":(self.etat_fi,self.etat_fi_list,self.set_etat_fi),
			"Partie affectée":(self.partie_de_gest,self.partie_list,self.set_partie_de_gest)
		}
		for info,tup in th_d.items():
			txt,lis,fonc = tup
			self.add_text(info,text_color = self.sc.text_col1,
				size_hint = (.3,h))
			self.add_surf(liste_set(self,txt,lis,size_hint = (.6,h),
				mult = 1, mother_fonc = fonc))

		self.add_text_input("Type de compte",(.3,h),(.6,h),self.sc.text_col1,
			text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
			default_text = self.typ,on_text = self.set_typ)
		self.add_icon_but(icon = 'plus',size_hint = (.1,h),font_size = "34sp",
			text_color = self.sc.black,on_press = self.save_typ)
		self.typ_lis_surf = stack(self,size_hint = (1,.2),spacing = dp(10))
		self.add_surf(self.typ_lis_surf)
		self.up_typ_list()

		self.add_button_custom('Nouveau compte',self.add_new_comp,
			text_color = self.sc.text_col1,bg_color = self.sc.green,
			size_hint = (.4,h),padd = (.3,h))

	@Cache_error
	def up_typ_list(self):
		self.typ_lis_surf.clear_widgets()
		liste = [i for i in self.typ_list if self.typ.lower() in i.lower()]
		self.typ_lis_surf.add_surf(liste_set(self,self.typ,liste,"V",
			mother_fonc = self.def_typ,mult = 1,size_hint = (1,1)))

	@Cache_error
	def up_cals_surf(self):
		self.class_surf.clear_widgets()
		if self.num:
			clas = self.num[0]
			cat = self.sc.DB.Get_plan_class().get(clas)
			d = {
				"Classe comptable :":clas,
				"Catégorie :":cat
			}
			for k,v in d.items():
				self.class_surf.add_text_input(k,(.3,.5),(.6,.5),self.sc.text_col1,
					text_color = self.sc.text_col1,bg_color = self.sc.aff_col1,
					readonly = True, default_text = v)

# Gestion des actions des boutons
	@Cache_error
	def add_new_comp(self,wid):
		if self.num and self.intitule and self.nat_cmpt and self.typ:
			self.new_compt["N°"] = self.num
			clas = self.num[0]
			cat = self.sc.DB.Get_plan_class().get(clas)
			self.new_compt['class'] = clas
			self.new_compt['catégorie'] = cat
			self.new_compt['intitulé'] = self.intitule
			self.new_compt['type'] = self.typ
			self.new_compt['nature comptable'] = self.nat_cmpt
			self.new_compt['solde normal'] = self.sold_n
			self.new_compt['état financier'] = self.etat_fi
			self.new_compt['partie affectée'] = self.partie_de_gest
			self.new_compt['solde'] = self.solde

			#self.sc.DB.Save_compte(self.new_compt)
			self.excecute(self.sc.DB.Save_compte,self.new_compt)
		else:
			self.sc.add_refused_error("Imformations incomplètes")

	def close_th(self,wid):
		self.mother.add_part1_surf()

	def set_num(self,wid,val):
		wid.text = self.regul_input(wid.text)
		self.num = wid.text

		self.up_cals_surf()

	def set_solde(self,wid,val):
		wid.text = self.regul_input(wid.text)
		if wid_text:
			self.solde = float(wid.text)
		else:
			self.solde = float()

	def def_typ(self,info):
		self.typ = info

	def set_int(self,wid,val):
		self.intitule = val

	def set_nat_cmpt(self,info):
		self.nat_cmpt = info

	def set_etat_fi(self,info):
		self.etat_fi = info

	def set_partie_de_gest(self,info):
		self.partie_de_gest = info

	def set_sold_n(self,info):
		self.sold_n = info

	def set_typ(self,wid,val):
		self.typ = val
		self.up_typ_list()

	def save_typ(self,wid):
		self.excecute(self.sc.DB.Save_cmpt_type_list,self.typ)
		#self.sc.DB.Save_cmpt_type_list(self.typ)
		self.up_typ_list()

class Show_cmpt(box):
	@Cache_error
	def initialisation(self):
		self.cmpt_num = str()

		self.nat_liste = 'passif','actif',"produit"
		self.typ = str()

		self.sold_n_list = 'Crédit',"Débit"
		self.sold_n = str()
		self.typ_list = self.sc.DB.Get_cmpt_type_list()
		self.etat_fi = str()
		self.etat_fi_list = "bilan",'compte de résultat',"aucun"

		self.size_pos()
	
	def size_pos(self):
		self.part_info = stack(self,size_hint = (1,.4),
			spacing = dp(10))
		self.part_ecrit = stack(self,size_hint = (1,.6),
			spacing = dp(10))

		self.add_surf(self.part_info)
		self.add_surf(self.part_ecrit)

	@Cache_error
	def Foreign_surf(self):
		self.add_part_info()
		self.add_part_ecrit()

	@Cache_error
	def add_part_info(self):
		h = .1
		self.part_info.clear_widgets()
		if self.cmpt_num:
			self.cmpt_infos = self.sc.DB.Get_this_compt_infos(self.cmpt_num)
			dic_stact = {
				"Class comptable":self.cmpt_infos.get('class'),
				"Numéro de compte":self.cmpt_infos.get('N°'),
				"Catégorie":self.cmpt_infos.get('catégorie'),
			}
			for k,v in dic_stact.items():
				self.part_info.add_text_input(k,(.15,h),(.18,h),self.sc.text_col1,
					text_color = self.sc.orange,bg_color = self.sc.aff_col1,
					readonly = True,default_text = str(v),font_size = "20sp")
			H = .94-h
			partDef = stack(self,size_hint = (.66,H),spacing = dp(10))
			self.part_typ = stack(self,size_hint = (.33,H))
			self.part_info.add_surf(partDef)
			th_h = .14
			partDef.add_text_input('Intitulé de compte',(.35,th_h),(.6,th_h),
				self.sc.text_col1,text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,on_text = self.set_intitul,
				default_text = self.cmpt_infos.get('intitulé'))
			th_d = {
				"Nature comptable":(self.cmpt_infos.get('nature comptable'),
					self.nat_liste,self.set_nat_cmpt),
				"Solde normal":(self.cmpt_infos.get('solde normal'),
					self.sold_n_list,self.set_sold_n),
				"Etat financier":(self.cmpt_infos.get('état financier'),
					self.etat_fi_list,self.set_etat_fi),
				}
			for info,tup in th_d.items():
				txt,lis,fonc = tup
				partDef.add_text(info,text_color = self.sc.text_col1,
					size_hint = (.35,th_h))
				partDef.add_surf(liste_set(self,txt,lis,size_hint = (.6,th_h),
					mult = 1,mother_fonc = fonc))

	@Cache_error
	def add_part_ecrit(self):
		h = .1
		self.part_ecrit.clear_widgets()
		self.part_typ = stack(self,size_hint = (.5,.9))
		self.part_gest = stack(self,size_hint = (.5,.9))
		self.part_ecrit.add_surf(self.part_typ)
		self.part_ecrit.add_surf(self.part_gest)

		self.part_typ.add_text('Type de compte :',text_color = self.sc.text_col1,
			size_hint = (.3,h))
		self.part_typ.add_surf(input_search_lay_new(self,
			self.cmpt_infos.get('type'),self.sc.DB.Get_cmpt_type_list(),
			self.set_typ,size_hint = (.65,1),mult = 7,sub_mod = 1,
			text_size = (.35,1),inp_size = (1,.08)))

		self.part_gest.add_text('Partie de gestion :',text_color = self.sc.text_col1,
			size_hint = (.3,h))
		self.part_gest.add_surf(input_search_lay_new(self,
			self.cmpt_infos.get('partie affectée'),self.sc.DB.Get_partie_affect_list(),
			self.set_partie_de_gest,size_hint = (.65,1),mult = 7,sub_mod = 1,
			text_size = (.35,1),inp_size = (1,.08)))

		

		if self.cmpt_infos.get("éditable"):
			self.part_ecrit.add_button_custom('Modifier',self.set_modif_cmp,
				size_hint = (.2,.08),padd = (.2,.08))
			if float(self.cmpt_infos.get('solde')) == 0.0:
				self.part_ecrit.add_button_custom('Supprimer',self.set_supp_cmp,
					size_hint = (.2,.08),	padd = (.2,.08),
					bg_color = self.sc.red)

# Gestion des actions des bouttons
	@Cache_error
	def set_modif_cmp(self,wid):
		self.excecute(self.sc.DB.Update_this_cmpt,self.cmpt_infos)
		#self.sc.DB.Update_this_cmpt(self.cmpt_infos)
		self.add_all()

	def set_supp_cmp(self,wid):
		self.excecute(self.sc.DB.Supp_this_cmpt,self.cmpt_infos)
		#self.sc.DB.Supp_this_cmpt(self.cmpt_infos)
		self.add_all()

	def set_typ(self,info):
		self.cmpt_infos['type'] = info

	def set_intitul(self,wid,val):
		if val:
			self.cmpt_infos['intitulé'] = val

	def set_nat_cmpt(self,info):
		if info:
			self.cmpt_infos['nature comptable'] = info

	def set_etat_fi(self,info):
		if info:
			self.cmpt_infos['état financier'] = info

	def set_partie_de_gest(self,info):
		if info:
			self.cmpt_infos['partie affectée'] = info

	def set_sold_n(self,info):
		if info:
			self.cmpt_infos['solde normal'] = info

class show_M_access(box):
	def initialisation(self):
		self.access_indent = str()

	@Cache_error
	def Foreign_surf(self):
		self.size_pos()
		if self.access_indent:
			self.acc_info = self.sc.DB.Get_this_M_accessires(self.access_indent)
			self.add_info_part()
			self.det_part.access_indent = self.access_indent
			self.det_part.add_all()

	@Cache_error
	def size_pos(self):
		self.clear_widgets()
		w,h = inf_s = (1,.3)
		det_s = w,1-h

		self.info_part = stack(self,size_hint = inf_s,padding = dp(10),
			spacing = dp(10))

		self.det_part = show_M_access_det(self,size_hint = det_s)

		self.add_surf(self.info_part)
		self.add_surf(self.det_part)

	@Cache_error
	def add_info_part(self):
		h = .2
		self.info_part.clear_widgets()
		info_d = {
			"Numéro de référence":self.acc_info.get('N°'),
			"Date d'enregistrement":self.acc_info.get("date d'enregistrement"),
			"Solde actuel":self.format_val(self.acc_info.get('solde actuel')),
		}
		for k,v in info_d.items():
			self.info_part.add_text(k,size_hint = (.17,h),
				text_color = self.sc.text_col1,
				valign = 'top')
			self.info_part.add_text(self.format_val(v),size_hint = (.16,h),
				text_color = self.sc.green,font_size = "18sp",
				valign = 'top')
			
		inf_p = stack(self,size_hint = (.5,.8),spacing = dp(10))
		self.info_part.add_surf(inf_p)
		self.info_part.add_text('Partenaire :',size_hint = (.16,h),
			text_color = self.sc.text_col1,padding_right = dp(10),
			halign = 'right',valign = 'top')
		self.info_part.add_surf(input_search_lay_new(self,self.acc_info.get('partenaire'),
			self.mother.part_lise,self.set_part,
			size_hint = (.33,.8)))
		d = {
			"Décaissements total":self.format_val(self.acc_info.get("décaissement")),
			"Solde total":self.format_val(self.acc_info.get('solde total')),
			"libelé":self.acc_info.get('libelé')
		}
		for k,v in d.items():
			txt_col1 = self.sc.black
			txt_col2 = self.sc.green
			fon_s = "18sp"
			read = True
			bg_col = self.sc.aff_col1
			if k == "libelé":
				txt_col1 = self.sc.text_col1
				txt_col2 = self.sc.text_col1
				fon_s = "17sp"
				read = False
				bg_col = self.sc.aff_col3
			inf_p.add_text_input(k,(.4,.22),(.6,.22),txt_col1,
				text_color = txt_col2,bg_color = bg_col,default_text = v,
				font_size = fon_s,readonly = read,on_text = self.set_name)
		if "écritures" in self.sc.DB.Get_access_of('Montants accessoires'):
			inf_p.add_button_custom("Modifier",self.modif_mont_acc,size_hint = (.4,.22),
				padd = (.3,.22),bg_color = self.sc.orange,text_color = self.sc.text_col1,)

# Gestion des actions des bouttons
	def set_part(self,info):
		self.acc_info['partenaire'] = info

	def set_name(self,wid,val):
		if val:
			self.acc_info['libelé'] = val

	def modif_mont_acc(self,wid):
		self.excecute(self.sc.DB.Save_M_accessoires,self.acc_info)
		#self.sc.DB.Save_M_accessoires(self.acc_info)
		self.sc.add_refused_error('Informations prise en compte')

class show_M_access_det(stack):
	def initialisation(self):
		pass

	@Cache_error
	def Foreign_surf(self):
		self.spacing = dp(5)
		h = .07
		self.add_text('Historiques des actions',text_color = self.sc.text_col1,
			size_hint = (.9,h),halign = "center",underline = True)
		self.add_icon_but(icon = 'printer',size_hint = (.1,h),
			text_color = self.sc.black,on_press = self.Impression)
		self.add_surf(Periode_set(self,size_hint = (.5,h),exc_fonc = self.Up_tab))
		self.tab = Table(self,size_hint = (1,.78),padding = dp(10),
			exec_key = "date",exec_fonc = self.show_act,radius = dp(10))
		self.add_surf(self.tab)
		self.Up_tab()

	@Cache_error
	def Up_tab(self):
		entete = 'date','solde de départ','débit','crédit','solde final'
		wid_l = .2,.2,.2,.2,.2
		date_l = self.get_date_list(self.day1,self.day2)
		hist_sets = self.mother.acc_info.get('historique général')
		liste = [dic for i,dic in hist_sets.items() if i in date_l]
		self.tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.08))

	@Cache_error
	def Set_all_infos(self,date):
		self.clear_widgets()
		h = .1
		self.add_text(f'Historiques des actions du {date}',
			text_color = self.sc.text_col1,
			size_hint = (.9,h),halign = "center",underline = True)
		self.add_icon_but(icon = 'close',size_hint = (.05,h),
			text_color = self.sc.red,on_press = self.close)
		self.add_icon_but(icon = 'printer',size_hint = (.05,h),
			text_color = self.sc.black,on_press = self.Impression_sec)
		self.tab = Table(self,size_hint = (1,.9),padding = dp(10),
			radius = dp(10))
		self.TH_DATE = date
		hist_det = self.mother.acc_info.get('historique détailé').get(date)
		entete = 'date',"libelé","montant","référence","crédit","débit","forme d'action"
		wid_l = [.143]*7
		liste = [i for i in hist_det.values()]
		self.tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.11))
		self.add_surf(self.tab)

# Gestion des actions au niveau des bouttons
	@Cache_error
	def Impression(self,wid):
		obj = self.sc.imp_part_dic('Résumé')(self)
		date_l = self.get_date_list(self.day1,self.day2)
		hist_sets = self.mother.acc_info.get('historique général')
		liste = [dic for i,dic in hist_sets.items() if i in date_l]
		entete = ['date','solde de départ','débit','crédit','solde final']
		wid_l = .24,.19,.19,.19,.19
		titre = f"Historiques financiers du {self.mother.acc_info.get('libelé')}"
		info = f'Période : du {self.day1} au {self.day2}<br/>'
		info += 'Agence TOKPOTA1'
		obj.Create_fact(wid_l,entete,liste,titre,info)

	def Impression_sec(self,wid):
		obj = self.sc.imp_part_dic('Résumé')(self)
		hist_det = self.mother.acc_info.get('historique détailé').get(self.TH_DATE)
		liste = [i for i in hist_det.values()]
		entete = ['date',"libelé","montant","référence","crédit",
			"débit","forme d'action"]
		wid_l = [.203,.133,.133,.133,.133,.133,.133,]
		titre = f"Historiques du {self.TH_DATE} de {self.mother.acc_info.get('nom')}"
		info = 'Agence TOKPOTA1'
		obj.Create_fact(wid_l,entete,liste,titre,info)

	def show_act(self,wid):
		date = wid.info
		self.Set_all_infos(date)

	def close(self,wid):
		self.add_all()

class P_finan(stack):
	@Cache_error
	def initialisation(self):
		self.padding = dp(10)
		self.spacing = dp(10)
		h = .045
		self.add_text("Le point financier traditionnel",size_hint = (.9,h),
			text_color = self.sc.text_col1, halign = 'center',underline = True)
		self.add_icon_but(icon = 'printer',size_hint = (.1,h),text_color = self.sc.black,
			on_press = self.Print_info)
		self.add_text(f'Solde Financier général : {self.format_val(self.sc.DB.Get_solde_financier())}',
			text_color = self.sc.green,size_hint = (.35,h),font_size = "20sp")
		self.add_surf(Periode_set(self,size_hint = (.3,h),exc_fonc = self.Up_tab))
		
		self.tab = Table(self,size_hint = (1,.83),padding = dp(10),
			radius = dp(10),bg_color = self.sc.aff_col3)
		self.add_surf(self.tab)
		self.result_part = box(self,size_hint = (1,.05),padding = dp(1),
			spacing = dp(1),bg_color = self.sc.black,orientation = "horizontal")
		self.add_surf(self.result_part)
		self.Up_tab()

	@Cache_error
	def Up_tab(self):
		entete = ("date","Entrées",'Sorties',"A déversé","Déversé","Résultat")
		wid_l = [round(1/len(entete),3)]*len(entete)
		liste = self.Trie_list()
		self.tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.07),
			force_tire = False)

	def Trie_list(self):
		self.entre_t = float()
		self.sortie_t = float()
		self.a_derse_t = float()
		self.devers = float()
		self.resulta = float()

		date_liste = self.get_date_list(self.day1,self.day2)
		liste = [i for i in map(self.trie_b,date_liste) if i]
		liste = self.Sort_infos(liste,"date",True)
		self.Up_result_part()
		return liste

	@Cache_error
	def Up_result_part(self):
		self.result_part.clear_widgets()
		liste = ["Résumé total",self.entre_t,self.sortie_t,self.a_derse_t,
			self.devers,self.resulta]
		for txt in liste:
			self.result_part.add_text(self.format_val(txt),text_color = self.sc.black,
				bg_color = self.sc.aff_col1,halign = 'center')

	def trie_b(self,date):
		point = self.sc.DB.Get_to_day_point(date)
		self.entre_t+=point.get('Entrées')
		self.sortie_t+=point.get('Sorties')
		self.a_derse_t+=point.get('A déversé')
		self.devers+=point.get('Déversé')
		self.resulta+=point.get('Résultat')
		return point

# Gestion des actions des bouttons
	@Cache_error
	def Print_info(self,wid):
		obj = self.sc.imp_part_dic('Fiche')(self)
		date_l = self.get_date_list(self.day1,self.day2)
		liste = self.Trie_list()
		entete = "date","Entrées",'Sorties',"A déversé","Déversé","Résultat"
		wid_l = .21,.16,.16,.16,.16,.15
		titre = f"Historiques des points financier"
		info = f'Période : du {self.day1} au {self.day2}<br/>'
		info += 'Agence TOKPOTA1'
		total_ent = "Entrées",'Sorties',"A déversé","Déversé","Résultat"
		obj.Create_fact(wid_l,entete,liste,titre,info,total_ent)

class N_devers(box):
	def __init__(self,mother,**kwargs):
		kwargs['bg_color'] = mother.sc.aff_col2
		box.__init__(self,mother,**kwargs)

	@Cache_error
	def initialisation(self):
		self.clear_widgets()
		self.spacing = dp(10)
		self.add_text("Surface de déversement comptable",
			text_color = self.sc.text_col3,halign = 'center',
			size_hint = (1,.2),valign = 'bottom',font_size = '20sp',
			underline = True)
		self.obj = th_dever_surf(self,.1,"Déversement",int(),
			size_hint = (.6,.45),pos_hint = (.2,1),radius = dp(10),
			padding = dp(10),spacing = dp(10),bg_color = self.sc.aff_col1)
		self.add_surf(self.obj)
		self.add_text("",
			text_color = self.sc.text_col1,halign = 'center',
			size_hint = (1,.3),valign = 'bottom')

class th_dever_surf(paiem_surf):
	montant = float()

	@Cache_error
	def add_Tress_part(self):
		h = dp(40)
		self.montant = float()
		self.Compte_surf.clear_widgets()
		self.Get_compt_info()
		H = (h+dp(5))*len(self.Paie_cmt_dict)
		st = stack(self,size_hint = (1,None),height = H,
			spacing = dp(10))
		self.Compte_surf.add_surf(st)
		for info,ident in self.Paie_cmt_dict.items():
			cmpt_info = self.sc.DB.Get_this_compte(ident)
			mont_comt = float(cmpt_info.get('solde actuel'))
			self.montant += mont_comt
			read = True
			txt_col = self.sc.text_col1
			bg_col = self.sc.aff_col3
			if info in self.this_pai_list:
				read = False
				txt_col = self.sc.green
				bg_col = self.sc.green
			b = box(self,size_hint = (1,None),spacing = dp(10),
				height = h,bg_color = self.sc.aff_col1,
				radius = dp(10),orientation = "horizontal")
			b.add_button('',size_hint = (None,None),width = dp(20),
				height = dp(20),on_press = self.set_cmpt,info = info,
				bg_color = bg_col,pos_hint = (0,.25))
			b.add_button(info,size_hint = (.45,1),on_press = self.set_cmpt,
				info = info,bg_color = self.sc.aff_col1,
				halign = "left",text_color = txt_col)
			b.add_input(info,default_text = str(self.montant_dic.get(info,mont_comt)),
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				padding_left = dp(10),readonly = read,on_text = self.set_mont_dic,
				placeholder = "Montant",size_hint = (.2,1))
			b.add_input(info,default_text = str(self.reference_dic.get(info,str())),
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				padding_left = dp(10),readonly = read,on_text = self.set_ref_dic,
				placeholder = "Recevant/Référence",size_hint = (.25,1))
			st.add_surf(b)

	@Cache_error
	def add_montant_part(self):
		h = .1
		self.montant_part.clear_widgets()
		b = box(self,size_hint = (1,h*2.5),padding = dp(10),
			radius = dp(10),bg_color = self.sc.aff_col1)
		b.add_text_input("Montant des comptes confondus",(1,.45),(1,.55),
			self.sc.text_col1, bg_color = self.sc.aff_col3,
			text_color = self.sc.text_col1,
			default_text = self.format_val(self.montant),
			readonly = True,text_halign = 'center',
			halign = "center")
		self.montant_part.add_surf(b)
		b1 = box(self,size_hint = (1,h*2.5),padding = dp(10),
			radius = dp(10),bg_color = self.sc.aff_col1)
		b1.add_text('Montant déversé',size_hint = (1,.45),
			text_color = self.sc.text_col1,halign = 'center')
		self.mont_paye = b1.add_text(str(),size_hint = (1,.55),
			text_color = self.sc.text_col1,halign = 'center')
		self.montant_part.add_surf(b1)

		b2 = box(self,size_hint = (1,h*2.5),padding = dp(10),
			radius = dp(10),bg_color = self.sc.aff_col1)
		b2.add_text('Montant restant',size_hint = (1,.45),
			text_color = self.sc.text_col1,halign = 'center')
		self.mont_rest = b2.add_text(str(),size_hint = (1,.55),
			text_color = self.sc.text_col1,halign = 'center')
		self.montant_part.add_surf(b2)

# Gestion des actions
	def valide_paie(self,montant,cmp_ident):
		cmpt_dic = self.sc.DB.Get_this_compte(cmp_ident)
		if not montant:
			montant = cmpt_dic.get("solde actuel")
		return self.Save_ecriture(cmpt_dic,float(montant))

	def Save_ecriture(self,cmpt_dic,montant):
		decaiss_for = self.sc.DB.Get_decaissement_form()
		decaiss_for["bénéficiaire"] = "Comptabilité général"
		decaiss_for["type de bénéficiaires"] = 'Interne'
		decaiss_for["compte bénéficiaires"] = "Interne"
		decaiss_for["compte de sortie"] = cmpt_dic.get('institutions')+f"(_){cmpt_dic.get('N° de compte')}"
		decaiss_for["motif de décaissement"] = "Déversement de fin de journée"
		decaiss_for["référence"] = self.reference
		decaiss_for["montant décaissé"] = montant
		decaiss_for["mode de sortie"] = cmpt_dic.get('type de compte')
		decaiss_for["mode de reception"] = cmpt_dic.get('type de compte')
		decaiss_for["id de la transaction"] = "Bureau"
		return decaiss_for
	
	def save_paie(self,wid):
		Conf_s = Confirmation(self,bg_color = self.sc.aff_col1)
		Conf_s.add_all(self.th_add_paie)
		self.add_modal_surf(Conf_s,size_hint = (.3,.3))
	
	@Cache_error
	def th_add_paie(self):
		refs = list()
		decaiss_dict = dict()
		for info in self.this_pai_list:
			cmp_ident = self.Paie_cmt_dict.get(info)
			if cmp_ident:
				mont = self.montant_dic.get(info)
				if not mont:
					mont = 0
				mont = float(mont)

				ref_dep = self.reference_dic.get(info)
				if not ref_dep:
					ref_dep = '/'
				liste = ref_dep.split("/")
				if liste:
					self.deposant = liste[0]
					self.reference = liste[-1]
				else:
					self.deposant,self.reference = 0,0

				#if mont < 0:
				#	self.sc.add_refused_error("Impossible d'enrégistrer un déversement négatif")
				#	return
				ret = self.valide_paie(mont,cmp_ident)
				ident = ret.get("N°")
				decaiss_dict[ident] = ret
				refs.append(ident)
		
		if self.Add_deversement(refs):
			for dic in decaiss_dict.values():
				print(dic)
				self.sc.DB.Save_decaissement(dic,False)
				#self.excecute(self.sc.DB.Save_decaissement,dic,False)
		#self.add_all()

	@Cache_error
	def Add_deversement(self,refs):
		dev_dict = self.sc.DB.deversement_format()
		dev_dict['référence'] = refs
		th_mont = float()
		for mont in self.montant_dic.values():
			th_mont += mont
		dev_dict['montant'] = th_mont
		dev_dict['déposant'] = self.sc.get_curent_perso()
		dev_dict['compte sortant'] = self.this_pai_list
		dev_dict['motif'] = f"Déversement du {self.sc.get_today()}"
		ret = self.sc.DB.Save_deversements(dev_dict)
		if ret ==True:
			self.sc.add_refused_error('Déversement sauvegardé avec succès!')
			self.excecute(self.sc.DB.Save_local_backup,self.sc.get_today())
			self.initialisation()
			return True
		else:
			self.sc.add_refused_error(ret)
#abs
class Mouv_F(stack):
	def __init__(self,mother,**kwargs):
		kwargs['bg_color'] = mother.sc.aff_col3
		stack.__init__(self,mother,**kwargs)

	def initialisation(self):
		self.add_all()

	@Cache_error
	def Foreign_surf(self):
		self.clear_widgets()
		self.padding = dp(10)
		self.spacing = dp(10)
		self.typ_mouv = str()
		self.add_padd((1,.18))
		self.add_padd((.3,.05))
		self.add_text("Type de Mouvement",text_color = self.sc.text_col3,
			size_hint = (.12,.05),)
		self.add_surf(liste_set(self,self.typ_mouv,("Dépot de fond",
			"Décaissements"),mother_fonc = self.set_mouv_info,
			size_hint = (.1,.05),mult = 2))
		self.add_padd((.3,.05))
		self.add_padd((.2,.4))
		self.cont_surf = stack(self,size_hint = (.6,.5),
			spacing = dp(10),bg_color = self.sc.aff_col1,
			radius = dp(10),padding = dp(10))
		self.add_surf(self.cont_surf)
		self.add_cont_surf()

	def add_cont_surf(self):
		h = .1
		self.cont_surf.clear_widgets()
		if self.typ_mouv == "Dépot de fond":
			self.typ_m = "débit"
		elif self.typ_mouv == "Décaissements":
			self.typ_m = "crédit"
		if self.typ_mouv:
			self.info_dic = {
				"montant":float(),
				"référence":str(),
			}
			d = {
				"date":self.sc.get_today(),
				"heure":self.sc.get_hour(),
				"type d'opérations":self.typ_m,
			}
			for k,v in d.items():
				self.cont_surf.add_padd((.25,h))
				self.cont_surf.add_text_input(k,(.2,h),(.3,h),
					self.sc.text_col1,text_color = self.sc.text_col1,
					bg_color = self.sc.aff_col1,readonly = True,default_text = v)
				self.cont_surf.add_padd((.25,h))
			for k,v in self.info_dic.items():
				self.cont_surf.add_padd((.25,h))
				self.cont_surf.add_text_input(k,(.2,h),(.25,h),
					self.sc.text_col1,text_color = self.sc.text_col1,
					bg_color = self.sc.aff_col3,placeholder = k,
					default_text = str(v),on_text = self.set_info)
				self.cont_surf.add_padd((.25,h))

			self.cont_surf.add_button_custom('Valider',self.save_fin_mouv,
				text_color = self.sc.text_col1,bg_color = self.sc.orange,
				size_hint = (.5,h),padd = (.25,h))

# Gestion des actions des bouttons
	@Cache_error
	def save_fin_mouv(self,wid):
		if self.check(self.info_dic):
			Conf_s = Confirmation(self,bg_color = self.sc.aff_col1)
			Conf_s.add_all(self.th_save_fin_mouv)
			self.add_modal_surf(Conf_s,size_hint = (.3,.3))
		else:
			self.sc.add_refused_error('Les informations demandés sont obligatoire !!!')

	def th_save_fin_mouv(self):
		montant = float(self.info_dic.get('montant'))
		ref = self.info_dic.get('référence')
		motif = self.typ_mouv
		hist = self.sc.DB.hist_finance_f()
		hist[self.typ_m] = montant
		hist['référence'] = ref
		hist["motif"] = motif
		hist['solde précédent'] = self.sc.DB.Get_solde_financier()
		if self.typ_m == "crédit":
			montant = -montant
		hist['solde final'] = hist['solde précédent'] + montant
		self.excecute(self._save_fin,hist,montant)
		self.sc.add_refused_error('Mouvement prise en compte avec succès !!!')
		self.add_all()

	def _save_fin(self,hist,montant):
		self.sc.DB.Save_histo_finance(hist)
		self.sc.DB.Save_solde_financier(montant)

	def set_info(self,wid,info):
		if wid.info == "montant":
			wid.text = self.regul_input(wid.text)
		self.info_dic[wid.info] = wid.text

	def set_mouv_info(self,info):
		self.typ_mouv = info
		self.add_cont_surf()

class Histo_Gene(stack):
	def initialisation(self):
		self.add_all()

	@Cache_error
	def Foreign_surf(self):
		self.clear_widgets()
		h = .05
		self.all_histo = self.sc.DB.Get_histo_finance()
		self.padding = dp(10)
		self.spacing = dp(10)
		self.typ_ope = str()
		self.motif = str()

		self.add_text("Historiques des Mouvements du comptes globale de l'entreprise",
			text_color = self.sc.text_col1,halign = "center",size_hint = (.9,h),
			underline = True)
		self.add_icon_but(icon = "printer",text_color = self.sc.black,
			on_press = self.Impression,size_hint = (.05,h))
		self.add_surf(Periode_set(self,info = "Période de définition",
			info_w = .3,size_hint = (.3,h),exc_fonc = self.add_tab_surf))
		dic = {
			"Type d'opérations :":(self.typ_ope,['débit','crédit'],
				self.set_typ_ope),
		}
		for k,tup in dic.items():
			self.add_text(k,text_color = self.sc.text_col1,
				size_hint = (.1,h))
			txt,lis,fonc = tup
			self.add_surf(liste_set(self,txt,lis,size_hint = (.1,h),
				mother_fonc = fonc,mult = 2))
		self.add_text_input("Motif de l'opération",(.1,h),(.2,h),
			self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,on_text = self.set_motif)

		self.tab_surf = Table(self,size_hint = (1,.885),bg_color = self.sc.aff_col3,
			padding = dp(10))
		self.add_surf(self.tab_surf)
		self.add_tab_surf()

	@Cache_error
	def add_tab_surf(self):
		entete = ["N° d'ordre","date","heure","débit","crédit",
			"solde précédent","solde final","motif","opérateur"]
		wid_l = [.05,.11,.1,.11,.11,.11,.11,.2,.1]
		liste = self.Trie_list()
		self.tab_surf.Creat_Table(wid_l,entete,liste,ent_size = (1,.05),
			ligne_h = .07)

	def Trie_list(self):
		date_liste = self.get_date_list(self.day1,self.day2)
		liste = list()
		for i in date_liste:
			liste.extend(self.Get_hist_by_date(i))
		liste = [i for i in map(self.Trie,liste) if i]
		liste.sort(key = itemgetter("Numéro"),reverse = True)
		ind = 0
		for dic in liste:
			ind += 1
			dic["N° d'ordre"] = ind
		return liste

	def Get_hist_by_date(self,date):
		dic = self.all_histo.get(date,dict())
		if not dic:
			return []
		return [j for i, j in dic.items() if j]

	def Trie(self,dic):
		if self.motif:
			if self.motif.lower() not in dic.get('motif'):
				return None
		if self.typ_ope:
			if not dic.get(self.typ_ope):
				return None
		dic['Numéro'] = int(self.Get_real_num(dic.get('N°')))
		dic['opérateur'] = dic.get("référence")
		return dic

# Gestion des actions des bouttons
	@Cache_error
	def Impression(self,wid):
		obj = self.sc.imp_part_dic('Résumé')(self)
		date_l = self.get_date_list(self.day1,self.day2)
		liste = self.Trie_list()
		entete = ["Numéro","débit","crédit","solde précédent",
			"solde final","motif","référence"]
		wid_l = [.2,.1,.1,.15,.15,.2,.1]
		titre = f"Historiques des points financier"
		info = f'Période : du {self.day1} au {self.day2}<br/>'
		info += 'Agence TOKPOTA1'
		obj.Create_fact(wid_l,entete,liste,titre,info)


	def set_typ_ope(self,info):
		self.typ_ope = info
		self.add_tab_surf()

	def set_motif(self,wid,val):
		self.motif = val
		self.add_tab_surf()
