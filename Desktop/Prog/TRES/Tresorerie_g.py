#Coding:utf-8
"""
	Gestion de la trésorerie générale du logiciel. 
	Même approche que celui de l'accueil.
"""
from lib.davbuild import *
from General_surf import *
from ..ACC.Accueil import Accueil
from kivy.utils import get_color_from_hex
from .Trs_surf import *

class Tress_general(Accueil):
	@Cache_error
	def initialisation(self):
		#self.padding = dp(10)
		self.bg_color = self.sc.aff_col3
		self.add_bg_color()

		self.but_dic = {
			"Trésorerie":"cash-multiple",
			"Prévisionnel":"calendar-clock",
			"Analyse financière":"chart-line",
			"Comptabilité simplifiée":"file-chart-outline",
			"Journal (Historique)":"history",
		}
		self.but_surf_dic = {
			"Trésorerie":Tresorerie(self,bg_color = self.sc.aff_col2),
			"Prévisionnel":box(self,bg_color = self.sc.aff_col2),
			"Analyse financière":box(self,bg_color = self.sc.aff_col2),
			"Comptabilité simplifiée":box(self,bg_color = self.sc.aff_col2),
			"Journal (Historique)":box(self,bg_color = self.sc.aff_col2)
		}
		self.but_col_dic = {
			"Trésorerie":get_color_from_hex("#1565C0"),
			"Prévisionnel":get_color_from_hex("#F9A825"),
			"Analyse financière":get_color_from_hex("#8E24AA"),
			"Comptabilité simplifiée":get_color_from_hex("#43A047"),
			"Journal (Historique)":get_color_from_hex("#546E7A")
		}
	def size_pos(self):
		self.clear_widgets()
		w,h = self.buts_size = 1,.1
		self.aff_size = w,1-h

		self.but_s = box(self,padding = [dp(15),dp(15),dp(15),dp(0)],spacing = dp(20),
			orientation = 'horizontal',size_hint = self.buts_size)
		self.but_s.width = self.but_s.minimum_width
		self.aff_surf = Aff_surf(self,size_hint = self.aff_size)
		self.aff_surf.add_all()

		self.add_surf(self.but_s)
		self.add_surf(self.aff_surf)

class Aff_surf(box):
	pass

