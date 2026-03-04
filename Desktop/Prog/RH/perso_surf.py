#Coding:utf-8
"""
	Définition des objets surfaces à utiliser pour le compte
	de la gestion des personnels
"""
from lib.davbuild import *
from General_surf import *
from .perso_surf2 import *

class Define_surf(box):
	def __init__(self,mother,**kwargs):
		kwargs['spacing'] = 0
		kwargs["padding"] = dp(5)
		box.__init__(self,mother,**kwargs)
		self.size_pos()
	@Cache_error
	def size_pos(self):
		w,h = self.entete_size = 1,.039
		self.corps_size = w,1-h

		self.corps_color = self.sc.aff_col1

		self.entete_surf = stack(self,size_hint = self.entete_size,
			bg_color = self.sc.aff_col3,spacing = dp(5),
			padding_left = dp(10))

		self.corps_surf = box(self,size_hint = self.corps_size,
			bg_color = self.corps_color)

		self.add_surf(self.entete_surf)
		self.add_text("",size_hint= (1,None),height = dp(1),
			bg_color = self.sc.text_col1)
		self.add_surf(self.corps_surf)

	#
	def check_access(self,access):
		if self.access_liste == "all":
			return True
		else:
			if access in self.access_liste:
				return True
			else:
				return False

	@Cache_error
	def Foreign_surf(self):
		self.add_entete_surf()

	def Get_menu_infos(self):
		self.menu_dict = dict()

	@Cache_error
	def add_entete_surf(self):
		#self.sc.DB._Update_()
		self.entete_surf.clear_widgets()
		self.corps_surf.clear_widgets()
		for menu,surf in self.menu_dict.items():
			txt_col = self.sc.text_col1
			bg_color = self.sc.aff_col3
			f_s = "15sp"
			if menu == self.curent_menu:
				txt_col = self.sc.green
				bg_color = self.sc.green
				surf.add_all()
				self.corps_surf.add_all = surf.add_all
				self.corps_surf.add_surf(surf)
				f_s = '17sp'
			w = len(menu)*dp(10)
			if w < dp(100):
				w = dp(100)

			b = box(self,size_hint = (None,1),width = w + dp(30),
				orientation = "horizontal",spacing = dp(3))
			b.add_button('',size_hint = (None,None),
				bg_color = bg_color,width = dp(20),height = dp(20),
				on_press = self.change_part,pos_hint = (0,.2),
				info = menu)
			b.add_button(menu,text_color = txt_col,on_press = self.change_part,
				bg_color = None,halign = 'left',font_size = f_s)
			self.entete_surf.add_surf(b)

# Définition des actions au niveau des bouttons
	@Cache_error
	def change_part(self,wid):
		info = wid.info
		ret = self.sc.DB.Get_access_of(info)
		if ret:
			if self.curent_menu == wid.info:
				self.corps_surf.add_all()
			else:
				self.curent_menu = wid.info
				self.add_entete_surf()
		elif ret == False:
			self.sc.add_refused_error('Accès refusé !')

