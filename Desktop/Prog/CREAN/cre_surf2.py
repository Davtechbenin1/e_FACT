#Coding:utf-8
"""
"""
from lib.davbuild import *
from General_surf import *
from .cre_all_use import *

class Creances_general(box):
	@Cache_error
	def initialisation(self):
		self.clear_widgets()
		self.orientation = "horizontal"
		self.padding = dp(2)
		self.spacing = dp(10)
		self.size_pos()
		self.type_contra = str()
		self.type_rembou = ''
		self.fin_contrat = str()
		self.trie_client = str()
		self.type_set = 'Trier par le nom'
		self.charg_aff = str()
		self.type_liste = ['Trier par le nom',"Trier par le code"]

		self.trie_dict = {
			#"Lien d'affilliation":(self.type_contra,self.sc.DB.Get_association_list(),
			#	self.set_type_contra),
			#"Chargé d'affaire":(self.charg_aff,self.sc.get_all_charger(),
			#	self.set_charg_aff),
			"Status de la commande":(self.type_rembou,["Livrée","En traitement"],
				self.set_type_rembou),
		}
		self.cmd_ident = str()
		
	@Cache_error
	def Foreign_surf(self):
		self.add_creance_surf()

	def init_wid(self):
		self.clear_widgets()
		self.add_surf(self.creance_surf)
		self.add_creance_surf()

	def size_pos(self):
		w,h = self.creance_size = .4,1
		self.aff_size = 1-w,h

		self.creance_surf = stack(self,size_hint = self.creance_size,
			bg_color = self.sc.aff_col1,radius = dp(10),padding = dp(10),
			spacing = dp(5))

		self.details_surf = Show_creance_surf(self,size_hint = self.aff_size,
			bg_color = self.sc.aff_col1,radius = dp(10),padding = dp(10))

		self.add_surf(self.creance_surf)

	@Cache_error
	def add_creance_surf(self):
		self.imp_titre = 'Liste des Créances Générale'
		h = .045
		self.creance_surf.clear_widgets()
		self.creance_surf.add_surf(Periode_set(self,size_hint = (.25,h),
			info = "Période d'émission",exc_fonc = self.Up_trie,
			info_w = .3))
		for k,tup in self.trie_dict.items():
			txt,liste,fonc = tup
			self.creance_surf.add_text(k,size_hint = (.08,h),
				text_color = self.sc.text_col1,)
			self.creance_surf.add_surf(liste_set(self,txt,liste,size_hint = (.12,h),
				mult = 1, mother_fonc = fonc))
		
		
		self.inp_surf = box(self,orientation = 'horizontal',spacing = dp(5),
			size_hint = (.5,h))
		self.creance_surf.add_surf(self.inp_surf)
		self.Up_inp_surf()
		self.creance_surf.add_icon_but(icon = 'printer',
			text_color = self.sc.black,
			size_hint = (.05,h),on_press =self.Impression)
		
		self.Tab_surf = Table(self,size_hint = (1,.89),
			bg_color = self.sc.aff_col3,exec_key = "id de la commande",
			exec_fonc = self.Show_creance)

		self.creance_surf.add_surf(self.Tab_surf)
		self.total_surf = box(self,orientation = 'horizontal',
			spacing = dp(1),size_hint = (.75,.05),bg_color = self.sc.sep,
			padding = dp(1))
		self.creance_surf.add_padd((.125,.05))
		self.creance_surf.add_surf(self.total_surf)
		self.Up_trie()

	@Cache_error
	def Up_inp_surf(self):
		self.inp_surf.clear_widgets()
		typ_clt = str()
		if self.type_set:
			typ_clt = self.type_set +' du client'
		self.inp_surf.add_input(self.type_set,placeholder = typ_clt,
			on_text = self.set_type,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,size_hint = (.55,1),
			default_text = self.trie_client)
		self.inp_surf.add_surf(liste_set(self,self.type_set,
			self.type_liste,size_hint = (.35,1),mult = 1,
			mother_fonc = self.set_type_form))

	@Cache_error
	def Up_trie(self):
		entete = ['Nom du client',"N° à contacter",
		"chargé d'affaire",
		"montant TTC","montant payé","montant restant",
		"date premier échéance",
		"nombre de jour restant"]

		wid_l = [.17,.12,.12,.12,.12,.12,.12,.11]
		liste = self.Trie_comande()
		self.Tab_surf.Creat_Table(wid_l,entete,liste,ent_size = (1,.065))
		self.add_total_surf()
	
	def add_total_surf(self):
		self.total_surf.clear_widgets()
		for k,v in self.total_infos.items():
			self.total_surf.add_text_input(k,(.15,1),(.08,1),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col1,
				default_text = self.format_val(v),readonly = True,
				halign = 'left',text_halign = "left",txt_pad = dp(10),
				text_text_color = self.sc.aff_col3)

	@Cache_error
	def add_develop_surf(self):
		if self.cmd_ident:
			self.details_surf = Show_creance_surf(self,
				bg_color = self.sc.aff_col1,radius = dp(10))

			self.details_surf.cmd_ident = self.cmd_ident
			self.details_surf.add_all()
			self.add_modal_surf(self.details_surf,size_hint = (.9,.9),
				radius = dp(10), titre = self.cmd_ident)


	def Trie_comande(self):
		periode = self.get_date_list(self.day1,self.day2)
		return self.sort_th_info(periode)

	@Cache_error
	def sort_th_info(self,periode = list()):
		self.total_infos = {
			#"nombres de créances":int(),
			'montant TTC':float(),
			"montant payé":float(),
			"montant restant":float()
		}
		if periode:
			all_crean = self.sc.DB.get_fact_of(periode)
		else:
			all_crean = self.sc.DB.Get_cmd_encours()
		liste = [cmd for cmd in map(self.Trie, all_crean.values()) if cmd]

		if liste:
			for cmd in liste:
				mttc = cmd.get('montant TTC')
				mp = cmd.get('montant payé')
				cmd["montant restant"] = mttc - mp
				self.total_infos['montant TTC'] += mttc
				self.total_infos['montant payé'] += mp
				self.total_infos['montant restant'] += (mttc - mp)
			self.total_infos['nombres de factures'] = len(liste)

		liste.sort(key = itemgetter("th_sort"),reverse = True)
		i = 1
		th_l = list()
		for dic in liste:
			dic["N° d'ordre"] = i
			th_l.append(dic)
			i += 1
		return th_l
			
	def Trie(self,cmd):
		if type(cmd) == str:
			cmd = self.sc.DB.Get_this_cmd(cmd)
		if cmd:
			client_obj = self.sc.DB.Get_this_clt(cmd.get('client'))
			if not client_obj:
				client_obj = dict()
			cmd['nom client'] = client_obj.get('nom',str())
			cmd['Code client'] = client_obj.get('N°',str())
			#th_asso = self.sc.DB.Get_this_association(client_obj.get("association appartenue"))
			Num = client_obj.get('tel')
			cmd['N° à contacter'] = Num
			#cmd["lien d'affiliation"] = th_asso.get('nom',str())
			#cmd["affiliation"] = self.sc.DB.Get_this_association(client_obj.get("association appartenue")).get('nom',str())
			#if self.type_contra:
			#	if cmd.get("lien d'affiliation",str()).lower() != self.type_contra.lower():
			#		return None
			if self.type_rembou:
				if cmd.get("status de la commande").lower() != self.type_rembou.lower():
					return None
			#if self.charg_aff:
			#	if cmd.get("chargé d'affaire",str()).lower()!= self.charg_aff.lower():
			#		return None
			if self.type_set == 'Trier par le nom':
				if self.trie_client.lower() not in cmd.get('nom client').lower():
					return None
			else:
				if self.trie_client.lower() not in cmd.get('numéro client').lower():
					return None
	
			cmd["date d'achat"] = cmd["date de livraison"]
			cmd["catégorie"] = cmd["type de contrat"]
			fist,dates = self.get_date_first_ech(cmd.get("plan de paiements"))
			cmd["date premier échéance"] = fist
			cmd['th_sort'] = int(self.Get_real_num(cmd.get("id de la commande")))
			dif = 0
			if dates:
				a1 = datetime.strptime(self.sc.get_today(),self.date_format)
				a2 = dates[-1]
				dif = (a2-a1).days
			cmd['nombre de jour restant'] = dif
			return cmd