class Creance_charger(Tresorerie):
	@Cache_error
	def initialisation(self):
		self.size_pos()
		self.menu_ico_dic = {
			#"Livraison":"truck-delivery",
			"Créances en cours":"account-cash-outline",
			"Echéances":"calendar-clock",
			"Vos clients":"account-multiple-outline",
		}
		self.menu_surf_dic = {
			#"Livraison":Livraison,
			"Créances en cours":Creance,
			"Echéances":echeance,
			"Vos clients":Vos_clients,
		}
		self.menu_in_action = str()
		#self.add_all()
	def size_pos(self):
		w,h = self.menu_size = 1,.039
		self.aff_size = w,1-h

		self.menu_surf = stack(self,size_hint = self.menu_size,
			bg_color = self.sc.aff_col3,radius = dp(10))

		self.aff_surf = box(self,size_hint = self.aff_size,
			bg_color = self.sc.aff_col1,padding = dp(10),radius = dp(10))

		self.add_surf(self.menu_surf)
		self.add_surf(self.aff_surf)

	@Cache_error
	def Foreign_surf(self):
		self.Get_infos()
		self.add_menu_surf()

	def Get_infos(self):
		self.charger = self.sc.get_profile_perso()
		self.all_commande = dict()
		self.a_livrer = dict()
		self.echeance_dict = dict()
		ALL_dic = self.sc.DB.Get_cmd_non_sold()
		for num,dic in ALL_dic.items():
			clt_d = self.sc.DB.Get_this_clt(dic.get('client'))
			if clt_d.get("chargé d'affaire") == self.charger:
				dic = self.sc.DB.Get_this_cmd(num)
				if dic:
					thd_d = self.sc.DB.Get_format_creance_char()
					thd_d['N°'] = num
					thd_d["lien d'affiliation"] = clt_d.get("lien d'affiliation")
					thd_d['téléphone'] = clt_d.get('tel')
					thd_d['client'] = dic.get('client')
					thd_d['nom du client'] = clt_d.get('nom')
					thd_d['montant TTC'] = dic.get('montant TTC')
					thd_d['montant payé'] = dic.get('montant payé')
					thd_d['status de la commande'] = dic.get('status de la commande')
					thd_d["date de fin de contrat"] = dic.get('date de fin contrat')
					thd_d["nombre d'echéance"] = len(dic.get('plan de paiements'))-1
					self.all_commande[num] = thd_d
					if thd_d.get('status de la commande').lower() != 'livrée':
						self.a_livrer[num] = thd_d
					eche = self.Get_echeance(dic)
					if eche:
						eche["lien d'affiliation"] = clt_d.get("lien d'affiliation")
						eche['téléphone'] = clt_d.get('tel')
						eche["nom du client"] = clt_d.get('nom')
						eche['N°'] = num
						self.echeance_dict[num] = eche

	def Get_echeance(self,cmd_d):
		plan_dic = cmd_d.get('plan de paiements',dict())
		echeance_info = {
			"Num":self.Get_real_num(cmd_d.get("id de la commande")),
			"date":self.sc.get_today(),
			"client":cmd_d.get('client'),
			"montant de la commande":cmd_d.get('montant TTC'),
			"montant déjà payé":cmd_d.get('montant payé'),
			"impayée":float(),
			"nombre d'impayée":int(),
			"en cours":float(),
			"montant collectée":float(),
			"mode de paiement":str(),
			"référence":str()
		}
		if plan_dic:
			dates = [datetime.strptime(date,self.date_format) for date in plan_dic]
			today = datetime.strptime(self.sc.get_today(),self.date_format)
			encours = float()
			if today in dates:
				encours = plan_dic[today.strftime(
					self.date_format)].get('montant restant')
			liste = [i for i in dates if i<today]
			impay = float()
			nbr_imp = int()
			for date in liste:
				mont = plan_dic.get(date.strftime(self.date_format)
					).get('montant restant')
				if mont:
					impay += mont
					nbr_imp += 1
			if encours>0 or impay > 0:
				echeance_info["impayée"] = impay
				echeance_info['en cours'] = encours
				echeance_info["nombre d'impayée"] = nbr_imp
				return echeance_info