class Postes(box):
	@Cache_error
	def initialisation(self):
		if self.mother.access_dic == "all":
			self.access_liste = "all"
		else:
			self.access_liste = self.mother.access_dic.get('Postes')
		
		self.size_pos()
		self.poste_name = str()
		self.new_poste = False
		self.this_cate = str()
		self.this_hierachi = str()
		self.tab_liste = Table(self,size_hint = (1,.85),
			bg_color = self.sc.aff_col3,radius = dp(10),
			padding = dp(10),exec_fonc = self.developpe,
			exec_key = 'nom')

		self.New_dict = {
			"Nom":str(),
			"Salaire":float(),
			"Fonction":str(),
		}
		self.outils_sets = list()
		self.taches = ""
		self.Profile = ''

	def check_access(self,access):
		if self.access_liste == "all":
			return True
		else:
			if access in self.access_liste:
				return True
			else:
				return False

	@Cache_error
	def size_pos(self):
		w,h = self.new_size = .4,1
		self.corps_size = 1-w,h

		self.this_new_surf = stack(self,size_hint = self.new_size,
			spacing = dp(5),padding = dp(10))

		self.corps_surf = box(self,size_hint = self.corps_size,
			spacing = dp(5),padding = dp(10))
		self.add_surf(self.this_new_surf)
		self.add_text('',size_hint = (None,1),width=dp(1),
			bg_color = self.sc.sep)
		self.add_surf(self.corps_surf)

	@Cache_error
	def Foreign_surf(self):
		self.corps_surf.clear_widgets()
		if self.new_poste:
			self.add_new_poste()
		else:
			self.add_this_new_surf()

	@Cache_error
	def add_new_poste(self):
		h = .04
		self.New_dict['Nom'] = self.poste_name
		self.this_new_surf.clear_widgets()
		self.this_new_surf.add_text('Nouveau poste de gestion',
			text_color = self.sc.text_col1,halign = "center",
			size_hint = (.8,h),underline = True)
		self.this_new_surf.add_icon_but(icon = 'close',on_press = self.aff_poste,
			text_color = self.sc.red,size_hint = (.2,h))
		self.this_new_surf.add_text("Catégorie",
			text_color = self.sc.text_col1,size_hint = (.2,h))
		self.this_new_surf.add_surf(liste_set(self,self.this_cate,
			self.sc.DB.Get_categories(),size_hint = (.8,h),
			mult = 1,mother_fonc = self.set_cate))

		self.this_new_surf.add_text("Hiérachie",
			text_color = self.sc.text_col1,size_hint = (.2,h))
		self.this_new_surf.add_surf(liste_set(self,self.this_hierachi,
			self.sc.DB.Get_hierachie_list(),size_hint = (.8,h),
			mult = 1,mother_fonc = self.set_hierachi))
		for k,v in self.New_dict.items():
			self.this_new_surf.add_text_input(k,(.25,h),
				(.6,h),self.sc.text_col1,text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,default_text = str(v),
				on_text = self.Set_dic1,
				placeholder = k)

		liste = self.sc.DB.Get_Outils()
		self.this_new_surf.add_text('Les outils de travail requis',
			text_color = self.sc.text_col1,halign = 'center',
			size_hint = (1,h),underline = True)
		for k in liste:
			bg_col = self.sc.aff_col3
			txt_col = self.sc.text_col1
			if k in self.outils_sets:
				bg_col = self.sc.green
				txt_col = self.sc.green

			b = box(self,size_hint = (.33,h),spacing = dp(3),
				orientation = "horizontal")
			b.add_button('',size_hint = (None,None),
				height = dp(20),width = dp(20),
				on_press = self.add_outils,info = k,
				bg_color = bg_col,pos_hint = (0,.2))
			b.add_button(k,info = k,on_press = self.add_outils,
				text_color = txt_col,halign = 'left',
				bg_color = None)
			self.this_new_surf.add_surf(b)
		self.this_new_surf.add_text_input('Tâche :',(.2,h),
			(.8,h*4),self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,multiline = True,
			placeholder = 'Entrer la tâche à accomplire séparer par la touche entrer',
			on_text = self.set_tache,default_text = self.taches)

		self.this_new_surf.add_text_input('Profile :',(.2,h),
			(.8,h*4),self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,multiline = True,
			placeholder = 'Entrer le profile adéquate',
			on_text = self.set_pofile,default_text = self.Profile)

		self.this_new_surf.add_button_custom("Ajouter",self.add_new_p,
			padd = (.25,h),size_hint = (.5,h))

	@Cache_error
	def add_this_new_surf(self):
		h = .04
		self.this_new_surf.clear_widgets()
		self.this_new_surf.add_text("Catégorie",
			text_color = self.sc.text_col1,size_hint = (.2,h))
		self.this_new_surf.add_surf(liste_set(self,self.this_cate,
			self.sc.DB.Get_categories(),size_hint = (.6,h),
			mult = 1,mother_fonc = self.set_cate))
		self.this_new_surf.add_icon_but(icon = 'printer',
			size_hint = (.2,h),text_color = self.sc.black,
			on_press = self.Impression)

		self.this_new_surf.add_text("Hiérachie",
			text_color = self.sc.text_col1,size_hint = (.2,h))
		self.this_new_surf.add_surf(liste_set(self,self.this_hierachi,
			self.sc.DB.Get_hierachie_list(),size_hint = (.8,h),
			mult = 1,mother_fonc = self.set_hierachi))

		B = stack(self,size_hint = (1,h),spacing = dp(5))
		B.add_input('nom',text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,on_text = self.set_nom,
			placeholder = "Le nom du poste ici",size_hint = (.8,1),
			default_text = self.poste_name)
		if "écritures" in self.sc.DB.Get_access_of("Postes"):
			B.add_icon_but(icon = 'plus',size_hint = (.2,None),
				text_color = self.sc.green,
				on_press = self.add_poste,
				size = (dp(50), dp(25)))
			
		self.this_new_surf.add_surf(B)
		self.this_new_surf.add_surf(self.tab_liste)
		self.add_liste_trie()

	def add_liste_trie(self):
		wid_l = [.4,.3,.3]
		entete = 'nom',"nbres employés","status"
		liste = self.Get_poste_list()
		self.tab_liste.Creat_Table(wid_l,entete,liste,
			ent_size = (1,.05))

	@Cache_error
	def Get_poste_list(self):
		liste = self.sc.DB.Get_all_post_list()
		liste1 = list()
		liste2 = list()
		if self.this_cate:
			liste1 = self.sc.DB.Get_this_categories_poste(self.this_cate)
			liste = [i for i in liste if i in liste1]
		if self.this_hierachi:
			liste2 = self.sc.DB.Get_this_hierachie_poste(self.this_hierachi)
			liste = [i for i in liste if i in liste2]
		liste =  [i for i in liste if self.poste_name.lower() in i.lower()]
		this_liste = list()
		for poste in liste:
			poste_dic = self.sc.DB.Get_this_poste(poste)
			this_liste.append(
				{
					"nom":poste_dic["nom"],
					"nbres employés":len(poste_dic['occupants']),
					"status":poste_dic["status"],
					"date de création":poste_dic['date'],
					"salaire minimal":poste_dic["salaire minimal"]
				}
			)
		return this_liste