# Gestion des actions de méthodes
	@Cache_error
	def Impression(self,wid):
		obj = self.sc.imp_part_dic('Fiche')(self)
		liste = self.Trie_comande()
		entete = ['Nom du client',"N° à contacter",
		"catégorie","affiliation","chargé d'affaire",
		"montant TTC","montant payé","montant restant",
			"date d'achat","date premier échéance",
			"date de fin contrat","nombre de jour restant"]
		wid_l = [.1,.08,.08,.08,.09,.08,.08,.08,.08,.08,.08,.08,]
		
		titre = self.imp_titre
		info = ''
		if self.type_contra:
			info += f"Lien d'affiliation : {self.type_contra}<br/>"
		if self.type_rembou:
			info += f'status de la commande : {self.type_rembou}<br/>'
		if self.charg_aff:
			info += f"Chargé d'affaire : {self.charg_aff}<br/>"
		
		total_ent = ["montant TTC","montant payé","montant restant"]
		obj.Create_fact(wid_l,entete,liste,titre,info,total_ent)

	def set_type_contra(self,info):
		self.type_contra = info
		self.Up_trie()

	def set_charg_aff(self,info):
		self.charg_aff = info
		self.Up_trie()

	def set_type_rembou(self,info):
		self.type_rembou = info
		self.Up_trie()

	def set_type(self,wid,val):
		self.trie_client = val
		self.Up_trie()

	def set_type_form(self,info):
		self.type_set = info
		self.Up_inp_surf()

	def Show_creance(self,wid):
		self.cmd_ident = wid.info
		self.add_develop_surf()