class Livraison(stack):
	@Cache_error
	def initialisation(self):
		self.all_commande = self.mother.a_livrer
		self.charger = self.mother.charger
		self.nom_clt = str()
		self.this_periode = Periode_set(self,size_hint = (.12,.045),
			one_part = True,info = str(),info_w = .001,
			exc_fonc = self.set_this_definition,)
		self.titre = "Fiche de livraison du"
		self.entete = ["Num","nom du client","téléphone","lien d'affiliation"
		,"montant TTC","montant payé",
			"pourcentage d'accompte","montant d'accompte",
			"montant total reçus","livret de suivit"]
		self.wid_l = [.1]*10
		self.wid_ll = .2,.1,.1,.1,.1,.1,.1,.1,.1,.1
		self.titre_prefait = ("Num","nom du client","montant TTC","montant payé",
			"téléphone","lien d'affiliation")
		self.titre_mont = ("montant TTC","montant payé")
		self.total_ent = ["montant total reçus",'livret de suivit']

	def Get_this_defin(self):
		self.this_definition = self.sc.DB.Get_livraison_of(self.charger,self.day1)

	@Cache_error
	def Foreign_surf(self):
		h = .05
		self.mother.Get_infos()
		self.Get_this_defin()
		self.clear_widgets()
		self.add_padd((.05,h))
		self.add_text(self.titre,size_hint = (.15,h),
			text_color = self.sc.text_col1)
		self.add_surf(self.this_periode)
		self.add_icon_but(icon = 'printer', text_color = self.sc.black,
			size_hint = (.1,h),on_press = self.Impress_cmd)
		self.add_text_input("Nom du client",(.15,h),(.35,h),
			self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,on_text = self.set_clt_name, 
			placeholder = 'Le nom du client ici')
		b = box(self,size_hint = (1,h),padding = dp(1),spacing = dp(1),
				bg_color = self.sc.black,orientation = 'horizontal')
		self.add_padd((1,.01))
		self.add_surf(b)
		for num,ent in enumerate(self.entete):
			b.add_text(ent,text_color = self.sc.text_col1,
				halign = 'left',bg_color = self.sc.aff_col3,
				size_hint = (self.wid_l[num],1),padding_left = dp(5))
		self.trie_info = scroll(self,size_hint = (1,.8))
		self.add_surf(self.trie_info)
		self.add_button_custom("Valider",self.save_infos,
			size_hint = (.2,h),padd = (.4,h),
			text_color = self.sc.text_col1,
			bg_color = self.sc.orange)
		self.Set_trie_info()

	@Cache_error
	def Set_trie_info(self):
		self.trie_info.clear_widgets()
		h = .065
		hh = dp(50)
		liste = [i for i in map(self.trie,self.all_commande.values()) if i]
		liste = self.Sort_infos(liste,"Num")
		Sta = stack(self,size_hint = (1,None),height = hh*(len(liste)+dp(3)) )
		self.trie_info.add_surf(Sta)
		for dic in liste:
			b = box(self,size_hint = (1,None),padding = [dp(1),0,dp(1),dp(1)],
				spacing = dp(1),bg_color = self.sc.black,
				orientation = 'horizontal',height = hh)
			Sta.add_surf(b)
			for num,ent in enumerate(self.entete):
				read = False
				if self.day1 != self.sc.get_today():
					read = True
				text_color = self.sc.black
				bg_color = self.sc.aff_col3
				if ent in self.titre_prefait:
					val = dic.get(ent)
					if ent in self.titre_mont:
						val = self.format_val(val)
					read = True
					text_color = self.sc.aff_col1
					bg_color = self.sc.aff_col1
					b.add_text(self.format_val(val),text_color = self.sc.text_col1,bg_color = bg_color,
						size_hint = (self.wid_l[num],1),padding_left = dp(5),
						)
				else:
					val = self.this_definition.get(dic.get('N°'),
						dict()).get(ent,str())
					b.add_input(f"{ent}((_)){dic.get('N°')}",
						text_color = self.sc.text_col1,bg_color = bg_color,
						on_text = self.set_all_infos,readonly = read,
						size_hint = (self.wid_l[num],1),padding_left = dp(5),
						default_text = val)

	def trie(self,dic):
		if self.nom_clt.lower() in dic.get('nom du client',str()).lower():
			num = self.Get_real_num(dic.get('N°'))
			dic['Num'] = num
			return dic

	def trie_(self,dic):
		entete = ["pourcentage d'accompte","montant d'accompte",
			"montant total reçus","livret de suivit"]
		#if dic.get('status de la commande').lower() != 'livrée':
		num = self.Get_real_num(dic.get('N°'))
		dic['Num'] = num
		for ent in entete:
			dic[ent] = self.this_definition.get(dic.get('N°'),dict()).get(ent,str())

		return dic