# Gestion des actions au niveau des bouttons
	@Cache_error
	def Impression(self,wid):
		obj = self.sc.imp_part_dic('Résumé')(self)
		liste = self.Get_poste_list()
		entete = ['date de création',"nom","nbres employés",'status',
		"salaire minimal"]
		wid_l = [.2]*5
		titre = f"Liste des postes"
		info = str()
		if self.this_cate:
			info += f"Catégorie : {self.this_cate}<br/>"
		if self.this_hierachi:
			info += f"Hiérachie : {self.this_hierachi}<br/>"

		info += "Agence TOKPOTA1"
		obj.Create_fact(wid_l,entete,liste,titre,info)

	@Cache_error
	def add_new_p(self,wid):
		nom = self.New_dict['Nom']
		if not nom:
			self.sc.add_refused_error('Le nom est obligatoire')
		elif nom in self.sc.DB.Get_all_post_list():
			self.sc.add_refused_error('Le nom du poste est déjà existant')
		elif nom.lower() == "admin":
			self.sc.add_refused_error('Vous ne pouvez pas créer un compte <admin>')
		else:
			self.poste_info = self.sc.DB.Poste_save_format()
			self.poste_info['nom'] = nom
			self.poste_info['fonction principal'] = self.New_dict['Fonction']
			self.poste_info['niveau hiérachique'] = self.this_hierachi
			self.poste_info['catégorie'] = self.this_cate
			self.poste_info['salaire minimal'] = self.New_dict['Salaire']
			self.poste_info['outils'] = self.outils_sets
			self.poste_info["tâches"] = [i for i in self.taches.split('\n')]
			self.poste_info['profile'] = [i for i in self.Profile.split('\n')]
			self.excecute(self.sc.DB.Save_poste,self.poste_info)
			#self.sc.DB.Save_poste(self.poste_info)
			self.aff_poste()

	def set_tache(self,wid,val):
		self.taches = val

	def set_pofile(self,wid,val):
		
		self.Profile = val

	def add_outils(self,wid):
		if wid.info in self.outils_sets:
			self.outils_sets.remove(wid.info)
		else:
			self.outils_sets.append(wid.info)
		self.add_new_poste()

	def Set_dic1(self,wid,val):
		if wid.info == 'Salaire':
			try:
				float(val)
			except:
				wid.text = self.regul_input(wid.text)
				if wid.text:
					val = wid.text
				else:
					val = 0
			finally:
				self.New_dict[wid.info] = float(val)
		else:
			self.New_dict[wid.info] = val
			if wid.info == "Nom":
				self.poste_name = val

	def set_hierachi(self,info):
		if self.this_hierachi:
			self.this_hierachi = str()
		else:
			self.this_hierachi = info
		self.add_liste_trie()

	def set_cate(self,info):
		if self.this_cate:
			self.this_cate = str()
		else:
			self.this_cate = info
		self.add_liste_trie()

	def set_nom(self,wid,val):
		self.poste_name = val
		self.add_liste_trie()

	def add_poste(self,wid):
		self.new_poste = True
		self.add_all()

	def aff_poste(self,*args):
		self.new_poste = False
		self.add_all()

	def developpe(self,wid):
		info = wid.info
		self.corps_surf.clear_widgets()
		surf = Gestion_postes(self,self.sc.DB.Get_this_poste(info))
		self.corps_surf.add_surf(surf)

