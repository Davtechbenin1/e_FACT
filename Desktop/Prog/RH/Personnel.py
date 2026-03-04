#Coding:utf-8
from lib.davbuild import *
from General_surf import *
from .perso_surf import *
from .perso_surf3 import *

class all_General(Define_surf):
	@Cache_error
	def initialisation(self):
		self.this_access_d = self.mother.This_user.get('accès')
		if self.this_access_d == "all":
			self.access_dic = "all"
		else:
			poste = self.mother.This_user.get('poste actuel')
			self.this_access_d = self.sc.DB.Get_this_poste_access(poste)
			self.access_dic = self.this_access_d.get('Ressouses Humaines',dict())
		
		self.access_dic = self.mother.access_dic
		self.curent_menu = str()
		self.Get_menu_infos()

	def Get_menu_infos(self):
		dic = {
			"Personnels":Personnel,
			"Postes":Postes,
			"Recrutements":Recrutements,
			"Salaires":Salaires,
		}
		self.menu_dict = dict()
		for i in dic:
			for i,srf in dic.items():
				if not self.curent_menu:
					self.curent_menu = i
				self.menu_dict[i] = srf(self,orientation = "horizontal")

class Personnel(box):
	def __init__(self,mother,**kwargs):
		kwargs['spacing'] = dp(2)
		kwargs['orientation'] = 'horizontal'
		kwargs['padding'] = [dp(2),dp(2),dp(2),0]
		box.__init__(self,mother,**kwargs)
		self.perso_info_dic = {
			"nom":str(),
			"prénom":str(),
			"téléphone":str(),
			"whatsapp":str(),
			"email":str(),
			"pays de résidence":str(),
			"ville de résidence":str(),
			"quartier":str(),
			"maison":str(),
			"nationalité":str(),
		}
		self.type_perso = str()
		self.perso_choose = str()
		self.poste_name = str()
		self.perso_name = str()
		self.poste = str()
		
		self.size_pos()

	@Cache_error
	def Foreign_surf(self):
		self.liste_type_perso = self.sc.Get_liste_type_perso()
		self.add_this_new_surf()
		self.add_aff_surf()

	@Cache_error
	def size_pos(self):
		w,h = self.new_size = .4,1
		self.aff_size = 1-w,1

		self.new_surf = stack(self,size_hint = self.new_size,
			bg_color = self.sc.aff_col1,radius = dp(10),
			padding = dp(5),spacing = dp(10))

		self.aff_surf = box(self,size_hint = self.aff_size,
			bg_color = self.sc.aff_col1,radius = dp(10))
		self.add_surf(self.new_surf)
		self.add_text('',size_hint = (None,1),width = dp(1),
			bg_color = self.sc.sep)
		self.add_surf(self.aff_surf)

	@Cache_error
	def add_this_new_surf(self):
		h = .04
		self.new_surf.clear_widgets()
		self.new_surf.add_text('Liste des personnels actifs',
			size_hint = (.8,h),text_color = self.sc.text_col1,
			halign = 'center',underline = True)
		self.new_surf.add_icon_but(icon = "printer",
			text_color = self.sc.black,on_press = self.Impression,
			size_hint = (.1,h))
		ret = self.sc.DB.Get_access_of('Personnels')
		if ret and "écritures" in ret:
			self.new_surf.add_icon_but(icon = "plus",
				text_color = self.sc.green,on_press = self.New_perso,
				size_hint = (.1,h))
		self.new_surf.add_text('Type :',size_hint = (.12,h),
			text_color = self.sc.text_col1)
		self.new_surf.add_surf(liste_set(self,self.type_perso,
			self.sc.DB.Get_perso_type(),size_hint = (.88,h),
			mult = 1,mother_fonc = self.choose_type))
		
		if self.type_perso:
			self.new_surf.add_text('Poste :',size_hint = (.12,h),
				text_color = self.sc.text_col1,)
			self.new_surf.add_surf(liste_set(self,self.poste_name,
				self.sc.DB.Get_poste_par_typ(self.type_perso),
				size_hint = (.8,h),mult = 1,mother_fonc = self.choose_poste))
		
		self.new_surf.add_text_input("Trie par nom :",
			(.3,h),(.6,h),self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,on_text = self.set_perso_name,
			default_text = self.perso_name,placeholder = "Le nom du personnel ici")

		self.aff_tab_surf = Table(self,size_hint = (1,.84),
			bg_color = self.sc.aff_col3,exec_fonc = self.show_this_perso,
			exec_key = 'NOM')
		self.new_surf.add_surf(self.aff_tab_surf)
		self.aff_tab()

	@Cache_error
	def aff_tab(self):
		wid_l = [.4,.2,.2,.2]
		entete = ["nom","prénom","poste actuel","téléphone"]
		liste = self.Trie_perso()
		self.aff_tab_surf.Creat_Table(wid_l,entete,liste,
			ent_size = (1,.07))

	@Cache_error
	def Trie_perso(self):
		L = [i for i in self.liste_type_perso if 
		self.type_perso.lower() in i.get('type').lower()]
		
		L = [i for i in L if self.poste_name.lower() in
		i.get('poste actuel').lower()]
		L = [i for i in L if self.perso_name.lower() in 
		i.get("NOM").lower()]
		return L

	def add_aff_surf(self):
		self.aff_surf.clear_widgets()
		if self.perso_choose:
			surf = Personal_surf(self,self.perso_choose)
			self.aff_surf.add_all = surf.add_all
			self.aff_surf.add_surf(surf)
		else:
			pass
		self.aff_surf.add_all()

	@Cache_error
	def add_new_perso(self):
		h = .04
		self.new_surf.clear_widgets()
		self.new_surf.add_text('Nouveau personnel',text_color = self.sc.text_col1,
			size_hint = (.8,h),halign = "center",underline = True)
		self.new_surf.add_icon_but(icon = 'close',text_color = self.sc.red,
			on_press = self.aff_s,size_hint = (.2,h))
		self.new_surf.add_text('Poste concerné',text_color = self.sc.text_col1,
			size_hint = (.3,h))
		input_search_new(self.new_surf,self.poste,self.sc.DB.Get_all_post_list(),
			self.def_post,size_hint = (.7,h))
		dic = {
			"nom":str(),
			"prénom":str(),
			"téléphone":str(),
			"whatsapp":str(),
			"email":str(),
			"pays de résidence":str(),
			"ville de résidence":str(),
			"quartier":str(),
			"maison":str(),
			"nationalité":str(),
		}
		self.perso_info_dic = dic
		for k,v in dic.items():
			self.new_surf.add_text_input(k,(.3,h),(.65,h),
				self.sc.text_col1,text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3, on_text = self.set_new_info,
				)
		self.new_surf.add_button_custom("Valider",self.valide_perso,
			size_hint = (.5,h), padd = (.25,h),bg_color = self.sc.orange)