# Gestion des actions des bouttons
	@Cache_error
	def save_infos(self,wid):
		if self.this_definition:
			self.excecute(self.sc.DB.Save_livraison_of_ch,
				self.charger,self.this_definition)
			#self.sc.DB.Save_livraison_of_ch(self.charger,self.this_definition)
			self.sc.add_refused_error("Fiche d'enrégistrement sauvegardée avec succès!")
		else:
			self.sc.add_refused_error('Rien à enrégistrer')

	def set_this_definition(self,*args):
		self.add_all()

	@Cache_error
	def Impress_cmd(self,wid):
		liste = [i for i in map(self.trie_,self.all_commande.values()) if i]
		liste = self.Sort_infos(liste,"Num")
		entete = [i for i in self.entete if i != "Num"]
		wid_l = self.wid_ll
		obj = self.sc.imp_part_dic('Fiche')(self)
		titre = self.titre
		info = f"Chargé d'affaire : {self.charger}<br/>"
		info += f"date de livraison : {self.day1}<br/>"
		info += 'Agence TOKPOTA1'
		total_ent = self.total_ent
		obj.Create_fact(wid_l,entete,liste,titre,info,total_ent)

	def set_clt_name(self,wid,val):
		self.nom_clt = val
		self.Set_trie_info()

	def set_all_infos(self,wid,val):
		if self.sc.get_today() == self.day1:
			part,info = wid.info.split('((_))')
			th_d = self.this_definition.get(info,dict())
			th_d[part] = val
			self.this_definition[info] = th_d
		else:
			self.sc.add_refused_error("Impossible de modifier les informations définie précédemment !!")
			wid.text = str()

class Creance(Livraison):
	@Cache_error
	def initialisation(self):
		self.all_commande = self.mother.all_commande
		self.charger = self.mother.charger
		self.nom_clt = str()
		self.this_periode = Periode_set(self,size_hint = (.12,.045),
			one_part = True,info = str(),info_w = .001,
			exc_fonc = self.set_this_definition,)
		self.titre = "Fiche de gestion des Créances du"
		self.entete = ["Num","nom du client","montant TTC","montant payé",
			"téléphone","lien d'affiliation",
			"montant restant",
			"montant collectée","mode de paiments","référence"]
		self.wid_l = [.1]*10
		self.wid_ll = .2,.1,.1,.1,.1,.1,.1,.1,.1,.1
		self.titre_prefait = ("Num","nom du client","montant TTC",
			"montant payé","montant restant","téléphone","lien d'affiliation")
		self.titre_mont = ("montant TTC","montant payé","montant restant")
		self.total_ent = ["montant collectée"]

	def trie(self,dic):
		if self.nom_clt.lower() in dic.get('nom du client',str()).lower():
			num = self.Get_real_num(dic.get('N°'))
			dic['Num'] = num
			try:
				dic["montant restant"] = float(dic['montant TTC']) - float(dic["montant payé"])
			except Exception as E:
				self.sc.add_refused_error(E)
				dic["montant restant"] = 0
			return dic

	def trie_(self,dic):
		entete = ["montant collectée","mode de paiments","référence"]
		num = self.Get_real_num(dic.get('id de la commande'))
		dic['Num'] = num
		try:
			dic["montant restant"] = float(dic['montant TTC']) - float(dic["montant payé"])
		except Exception as E:
			self.sc.add_refused_error(E)
			dic["montant restant"] = 0

		for ent in entete:
			dic[ent] = self.this_definition.get(ent,str())
		return dic


	def Get_this_defin(self):
		self.this_definition = self.sc.DB.Get_creance_fiche_of(self.charger,self.day1)

	@Cache_error
	def save_infos(self,wid):
		if self.this_definition:
			for cmd_num in self.this_definition:
				cmd_dic = self.sc.DB.Get_this_cmd(cmd_num)
				self.this_definition[cmd_num]['montant de la commande'] = cmd_dic.get('montant TTC')
				self.this_definition[cmd_num]['montant déjà payé'] = cmd_dic.get('montant payé')
				self.this_definition[cmd_num]['montant restant'] = cmd_dic.get('montant TTC') - cmd_dic.get('montant payé')
				self.this_definition[cmd_num]["date d'émission"] = cmd_dic.get("date d'émission")
				self.this_definition[cmd_num]['client'] = cmd_dic.get('client')
			self.excecute(self.sc.DB.Save_creance_fiche_of,
				self.charger, self.this_definition)
			#self.sc.DB.Save_creance_fiche_of(self.charger,self.this_definition)
			self.sc.add_refused_error("Fiche d'enrégistrement sauvegardée avec succès!")
		else:
			self.sc.add_refused_error('Rien à enrégistrer')