class Gestion_postes(stack):
	def __init__(self,mother,poste_dic,**kwargs):
		kwargs['padding'] = dp(10)
		kwargs['spacing'] = dp(10)

		stack.__init__(self,mother,**kwargs)
		self.check_access = self.mother.check_access
		self.size_pos()

		self.poste_dic = poste_dic
		self.tache = '\n'.join(self.poste_dic.get('tâches'))
		self.profile = '\n'.join(self.poste_dic.get('profile'))
		self.acces_dict = self.sc.Get_access_dict()
		self.curent_acces = str()
		self.curent_menu = str()
		self.curent_part = str()
		self.part_auto = float()

		self.This_access_setting = self.poste_dic.get("accès")
		if self.This_access_setting:
			self.curent_acces = [i for i in self.This_access_setting][0]
			menu_dict = self.This_access_setting.get(self.curent_acces)
			self.curent_menu = [i for i in menu_dict][0]

		self.add_infos()

	def size_pos(self):
		self.acces_surf = stack(self,size_hint = (1,.5),
			bg_color = self.sc.aff_col3)

	@Cache_error
	def add_acces_surf(self):
		h = .08
		self.acces_surf.clear_widgets()
		if self.sc.DB.Get_access_of('Accèss logiciel'):
			self.acces_surf.add_text('Gestion des accès au logiciel',
				text_color = self.sc.text_col1,halign = 'center',
				size_hint = (1,h),font_size = '20sp',
				underline = True)
			self.part1 = stack(self,size_hint = (.3,.9),
				spacing = dp(5),padding = dp(5))
			self.part2 = stack(self,size_hint = (.3,.9),
				spacing = dp(5),padding = dp(5))
			self.part3 = stack(self,size_hint = (.4,.9),
				spacing = dp(5),padding = dp(5))
			self.acces_surf.add_surf(self.part1)
			self.acces_surf.add_surf(self.part2)
			self.acces_surf.add_surf(self.part3)
			self.add_part1()
			self.add_part2()
			self.add_part3()

	@Cache_error
	def add_part1(self):
		self.part1.clear_widgets()
		h = .09
		self.part1.add_text('Les grandes parties',underline = True,
			text_color = self.sc.green,size_hint = (1,h),
			halign = "center")
		sc = scroll(self,size_hint = (1,.89))
		h = dp(25)
		H = dp(10) + (len(self.acces_dict) * (h + dp(10)))
		st = stack(self,size_hint = (1,None),height = H)
		for menu in self.acces_dict:
			bg_col = self.sc.aff_col3
			txt_col = self.sc.text_col1
			f_s = "15sp"
			h = dp(25)
			if menu == self.curent_acces:
				bg_col = self.sc.green
				f_s = "16sp"
			if menu in self.This_access_setting:
				txt_col = self.sc.green
			b = box(self,size_hint = (1,None),height = h,
				orientation = 'horizontal',spacing = dp(5))
			b.add_button('',size_hint = (None,None),
				width = dp(20),
				on_press = self.set_access_part,
				height = dp(20),
				bg_color = bg_col,pos_hint = (0,.1),
				info = menu)
			b.add_button(menu,halign = 'left',
				text_color = txt_col,font_size = f_s,
				bg_color = None,on_press = self.set_access_part,)
			st.add_surf(b)
		sc.add_surf(st)
		self.part1.add_surf(sc)

	@Cache_error
	def add_part2(self):
		h = .09
		self.part2.clear_widgets()
		self.part2.add_text('Les ménus Associées',underline = True,
			text_color = self.sc.green,size_hint = (1,h),
			halign = 'center')
		sc = scroll(self,size_hint = (1,.89))
		h = dp(25)
		menu_liste = self.acces_dict.get(self.curent_acces)
		if menu_liste:
			H = dp(10) + (len(menu_liste) * (h + dp(10)))
			st = stack(self,size_hint = (1,None),height = H)
			for menu in menu_liste:
				bg_col = self.sc.aff_col3
				txt_col = self.sc.text_col1
				f_s = "15sp"
				h = dp(25)
				if menu in self.This_access_setting.get(self.curent_acces,dict()):
					txt_col = self.sc.green
					f_s = "16sp"
				if menu == self.curent_menu:
					bg_col = self.sc.green
				b = box(self,size_hint = (1,None),height = h,
					orientation = 'horizontal',spacing = dp(5))
				b.add_button('',size_hint = (None,None),width = dp(20),
					height = dp(20),
					on_press = self.set_menu_part,
					bg_color = bg_col,pos_hint = (0,.1),
					info = menu)
				b.add_button(menu,halign = 'left',
					text_color = txt_col,font_size = f_s,
					bg_color = None,on_press = self.set_menu_part,)
				st.add_surf(b)
			sc.add_surf(st)
			self.part2.add_surf(sc)

	@Cache_error
	def add_part3(self):
		h = .09
		self.part3.clear_widgets()
		self.part3.add_text('Les Options et leurs autorisation',underline = True,
			text_color = self.sc.green,size_hint = (1,h),
			halign = 'center')
		sc = scroll(self,size_hint = (1,.89))
		h = dp(25)
		menu_liste = self.acces_dict.get(self.curent_acces)
		if menu_liste:
			opt_tupe = menu_liste.get(self.curent_menu,list())
			H = dp(10) + (len(menu_liste) * (h + dp(10)))
			st = stack(self,size_hint = (1,None),height = H)
			this_dicts = self.This_access_setting.get(self.curent_acces,dict())
			my_list = this_dicts.get(self.curent_menu,list())
			listes = [i for i in my_list]
			for menu in opt_tupe:
				menu = menu
				bg_col = self.sc.aff_col1
				txt_col = self.sc.text_col1
				f_s = "15sp"
				if menu == self.curent_part:
					f_s = "16sp"
				if menu in listes:
					txt_col = self.sc.green
					
				b = box(self,size_hint = (1,None),height = h,
					orientation = 'horizontal',spacing = dp(2))
				b.add_button(menu,text_color = txt_col,
					bg_color = None,info = menu,
					on_press = self.Set_options,halign = 'left')
				st.add_surf(b)
			sc.add_surf(st)
			self.part3.add_surf(sc)

	@Cache_error
	def add_infos(self):
		h = .055
		self.add_text(self.poste_dic.get('nom'),
			text_color = self.sc.green,font_size = '18sp',
			size_hint = (.5,h),halign = 'center',)
		self.add_text_input("Nbres d'employés :",(.2,h),(.25,h),
			self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,readonly = True,
			default_text = str(len(self.poste_dic.get('occupants'))),
			)
		self.add_text('Catégorie :',text_color = self.sc.text_col1,
			size_hint = (.15,h))
		self.add_surf(liste_set(self,self.poste_dic.get('catégorie'),
			self.sc.DB.Get_categories(),size_hint = (.3,h),
			mother_fonc = self.modif_cat,mult = 1))

		self.add_text('Hiérachie :',text_color = self.sc.text_col1,
			size_hint = (.12,h))
		self.add_surf(liste_set(self,self.poste_dic.get('niveau hiérachique'),
			self.sc.DB.Get_hierachie_list(),size_hint = (.38,h),
			mother_fonc = self.modif_hie,mult = 1))
		self.add_text_input('fonction principal :',(.25,h),(.4,h),
			self.sc.text_col1,text_color = self.sc.text_col1,
			inp_info = "fonction principal",
			bg_color = self.sc.aff_col3,on_text = self.modif_info,
			default_text = self.poste_dic.get('fonction principal'))

		self.add_text_input('salaire minimal :',(.2,h),(.15,h),
			self.sc.text_col1,text_color = self.sc.text_col1,
			inp_info = "salaire minimal",
			bg_color = self.sc.aff_col3,on_text = self.modif_info,
			default_text = self.poste_dic.get('salaire minimal'))

		self.add_text_input('tâches :',(.1,h),(.4,h*3),self.sc.text_col1,
			bg_color = self.sc.aff_col3,text_color = self.sc.text_col1,
			multiline = True,default_text = self.tache ,
			on_text = self.modif_tache,inp_info = "tâches" )

		self.add_text_input('profile :',(.1,h),(.4,h*3),self.sc.text_col1,
			bg_color = self.sc.aff_col3,text_color = self.sc.text_col1,
			multiline = True,default_text = self.profile,
			on_text = self.modif_profile,inp_info = "profile" )

		self.add_padd((1,.00000001))
		cat = self.poste_dic.get('catégorie')
		if cat in ["Administration","Maintenance"]:
			self.add_acces_surf()
			self.add_surf(self.acces_surf)

		but_liste = ["Modifier le poste",'Lancer un recrutement',
		"Listes des occupants"]
		col_l = [self.sc.green,(0,.15,.5),(1,.5,.15),self.sc.red]
		if len(self.poste_dic.get('occupants')) == 0:
			but_liste.append('Supprimer le poste')
		b = box(self,size_hint = (.8,h),
			orientation = 'horizontal',spacing = dp(5))
		for but,col in zip (but_liste,col_l):
			b.add_button(but,on_press = self.multi_act,
				bg_color = col,text_color = self.sc.text_col3)
		self.add_padd((.1,h))
		self.add_surf(b)
		self.add_padd((.1,h))