class Fact_avoir(Creances_general):
	def Trie_comande(self):
		periode = self.get_date_list(self.day1,self.day2)
		return self.sort_th_info(periode)

	def sort_th_info(self,periode = list()):
		self.total_infos = {
			"nbres créances":int(),
			"montant restant":float()
		}
		if periode:
			all_crean = self.sc.DB.get_fact_retour_of(periode)
		else:
			all_crean = self.sc.DB.Get_cmd_encours()
			
		liste = [cmd for cmd in map(self.Trie, all_crean.values()) if cmd]

		if liste:
			for cmd in liste:
				mttc = cmd.get('montant TTC')
				mp = cmd.get('montant payé')
				cmd["montant restant"] = mttc - mp
				self.total_infos['montant restant'] += (mttc - mp)
			self.total_infos['nbres factures'] = len(liste)

		liste.sort(key = itemgetter("th_sort"),reverse = True)
		i = 1
		th_l = list()
		for dic in liste:
			dic["N° d'ordre"] = i
			th_l.append(dic)
			i += 1
		return th_l
		

	def add_creance_surf(self):
		self.imp_titre = 'Liste des Factures avoires'
		h = .045
		self.creance_surf.clear_widgets()
		#self.creance_surf.add_padd((.075,h))
		self.creance_surf.add_surf(Periode_set(self,
			size_hint = (.3,h),
			info = "Période",exc_fonc = self.Up_trie,
			info_w = .2))
		Get_border_input_surf(self.creance_surf,'Trier par nom du client',
			size_hint = (.3,h),bg_color = self.sc.aff_col1,
			on_text = self.set_type,default_text = self.trie_client)
		
		
		#self.creance_surf.add_icon_but(icon = 'printer',
		#	text_color = self.sc.black,
		#	size_hint = (.1,.035),on_press =self.Impression)
		
		
		self.Tab_surf = Table(self,size_hint = (1,.9),
			bg_color = self.sc.aff_col3,
			exec_key = "id de la commande",
			exec_fonc = self.Show_creance)

		self.creance_surf.add_surf(self.Tab_surf)
		self.total_surf = box(self,orientation = 'horizontal',
			spacing = dp(1),size_hint = (1,.045),
			bg_color = self.sc.aff_col3,
			padding = dp(1))
		self.creance_surf.add_surf(self.total_surf)
		
		self.Up_trie()