class Vos_clients(stack):
	@Cache_error
	def initialisation(self):
		self.charger = self.mother.charger
		self.all_commande = self.mother.all_commande
		self.total_info = float()
		self.mother.Get_infos()
		self.clear_widgets()
		h = .05
		self.affil_list = list()
		liste = self.sc.DB.Get_clt_list()
		all_clt = [self.sc.DB.Get_this_clt(i) 
			for i in liste ]
		self.all_client = [i for i in map(self.Trie_F,all_clt) if i]
		self.add_text('Liste de vos clients et leur solde',
			text_color = self.sc.text_col1,halign = 'center',
			size_hint = (.9,.035),underline = True)
		self.add_icon_but(icon = "printer",text_color = self.sc.black,
			size_hint = (.1,.035),on_press = self.Print_clt)
		self.solde_typ = str()
		self.solde_list = ["Normal","Positif","Négatif"]
		self.affil_typ = str()
		dic = {
			"Solde du client":(self.solde_typ,self.solde_list,
				self.set_solde_typ),
			"lien d'affiliation":(self.affil_typ,self.affil_list,
				self.set_affil_typ)
		}
		for k,tup in dic.items():
			self.add_text(k,text_color = self.sc.text_col1,
				size_hint = (.1,h))
			txt,lis,fonc = tup
			self.add_surf(liste_set(self,txt,lis,mother_fonc = fonc,
				size_hint = (.3,h),mult = 1))
		self.add_text_input('Solde total',(.08,h),(.12,h),
			self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col1,font_size = "17sp",
			readonly = True, default_text = self.format_val(self.total_info))		

		self.tab_info = Table(self,size_hint = (1,.91),padding = dp(10),
			radius = dp(10))
		self.add_surf(self.tab_info)
		self.add_tab_info()

	@Cache_error
	def add_tab_info(self):
		entete = ["code client","nom","solde","status","date d'enregistrement",
		"lien d'affiliation","Solde comptable","nombre de commande"]
		wid_l = [.15,.15,.11,.11,.12,.12,.12,.12]
		liste = [i for i in map(self.Trie,self.all_client) if i]
		self.tab_info.Creat_Table(wid_l,entete,liste,ent_size = (1,.065),
			ligne_h = .06)

	def Trie(self,dic):
		if self.solde_typ:
			if dic.get('Solde comptable').lower() != self.solde_typ.lower():
				return None
		if self.affil_typ:
			if dic.get("lien d'affiliation").lower() != self.affil_typ.lower():
				return None
		return dic

	def Trie_F(self,dic):
		if dic:
			if dic.get("chargé d'affaire").lower() != self.charger.lower():
				return None
			aff = dic.get("lien d'affiliation")
			if aff not in self.affil_list:
				self.affil_list.append(aff)
			mont_ttc = dic.get('solde')
			if mont_ttc:
				self.total_info += float(mont_ttc)
			cmd_list = dic.get('commandes',list())
			ind = 0
			for ident in cmd_list:
				cmd = self.all_commande.get(ident)
				if cmd and cmd.get('status de la commande') == 'Livrée':
					ind += 1
			dic['nombre de commande'] = ind
			return dic