# Gestion des actions des buttons
	def set_new_info(self,wid,val):
		self.perso_info_dic[wid.info] = val

	@Cache_error
	def valide_perso(self,wid):
		dic = {
			"date de prise de fonction":self.sc.get_today(),
			"durée de contrat":360
		}
		if not self.poste:
			self.sc.add_refused_error(' le poste est obligatoire !')
			return
		if not self.check(self.perso_info_dic):
			self.sc.add_refused_error('Toutes les informations sont obligatoires')
			return
		poste_dic = self.sc.DB.Get_this_poste(self.poste)
		
		perso_dic = self.sc.DB.Get_perso_save_format()
		perso_dic.update(self.perso_info_dic)
		perso_dic.update(dic)
		perso_dic['type'] = poste_dic.get('catégorie')
		perso_dic['poste actuel'] = self.poste
		perso_dic['postes occupés'] = {
		self.poste:{
			"contrat":str(),
			"durée":360,
			"date de début":self.sc.get_today(),
		}}
		self.excecute(self._valide_p,perso_dic)
		self.sc.add_refused_error('Personnel Ajouté avec succès')
		self.add_this_new_surf()

	def _valide_p(self,perso_dic):
		perso_id = self.sc.DB.Save_personnel(perso_dic)
		self.sc.DB.add_employer(self.poste,perso_id)

	def def_post(self,info):
		self.poste = info

	def aff_s(self,wid):
		self.add_this_new_surf()

	@Cache_error
	def Impression(self,wid):
		obj = self.sc.imp_part_dic('Résumé')(self)
		liste = self.Trie_perso()
		entete = ["nom","prénom",'poste actuel',"type",
		'téléphone',"whatsapp"]
		wid_l = .15,.15,.15,.15,.2,.2
		titre = f"Liste du personnel"
		info = str()
		if self.poste_name:
			info += f"Poste : {self.poste_name}<br/>"
		if self.type_perso:
			info += f"Type : {self.type_perso}<br/>"

		info += "Agence TOKPOTA1"
		obj.Create_fact(wid_l,entete,liste,titre,info)

	def New_perso(self,wid):
		self.add_new_perso()


	def set_perso_name(self,wid,val):
		self.perso_name = val
		self.aff_tab()

	def show_this_perso(self,wid):
		if wid.info == self.perso_choose:
			self.perso_choose = str()
		else:
			self.perso_choose = wid.info
		self.add_aff_surf()

	def choose_type(self,info):
		if self.type_perso:
			self.type_perso = str()
		else:
			self.type_perso = info

	def choose_poste(self,info):
		if self.poste_name:
			self.poste_name = str()
		else:
			self.poste_name = info