class Creances_encours(Creances_general):
	@Cache_error
	def initialisation(self):
		self.clear_widgets()
		self.orientation = "horizontal"
		self.padding = dp(2)
		self.spacing = dp(10)
		self.size_pos()
		self.type_contra = str()
		self.type_rembou = 'Livrée'
		self.fin_contrat = str()
		self.trie_client = str()
		self.type_set = 'Trier par le nom'
		self.charg_aff = str()
		self.type_liste = ['Trier par le nom',"Trier par le code"]

		self.trie_dict = {
			#"Lien d'affilliation":(self.type_contra,self.sc.DB.Get_association_list(),
			#	self.set_type_contra),
			#"Chargé d'affaire":(self.charg_aff,self.sc.get_all_charger(),
			#	self.set_charg_aff),
		}
		self.cmd_ident = str()
		
	def Trie_comande(self):
		return self.sort_th_info()
			
	@Cache_error
	def add_creance_surf(self):
		h = .045
		self.imp_titre = 'Liste des Créances en cours'
		self.creance_surf.clear_widgets()
		for k,tup in self.trie_dict.items():
			txt,liste,fonc = tup
			self.creance_surf.add_text(k,size_hint = (.1,h),
				text_color = self.sc.text_col1,)
			self.creance_surf.add_surf(liste_set(self,txt,liste,
				size_hint = (.2,h),
				mult = 1, mother_fonc = fonc))
		
		self.inp_surf = box(self,orientation = 'horizontal',spacing = dp(5),
			size_hint = (.5,h))
		self.creance_surf.add_surf(self.inp_surf)
		self.creance_surf.add_icon_but(icon = 'printer',text_color = self.sc.black,
			size_hint = (.2,.035),on_press =self.Impression)
		
		self.Up_inp_surf()

		self.Tab_surf = Table(self,size_hint = (1,.9),
			bg_color = self.sc.aff_col3,exec_key = "id de la commande",
			exec_fonc = self.Show_creance)
		self.creance_surf.add_surf(self.Tab_surf)
		self.total_surf = box(self,orientation = 'horizontal',
			spacing = dp(1),size_hint = (.75,.05),bg_color = self.sc.sep,
			padding = dp(1))
		self.creance_surf.add_padd((.125,.05))
		self.creance_surf.add_surf(self.total_surf)
		self.Up_trie()