# Gestion des actions des boutons
	def set_solde_typ(self,info):
		self.solde_typ = info
		self.add_tab_info()

	def set_affil_typ(self,info):
		self.affil_typ = info
		self.add_tab_info()

	@Cache_error
	def Print_clt(self,wid):
		liste = [i for i in map(self.Trie,self.all_client) if i]
		entete = ["code client","nom","solde","status","date d'enregistrement",
		"lien d'affiliation","Solde comptable","nombre de commande"]
		wid_l = [.19,.15,.11,.11,.11,.11,.11,.11]
		obj = self.sc.imp_part_dic('Fiche')(self)
		titre = "Liste des vos clients et leur soldes"
		info = f"Chargé d'affaire : {self.charger}<br/>"
		if self.solde_typ:
			info += f"Solde comptable : {self.solde_typ}<br/>"
		if self.affil_typ:
			info += f"Lien d'affiliation : {self.affil_typ}<br/>"
		info += 'Agence TOKPOTA1'
		total_ent = ["solde","nombre de commande"]
		obj.Create_fact(wid_l,entete,liste,titre,info,total_ent)

class echeance(Livraison):
	@Cache_error
	def initialisation(self):
		self.all_commande = self.mother.echeance_dict
		self.charger = self.mother.charger
		self.nom_clt = str()
		self.this_periode = box(self,size_hint = (.12,.045)) #Periode_set(self,size_hint = (.12,.045),
			#one_part = True,info = str(),info_w = .001,
			#exc_fonc = self.set_this_definition,)
		self.titre = f"Fiche des Echéances du {self.sc.get_today()}"
		self.entete = ["Num","nom du client","téléphone","lien d'affiliation",
			"montant déjà payé","impayée","nombre d'impayée","en cours",
			]
		self.wid_l = .1,.1,.1,.1,.1,.1,.1,.1,.1,.1
		self.wid_ll = .2,.1,.1,.1,.1,.1,.1,.1,.1
		self.titre_prefait = self.entete.copy()#("Num","nom du client","téléphone","lien d'affiliation",
			#"montant déjà payé","impayée","nombre d'impayée","en cours",)
		self.titre_mont = ("montant de la commande",
			"montant déjà payé","impayée","nombre d'impayée","en cours")
		self.total_ent = ["montant collectée"]

	def trie(self,dic):
		if self.nom_clt.lower() in dic.get('nom du client',str()).lower():
			num = self.Get_real_num(dic.get('N°'))
			dic['Num'] = num
			try:
				dic["montant restant"] = float(dic['montant TTC']) - float(dic["montant payé"])
			except Exception as E:
				dic["montant restant"] = 0
			return dic

	def trie_(self,dic):
		entete = ["montant collectée","mode de paiments","référence"]
		
		try:
			dic["montant restant"] = (float(dic['montant de la commande'])
				- float(dic["montant déjà payé"]))
		except Exception as E:
			dic["montant restant"] = 0
		
		for ent in entete:
			val = self.this_definition.get(dic.get('N°'),dict()).get(ent,str())
			dic[ent] = val
		return dic

	def Get_this_defin(self):
		self.this_definition = self.sc.DB.Get_echeance_fiche_of(self.charger,self.day1)

	def save_infos(self,wid):
		if self.this_definition:
			self.excecute(self.sc.DB.Save_echeance_fiche_of,
				self.charger,self.this_definition)
			self.sc.add_refused_error("Fiche d'enrégistrement sauvegardée avec succès!")
		else:
			self.sc.add_refused_error('Rien à enrégistrer')

	@Cache_error
	def Impress_cmd(self,wid):
		liste = [i for i in map(self.trie_,self.all_commande.values()) if i]
		liste = self.Sort_infos(liste,"Num")
		entete = [i for i in self.entete if i != "Num"]
		wid_l = self.wid_ll
		obj = self.sc.imp_part_dic('Fiche')(self)
		titre = self.titre
		info = f"Chargé d'affaire : {self.charger}<br/>"
		info += f"date de livraison : {self.day1}<br/>"
		info += 'Agence TOKPOTA1'
		total_ent = self.total_ent
		obj.Create_fact(wid_l,entete,liste,titre,info,total_ent)