# Gestion des actions au niveau de buttons
	@Cache_error
	def set_access_part(self,wid):
		if "écritures" in self.sc.DB.Get_access_of('Accèss logiciel'):
			if self.curent_acces == wid.info:
				self.This_access_setting.pop(self.curent_acces)
				self.curent_acces = str()
				self.curent_menu = str()
			else:
				self.curent_acces = wid.info
				dic = {i:[u for u in j] for i,j in self.acces_dict[self.curent_acces].items()}
				if self.curent_acces in self.This_access_setting:
					pass
				else:
					self.This_access_setting[self.curent_acces] = dic
				self.curent_menu = [i for i in dic][0]
			self.add_part1()
			self.add_part2()
			self.add_part3()
		else:
			self.sc.add_refused_error("Impossible de continuer à cause d'une restriction système !! Parlez-en à votre supérieur hiérachique")

	@Cache_error
	def Set_options(self,wid):
		if "écritures" in self.sc.DB.Get_access_of('Accèss logiciel'):
			part = wid.info
			menu_d = self.This_access_setting.get(self.curent_acces,dict())
			part_l = menu_d.get(self.curent_menu,list())
			if part in part_l:
				part_l.remove(part)
			else:
				part_l.append(part)
			
			menu_d[self.curent_menu] = part_l
			self.This_access_setting[self.curent_acces] = menu_d
			self.add_part3()
		else:
			self.sc.add_refused_error("Impossible de continuer à cause d'une restriction système !! Parlez-en à votre supérieur hiérachique")

	@Cache_error
	def set_menu_part(self,wid):
		if "écritures" in self.sc.DB.Get_access_of('Accèss logiciel'):
			if self.curent_menu == wid.info:
				men_d = self.This_access_setting.get(self.curent_acces)
				if self.curent_menu in men_d:
					men_d.pop(self.curent_menu)
					self.curent_menu = str()
			else:
				self.curent_menu = wid.info
				men_d = self.This_access_setting.get(self.curent_acces)
				all_me_d = self.acces_dict.get(self.curent_acces)
				if self.curent_menu in men_d:
					pass
				else:
					men_d[self.curent_menu] = [i for i in all_me_d.get(self.curent_menu)]
			self.This_access_setting[self.curent_acces] = men_d
			self.add_part2()
			self.add_part3()
		else:
			self.sc.add_refused_error("Impossible de continuer à cause d'une restriction système !! Parlez-en à votre supérieur hiérachique")


	def modif_cat(self,info):
		self.poste_dic['catégorie'] = info

	def modif_hie(self,info):
		self.poste_dic['niveau hiérachique'] = info

	def modif_info(self,wid,val):
		self.poste_dic[wid.info] = val

	def modif_tache(self,wid,val):
		self.tache = val

	def modif_profile(self,wid,val):
		self.profile = val

	def modif_respo(self,info):
		self.poste_dic['responsable'] = info

	def show_recrutement(self,wid):
		pass

	@Cache_error
	def multi_act(self,wid):
		if wid.info == "Modifier le poste":
			if "écritures" in self.sc.DB.Get_access_of('Postes'):
				self.poste_dic['profile'] = self.profile.split("\n")
				self.poste_dic['tâches'] = self.tache.split('\n')
				self.poste_dic['accès'] = self.This_access_setting
				self.excecute(self.sc.DB.Save_poste,self.poste_dic)
				self.mother.add_all()
			else:
				self.sc.add_refused_error("Impossible de continuer à cause d'une restriction système !! Parlez-en à votre supérieur hiérachique")

		elif wid.info == "Supprimer le poste":
			if "écritures" in self.sc.DB.Get_access_of("Supprimer postes"):
				self.excecute(self.sc.DB.Del_poste,self.poste_dic)
				self.mother.add_all()
			else:
				self.sc.add_refused_error("Impossible de continuer à cause d'une restriction système !! Parlez-en à votre supérieur hiérachique")

		elif wid.info == 'Lancer un recrutement':
			if "écritures" in self.sc.DB.Get_access_of('Recrutements'):
				srf = self.mother.mother.menu_dict.get('Recrutements')
				if srf:
					self.mother.mother.curent_menu = "Recrutements"
					self.mother.mother.add_all()
					srf.new_rec = True
					srf.this_post = self.poste_dic.get("nom")
					srf.add_all()
					self.mother.mother.corps_surf.clear_widgets()
					self.mother.mother.corps_surf.add_surf(srf)
				else:
					self.sc.add_refused_error('Accèss refusé')

			else:
				self.sc.add_refused_error("Impossible de continuer à cause d'une restriction système !! Parlez-en à votre supérieur hiérachique")

		elif wid.info == 'Listes des occupants':
			self.mother.corps_surf.clear_widgets()
			self.mother.corps_surf.add_surf(Liste_occupants(self,
				self.poste_dic))

