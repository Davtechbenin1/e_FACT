#Coding:utf-8
"""
	Gestion des surfs utilisées pour la gestion des créances.
"""
from lib.davbuild import *
from General_surf import *
from .cre_all_use import *

class Creances_ch(box):
	"""
		Gestion des créances par chargé d'affaires
	"""
	@Cache_error
	def initialisation(self):
		self.clear_widgets()
		self.orientation = 'horizontal'
		self.spacing = dp(2)
		self.padding = dp(2)
		self.charger = str()
		self.associa = str()
		self.status = str()
		self.status_list = ["Soldée","En cours","Impayée"]
		self.f_liste = list()
		self.th_clt_name = str()
		self.cmd_ident = str()
		self.size_pos()

	@Cache_error
	def Foreign_surf(self):
		self.this_creance = self.sc.DB.Get_cmd_non_sold()
		self.add_ech_surf()

	def size_pos(self):
		w,h = self.ech_size = .4,1
		self.aff_size = 1-w,h

		self.ech_surf = stack(self,size_hint = self.ech_size,
			bg_color = self.sc.aff_col1,radius = dp(10),
			padding = dp(10),spacing = dp(5))

		self.add_surf(self.ech_surf)

	def add_ech_surf(self):
		...

	def add_pied_surf(self,lenf):
		self.pied_surf.clear_widgets()
		dic = {
			"Nombre total":lenf,
			"montant total des impayée":self.all_imp,
			"montant total des encoure":self.all_encour,
			"montant total à payer":self.all_paye,
		}
		self.pied_surf.add_text('',size_hint = (.1,1))
		for k,v in dic.items():
			b = box(self,radius = dp(10),bg_color = self.sc.aff_col3, 
				padding = dp(5),size_hint = (.1,1))
			b.add_text_input(k,(1,1),(1,1),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col1,
				radius = dp(5),halign = 'center',text_halign = 'center',
				default_text = self.format_val(v),readonly= True)
			self.pied_surf.add_surf(b)
		self.pied_surf.add_text("",size_hint = (.1,1))

	def Up_tab(self,new_date = False):
		entete = ("date d'achat","Nom du client","N° à contacter",
			"catégorie","chargé d'affaire",
			"montant de l'échéance","nombre d'impayé",
			"échéance échus non payé","total à payer ce jours",
			)
		wid_l = .11,.15,.12,.11,.11,.1,.1,.1,.1,.1
		liste = self.Trie_infos()
		self.Tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.075),
			apply_col_fonc = self.apply_fonc_col)

	def apply_fonc_col(self,data,ent):
		if ent == 'total à payer ce jours':
			return self.sc.orange
		elif ent == "nombre d'impayé":
			if data.get(ent) > 0:
				return self.sc.red
		elif ent == "échéance échus non payé":
			if data.get(ent) > 0:
				return self.sc.red
		return self.sc.text_col1

	def Trie_infos(self):
		liste = self._trie()
		self.add_pied_surf(len(liste))
		return liste

	def _trie(self):
		liste = list()
		all_cmd_dic = self.sc.DB.Get_cmd_non_sold()
		self.all_imp = float()
		self.all_encour = float()
		self.all_paye = float()
		for cmd_dic in all_cmd_dic.values():
			cmd = self.edite_cmd(cmd_dic)
			if cmd:
				liste.append(cmd)
		liste.sort(key = itemgetter("Num"),reverse = True)
		th_o = 1
		for dic in liste:
			dic["N° d'ordre"] = th_o
			th_o += 1
		return liste

	def edite_cmd(self,cmd_dic):
		cmd_dic = self.mother.edite_cmd(cmd_dic)
		if cmd_dic:
			montant_impay = cmd_dic.get('échéance échus non payé')
			encoure = cmd_dic.get("montant de l'échéance")
			clt_dic = self.sc.DB.Get_this_clt(cmd_dic.get('client'))
			if self.charger:
				if cmd_dic.get("chargé d'affaire").lower() != self.charger.lower():
					return None
			if self.associa:
				if cmd_dic.get('affiliation').lower() != self.associa.lower():
					return None
			if self.th_clt_name.lower() not in clt_dic.get('nom').lower():
				return None
			self.all_imp += montant_impay
			self.all_encour += encoure
			self.all_paye += (montant_impay + encoure)
			return cmd_dic
		else:
			return None

	def init_wid(self):
		self.close_modal()

	@Cache_error
	def add_develop_surf(self):
		self.aff_surf = th_Show_creance_surf(self,
			bg_color = self.sc.aff_col1,radius = dp(10),
			padding = dp(10),spacing = dp(5))

		if self.cmd_ident:
			self.aff_surf.cmd_ident = self.cmd_ident
			self.aff_surf.add_all()
			self.add_modal_surf(self.aff_surf,size_hint = (.9,.9))