class Creance_impayer(Creances_general):
	@Cache_error
	def initialisation(self):
		self.clear_widgets()
		self.orientation = "horizontal"
		self.padding = dp(2)
		self.spacing = dp(2)
		self.size_pos()
		self.type_contra = str()
		self.type_rembou = 'Livrée'
		self.fin_contrat = str()
		self.trie_client = str()
		self.type_set = 'Trier par le nom'
		self.charg_aff = str()
		self.type_liste = ['Trier par le nom',"Trier par le code"]

		self.trie_dict = {
			#"Lien d'affilliation":(self.type_contra,self.sc.DB.Get_association_list(),
			#	self.set_type_contra),
			#"Chargé d'affaire":(self.charg_aff,self.sc.get_all_charger(),
			#	self.set_charg_aff),
		}
		self.cmd_ident = str()

	def Trie_comande(self):
		#all_crean = self.mother.creance_imp
		return self.sort_th_info()

	def sort_th_info(self):
		self.total_infos = {
			#"nombres de créances":int(),
			'montant TTC':float(),
			"montant payé":float(),
			"montant restant":float()
		}
		all_crean = self.sc.DB.Get_cmd_impayer()
		liste = [cmd for cmd in map(self.Trie, all_crean.values()) if cmd]

		if liste:
			for cmd in liste:
				mttc = cmd.get('montant TTC')
				mp = cmd.get('montant payé')
				cmd["montant restant"] = mttc - mp
				self.total_infos['montant TTC'] += mttc
				self.total_infos['montant payé'] += mp
				self.total_infos['montant restant'] += (mttc - mp)
			self.total_infos['nombres de factures'] = len(liste)

		liste.sort(key = itemgetter("th_sort"),reverse = True)
		i = 1
		th_l = list()
		for dic in liste:
			dic["N° d'ordre"] = i
			th_l.append(dic)
			i += 1
		return th_l


	@Cache_error
	def Up_trie(self):
		entete = ['Nom du client',"N° à contacter",
		"chargé d'affaire","montant TTC","montant payé",
		"montant restant","pénalité","date premier échéance",
		"nombre de jour restant"]
		wid_l = [.15,.11,.11,.11,.11,.11,.08,.11,.11]
		
		liste = self.Trie_comande()
		self.Tab_surf.Creat_Table(wid_l,entete,liste,ent_size = (1,.065),
			ligne_h = .08)
		self.add_total_surf()

	@Cache_error
	def add_creance_surf(self):
		h = .045
		self.imp_titre = 'Liste des Créances impayées'
		self.creance_surf.clear_widgets()
		for k,tup in self.trie_dict.items():
			txt,liste,fonc = tup
			self.creance_surf.add_text(k,size_hint = (.1,h),
				text_color = self.sc.text_col1,)
			self.creance_surf.add_surf(liste_set(self,txt,liste,
				size_hint = (.2,h),
				mult = 1, mother_fonc = fonc))
		
		self.inp_surf = box(self,orientation = 'horizontal',spacing = dp(5),
			size_hint = (.5,h))
		self.creance_surf.add_surf(self.inp_surf)
		self.creance_surf.add_icon_but(icon = 'printer',text_color = self.sc.black,
			size_hint = (.2,.035),on_press =self.Impression)
		
		self.Up_inp_surf()

		self.Tab_surf = Table(self,size_hint = (1,.9),
			bg_color = self.sc.aff_col3,exec_key = "id de la commande",
			exec_fonc = self.Show_creance)
		self.creance_surf.add_surf(self.Tab_surf)
		self.total_surf = box(self,orientation = 'horizontal',
			spacing = dp(1),size_hint = (.75,.05),bg_color = self.sc.sep,
			padding = dp(1))
		self.creance_surf.add_padd((.125,.05))
		self.creance_surf.add_surf(self.total_surf)
		self.Up_trie()

	@Cache_error
	def Impression(self,wid):
		obj = self.sc.imp_part_dic('Fiche')(self)
		liste = self.Trie_comande()
		entete = ['Nom du client',"N° à contacter",
			"catégorie","affiliation","chargé d'affaire",
			"montant TTC","montant payé","montant restant",
			"pénalité","date d'achat","date premier échéance",
			"date de fin contrat","nombre de jour restant"]
		wid_l = [.12,.07,.07,.07,.08,.07,.07,.07,.06,.07,.07,.08,.08,]
		
		titre = self.imp_titre
		info = ''
		if self.type_contra:
			info += f"Lien d'affiliation : {self.type_contra}<br/>"
		if self.type_rembou:
			info += f'Type de remboursement : {self.type_rembou}<br/>'
		if self.charg_aff:
			info += f"Chargé d'affaire : {self.charg_aff}<br/>"
		
		info += 'Agence TOKPOTA1'
		total_ent = ["montant TTC","montant payé","montant restant"]
		obj.Create_fact(wid_l,entete,liste,titre,info,total_ent)