# Liste des occupants à définir après la définition de la gestion du perso
class Liste_occupants(stack):
	def __init__(self,mother,poste_dic,**kwargs):
		stack.__init__(self,mother,**kwargs)
		self.poste_dic = poste_dic
		self.occupants_liste = self.poste_dic.get('occupants')
		self.add_all()

	@Cache_error
	def initialisation(self):
		self.clear_widgets()
		self.add_text('Liste des occupants',size_hint = (.8,.035),
			text_color = self.sc.text_col1,halign = "center",
			underline = True, font_size = "18sp")
		self.add_icon_but(icon = "printer",size_hint = (.1,.035),
			text_color = self.sc.black,	on_press = self.Impression)
		self.add_icon_but(icon = 'close',size_hint = (.1,.035),
			text_color = self.sc.red,on_press = self.BACK)
		self.This_tab = Table(self,size_hint = (1,.95),
			bg_color = self.sc.aff_col3,padding = dp(10),
			radius = dp(10),exec_fonc = self.Show_perso,
			exec_key = "NOM")
		self.add_surf(self.This_tab)

	@Cache_error
	def Foreign_surf(self):
		self.add_infos()

	@Cache_error
	def add_infos(self):
		entete = ["nom",'prénom',"téléphone","whatsapp",
			"durée de contrat"]
		wid_l = .2,.2,.2,.2,.2
		liste = self.get_list()
		self.This_tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.05))

	def get_list(self):
		liste = list()
		for i in self.occupants_liste:
			j = self.sc.DB.Get_this_perso(i)
			j["NOM"] = j["nom"]+'_'+j["prénom"]
			liste.append(j)
		return liste

# Gestion des actions des buttons
	def BACK(self,wid):
		self.mother.mother.corps_surf.clear_widgets()
		self.mother.mother.corps_surf.add_surf(self.mother)

	def Show_perso(self,wid):
		pass

	@Cache_error
	def Impression(self,wid):
		obj = self.sc.imp_part_dic('Résumé')(self)
		liste = self.get_list()
		entete = ["nom","prénom",'poste actuel',"type",
		'téléphone',"whatsapp"]
		wid_l = .15,.15,.15,.15,.2,.2
		titre = f"Liste du personnel"
		info = str()
		info += f"Poste : {self.poste_dic.get('nom')}<br/>"
		
		info += "Agence TOKPOTA1"
		obj.Create_fact(wid_l,entete,liste,titre,info)