# Gestion des actions des bouttons
	@Cache_error
	def impression(self,wid):
		obj = self.sc.imp_part_dic('Fiche')(self)
		liste = self.Trie_infos()
		entete = ["date d'achat","Nom du client","N° à contacter",
			"catégorie","affiliation","chargé d'affaire",
			"montant de l'échéance","nombre d'impayé",
			"échéance échus non payé","total à payer ce jours",
			"PAYEE"]
		wid_l = .12,.07,.12,.09,.09,.09,.09,.09,.09,.09,.06
		titre = self.imp_titre
		info = f'Date de paiement : {self.day1}<br/>'
		if self.charger:
			info += f"Chargé d'affaire : {self.charger}<br/>"

		if self.associa:
			info += f'Affiliation : {self.associa}<br/>'

		if self.status:
			info += f'Status : {self.status}<br/>'

		info += 'Agence TOKPOTA1'
		total_ent = ["montant de l'échéance","échéance échus non payé",
			"total à payer ce jours"]
		obj.Create_fact(wid_l,entete,liste,titre,info,total_ent)

	def up_th_tab(self):
		self.Up_tab(True)

	def set_charger(self,info):
		self.charger = info
		self.add_all()

	def set_associa(self,info):
		self.associa = info
		self.Up_tab()

	def set_status(self,info):
		self.status = info
		self.Up_tab()

	def Show_echeance(self,wid):
		if self.cmd_ident == wid.info:
			self.cmd_ident = str()
		else:
			self.cmd_ident = wid.info
		self.add_develop_surf()

	def set_client_name(self,wid,val):
		self.th_clt_name = val
		self.Up_tab()

class Ech_en_cours(Creances_ch):
	@Cache_error
	def add_ech_surf(self):
		self.ech_surf.clear_widgets()
		self.imp_titre = 'Liste des échéance en cours'
		h = .05
		"""
		self.ech_surf.add_text('Affiliation',text_color = self.sc.text_col1,
			size_hint = (.1,h))
		self.ech_surf.add_surf(liste_set(self,self.associa,
			self.sc.DB.Get_association_list(),size_hint=(.1,h),mult = 1.5,
			mother_fonc = self.set_associa))
		
		self.ech_surf.add_text("Chargé d'affaire",text_color = self.sc.text_col1,
			size_hint = (.1,h))
		self.ech_surf.add_surf(liste_set(self,self.charger,
			self.sc.get_all_charger(),size_hint = (.1,h),mult = 1.5,
			mother_fonc = self.set_charger))
		"""

		self.ech_surf.add_text_input('Nom du client',(.1,h),(.4,h),
			self.sc.text_col1, bg_color = self.sc.aff_col3,
			text_color = self.sc.text_col1,on_text = self.set_client_name,
			default_text = self.th_clt_name)
		self.ech_surf.add_icon_but(icon = 'printer',size_hint = (.2,h),
			text_color = self.sc.black,on_press = self.impression)
		

		self.Tab = Table(self,size_hint = (1,.85),bg_color = self.sc.aff_col3,
			exec_fonc = self.Show_echeance,exec_key = "N°",padding = dp(5),
			radius = dp(10))

		self.pied_surf = box(self,size_hint = (1,.1),padding = dp(10),
			spacing = dp(5),orientation = 'horizontal')
		self.ech_surf.add_surf(self.Tab)
		self.ech_surf.add_surf(self.pied_surf)
		self.Up_tab(new_date = True)

	def Up_mont_trie(self,clt_dic,ech):
		self.montant_du += ech.get('montant dû')
		self.montant_payer += ech.get('montant payé')
		self.montant_restant += ech.get('montant restant')

# Gestion des actions des boutons
	def set_charger(self,info):
		self.charger = info
		self.Up_tab()

class Histo_echeance(Creances_ch):
	def add_ech_surf(self):
		self.ech_surf.clear_widgets()
		self.imp_titre = 'Historiques des Créances'
		h = .05
		self.ech_surf.add_text(self.imp_titre,text_color = self.sc.text_col1,
			halign = 'center',size_hint = (.8,h),underline = True)
		self.ech_surf.add_icon_but(icon = 'printer',size_hint = (.2,h),
			text_color = self.sc.black,on_press = self.impression)

		self.ech_surf.add_surf(Periode_set(self,size_hint = (.3,h),
			exc_fonc = self.Up_tab))

		self.ech_surf.add_text('Affiliation',text_color = self.sc.text_col1,
			size_hint = (.08,h))
		self.ech_surf.add_surf(liste_set(self,self.associa,
			self.sc.DB.Get_association_list(),size_hint=(.1,h),
			mother_fonc = self.set_associa))
		
		self.ech_surf.add_text("Chargé d'affaire",text_color = self.sc.text_col1,
			size_hint = (.09,h))
		self.ech_surf.add_surf(liste_set(self,self.charger,
			self.sc.get_all_charger(),size_hint = (.1,h),
			mother_fonc = self.set_charger))

		self.ech_surf.add_text_input('Nom du client',(.09,h),(.15,h),
			self.sc.text_col1, bg_color = self.sc.aff_col3,
			text_color = self.sc.text_col1,on_text = self.set_client_name,
			default_text = self.th_clt_name)

		self.Tab = Table(self,size_hint = (1,.785),bg_color = self.sc.aff_col3,
			exec_fonc = self.Show_echeance,exec_key = "N°",padding = dp(5),
			radius = dp(10))

		self.pied_surf = box(self,size_hint = (1,.1),padding = dp(10),
			spacing = dp(5),orientation = 'horizontal')
		self.ech_surf.add_surf(self.Tab)
		self.ech_surf.add_surf(self.pied_surf)
		self.Up_tab(new_date = True)

	def add_pied_surf(self,lenf):
		self.pied_surf.clear_widgets()
		dic = {
			"Nombre total":lenf,
			"montant total à payé":self.all_imp,
			"montant total avancé":self.all_encour,
			"montant total restant":self.all_paye,
		}
		self.pied_surf.add_text('',size_hint = (.1,1))
		for k,v in dic.items():
			b = box(self,radius = dp(10),bg_color = self.sc.aff_col3, 
				padding = dp(5),size_hint = (.1,1))
			b.add_text_input(k,(1,1),(1,1),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col1,
				radius = dp(5),halign = 'center',text_halign = 'center',
				default_text = self.format_val(v),readonly= True)
			self.pied_surf.add_surf(b)
		self.pied_surf.add_text("",size_hint = (.1,1))

	def Up_tab(self,new_date = False):
		entete = ("date d'achat","Nom du client","N° à contacter",
			"catégorie","affiliation","chargé d'affaire",
			"Montant à payer","Montant avancé",
			"Montant restant",)
		wid_l = .15,.15,.1,.1,.1,.1,.1,.1,.1,
		liste = self.Trie_infos()
		self.Tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.075))

	def Trie_infos(self):
		liste = self._trie()
		self.add_pied_surf(len(liste))
		return liste

	def _trie(self):
		liste = list()
		all_cmd_dic = self.sc.DB.Get_cmd_non_sold()
		self.all_imp = float()
		self.all_encour = float()
		self.all_paye = float()
		for cmd_dic in all_cmd_dic.values():
			cmd = self.edite_cmd(cmd_dic)
			if cmd:
				liste.append(cmd)
		return liste

	@Cache_error
	def edite_cmd(self,cmd_dic):
		if cmd_dic.get('status de la commande') == "Livrée":
			cmd_dic = dict(cmd_dic)
			plan_paie = cmd_dic.get("plan de paiements")
			date_liste = self.get_date_list(self.day1, self.day2)

			a_paye = float()
			paye = float()
			rest = float()
			for date in date_liste:
				date_info = plan_paie.get(date)
				if not date_info:
					pass

				elif date_info:
					a_paye += date_info.get('montant dû')
					paye += date_info.get('montant payé')
					rest += date_info.get('montant restant')
			if a_paye:
				cmd_dic["Montant à payer"] = a_paye
				cmd_dic["Montant avancé"] = paye
				cmd_dic["Montant restant"] = rest

				clt_dic = self.sc.DB.Get_this_clt(cmd_dic.get("client"))
				cmd_dic['affiliation'] = self.sc.DB.Get_this_association(
					clt_dic.get('association appartenue')).get('nom',str())

				if self.charger:
					if cmd_dic.get("chargé d'affaire").lower() != self.charger.lower():
						return None
				if self.associa:
					if cmd_dic.get('affiliation').lower() != self.associa.lower():
						return None
				if self.th_clt_name.lower() not in clt_dic.get('nom').lower():
					return None
				self.all_imp += a_paye
				self.all_encour += paye
				self.all_paye += rest
				return cmd_dic

# Gestion des actions des bouttons
	@Cache_error
	def impression(self,wid):
		obj = self.sc.imp_part_dic('Fiche')(self)
		liste = self.Trie_infos()
		entete = ["date d'achat","Nom du client","N° à contacter",
			"catégorie","affiliation","chargé d'affaire",
			"Montant à payer","Montant avancé",
			"Montant restant",]
		wid_l = .15,.15,.1,.1,.1,.1,.1,.1,.1,
		titre = self.imp_titre
		info = f'Période de paiement : du {self.day1} au {self.day2}<br/>'
		if self.charger:
			info += f"Chargé d'affaire : {self.charger}<br/>"

		if self.associa:
			info += f'Affiliation : {self.associa}<br/>'

		if self.status:
			info += f'Status : {self.status}<br/>'

		info += 'Agence TOKPOTA1'
		total_ent = ["Montant à payer","Montant avancé",
			"Montant restant"]
		obj.Create_fact(wid_l,entete,liste,titre,info,total_ent)

class th_Show_creance_surf(Show_creance_surf):
	def Close(self,wid):
		self.mother.close_modal()

