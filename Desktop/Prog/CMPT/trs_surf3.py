#Coding:utf-8
"""
	Troisième module de définition des objets surfaces utiliser
	au niveau de la trésorerie
"""
from lib.davbuild import *
from General_surf import *

class new_compte_surf(stack):
	@Cache_error
	def initialisation(self,default_height = .09,info_w = .3):
		self.def_height = default_height
		self.info_w = info_w
		
		self.size_pos()
		self.clear_widgets()
		compte = dict()
		self.add_text("Création d'un nouveau compte de Trésorerie",
			size_hint = (1,.04),text_color = self.sc.text_col1,
			underline = True,halign = 'center')
		self.type_cmpt = compte.get('type de compte',str())
		self.forme_cmpt = compte.get('forme de compte',str())
		self.manu_forme = str()
		self.createur = self.sc.get_curent_perso()
		self.devis = compte.get('devise',str())
		self.compte_info = compte
		self.compte_info['responsable de la création'] = self.createur

		self.add_text('Type de compte :',size_hint = self.info_size,
			text_color = self.sc.text_col1)
		self.add_surf(liste_set(self,self.type_cmpt,
			self.sc.mode_paie,size_hint = self.details_size,
			mother_fonc = self.set_type_compt, mult = 1))

		self.add_text('Libellé de compte :',size_hint = self.info_size,
			text_color = self.sc.text_col1)
		self.add_input("libellé",text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,on_text = self.set_cmpt_info,
			size_hint = self.details_size,placeholder = 'Libellé de compte')
		self.add_text('N° de compte :',size_hint = self.info_size,
			text_color = self.sc.text_col1)
		self.add_input('N° de compte',text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,on_text = self.set_cmpt_info,
			size_hint = self.details_size,placeholder = 'Numéro de compte')
		self.add_text('Institutions :',size_hint = self.info_size,
			text_color = self.sc.text_col1)
		if self.type_cmpt == 'banques':
			txt = "bancaire"
		else:
			txt = self.type_cmpt
		self.add_input('institutions',text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,on_text = self.set_cmpt_info,
			size_hint = self.details_size,placeholder = f'Institutions {txt}')

		self.add_text('Devis :',size_hint = self.info_size,
			text_color = self.sc.text_col1)
		self.add_surf(liste_set(self,self.devis,self.sc.devis_list,
			size_hint = (self.det_w*1.5,self.def_height),orientation = 'V',mult = 1,
			mother_fonc = self.change_devis))
		self.add_input('devis',placeholder = 'sauvegarder un dévis',
			text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
			on_text = self.set_manu_f_cmpt,default_text = self.devis,
			size_hint = self.det_size)
		self.add_button("+",size_hint = (self.det_w*.5,self.def_height),
			bg_color = None,bg_opact = 0,on_press = self.valid_manu_forme,
			info = 'devis',font_size = '35sp',text_color = self.sc.text_col1)

		self.add_surf(Periode_set(self,input_color = self.sc.aff_col3,
			exc_fonc = self.set_date,size_hint = (.7,self.def_height),
			one_part = True,info = "Date de création :",
			info_w = self.info_size[0],space = 0))
		self.add_padd((.3,.002))

		self.add_text('Solde à la création :',size_hint = self.info_size,
			text_color = self.sc.text_col1)
		self.add_input('solde initial',placeholder = "Premier dépot",
			text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
			on_text = self.set_cmpt_info,size_hint = self.details_size,
			padding_left = dp(10)
			)

		
		self.add_padd((.2,self.def_height))

		self.add_button('Créer le compte',size_hint = (.6,self.def_height),
			on_press = self.creer_compte,text_color = self.sc.text_col3,
			bg_color = self.sc.aff_col2,bg_opact = 0)
		self.info_surf = box(self,size_hint = (1,.1))
		self.add_surf(self.info_surf)
		self.add_basse()

	def add_basse(self):
		self.info_surf.clear_widgets()
		txt = self.error_text
		txt_col = self.sc.red
		if self.succes_text :
			txt = self.succes_text
			txt_col = self.sc.green
		self.info_surf.add_text(txt,halign = "center",
			text_color = txt_col,valign = 'top',
			strip = True,shorten = False)
		self.error_text = str()
		self.succes_text = str()

	def size_pos(self):
		self.details_w = 1-self.info_w
		self.info_size = self.info_w,self.def_height
		self.details_size = self.details_w,self.def_height
		self.det_w = self.details_w/5
		self.det_size = self.det_w*3,self.def_height

# Méthode d'action des buttons
	def set_date(self):
		self.compte_info['date de création'] = self.day1
	
	@Cache_error
	def creer_compte(self,wid):
		mini = {
			"libellé":str(),
			"type de compte":str(),
			"institutions":str(),
			"N° de compte":str(),
			"devise":str(),
			"solde initial":float(),
			"date de création":str(),
			"responsable de la création":str()
		}
		mini = {i:self.compte_info[i] for i in mini.keys()}
		if self.check(mini):
			self.compte_info['solde actuel'] = mini['solde initial']
			self.excecute(self.sc.DB.Save_compte,self.compte_info)
			#self.sc.DB.Save_compte(self.compte_info)
			self.initialisation(default_height = self.def_height,
				info_w = self.info_w)
			self.succes_text = "Enrégistrer avec succès"
			self.sc.add_refused_error("Un nouveau compte de Trésorerie vient d'être Enrégistrer dans la base")
		else:
			self.sc.add_refused_error('Toutes les informations sont obligatoires')
			self.error_text = 'Information non complète'
		self.mother.close_modal()
		self.add_basse()
	
	def set_createur(self,info):
		if self.createur:
			self.createur = str()
		else:
			self.createur = info
		self.compte_info['responsable de la création'] = self.createur

	def set_type_compt(self,info):
		if self.type_cmpt:
			self.type_cmpt = str()
		else:
			self.type_cmpt = info

		self.compte_info['type de compte'] = self.type_cmpt

	def change_forme(self,info):
		if self.forme_cmpt:
			self.forme_cmpt = str()
		else:
			self.forme_cmpt = info
		self.compte_info['forme de compte'] = self.forme_cmpt

	def change_devis(self,info):
		if self.devis:
			self.devis = str()
		else:
			self.devis = info
		self.compte_info["devise"] = self.devis

	def valid_manu_forme(self,wid):
		if wid.info == "N_forme":
			self.compte_info["forme de compte"] = self.manu_forme
			if self.manu_forme not in self.sc.forme_compt:
				self.sc.forme_compt.append(self.manu_forme)
		elif wid.info == 'devis':
			self.compte_info["devis"] = self.devis
			if self.devis not in self.sc.devis_list:
				self.sc.devis_list.append(self.devis)

	def set_cmpt_info(self,wid,val):
		if wid.info == "solde initial":
			wid.text = self.regul_input(wid.text)
		self.compte_info[wid.info] = wid.text

	def set_manu_f_cmpt(self,wid,val):
		if wid.info == 'N_forme':
			self.manu_forme = val
		elif wid.info == "devis":
			self.devis = val

class _list_surf_set(box):
	def __init__(self,mother,titre = 'encaissements',**kwargs):
		kwargs['padding'] = dp(10)
		kwargs['spacing'] = dp(5)
		box.__init__(self,mother,**kwargs)
		self.size_pos()
		self.mont_dict = {
			"Mont1":int(),
			"Mont2":int()
		}
		self.mode_paie = str()
		self.cmpt_paie = str()
		self.N_cmpt = str()
		self.agent = str()
		self.client = str()
		self.status = str()
		self.operateur = str()
		self.curent_typ = str() # Utiliser par le définisseur de surface

		self.entete_surf = stack(self,size_hint = self.entete_size,
			spacing = dp(5),padding = dp(10))
		self.corps_surf = Table(self,size_hint = self.corps_size,
			bg_color = self.sc.aff_col3)
		self.titre = f"Historique des {titre}"

		self.periode_surf = Periode_set(self,input_color = self.sc.aff_col3,
			exc_fonc = self.add_corps_surf,size_hint = (.5,.5),
			)
		self.add_surf(self.entete_surf)
		self.add_surf(self.corps_surf)

	@Cache_error
	def triage_complet(self,dicts):
		date_list = self.get_date_list(self.day1,self.day2)
		liste = [dicts.get(date) for date in date_list]
		L = list()
		for dic in liste:
			if dic:
				for i,d in dic.items():
					L.append(d)
		return [dic for dic in map(self.Trie,L) if dic]

	def Trie(self,dic):
		dic["mode de paiement"] = dic.get("mode de sortie")
		if self.operateur:
			if dic.get('opérateur').lower() != self.operateur.lower():
				return False
		num = dic.get('N°')
		if num:
			date,num = num.split('N°')[-1].split('_')
			d,m,y = date.split('-')
			num = f"{y}{m}{d}_{num}"
			dic['Numéro'] = num
		return dic

	def other_trie(self):
		self.other_surf.clear_widgets()
		liste = self.sc.get_moyen_paiement(self.mode_paie)
		if liste:
			self.other_surf.add_text('Moyen de paiement :',
				size_hint = (.14,1),text_color = self.sc.text_col1)
			self.other_surf.add_surf(liste_set(self,self.status,
				liste,size_hint = (.24,1),
				mother_fonc = self.set_status,mult = 1))
		self.other_surf.add_text('Agent :',size_hint = (.08,1),
			text_color = self.sc.text_col1)
		self.other_surf.add_surf(liste_set(self,self.agent,
			self.sc.get_devers_perso(),size_hint = (.24,1),
			mother_fonc = self.set_agent,mult = 1))

	@Cache_error
	def Foreign_surf(self):
		self.add_entete_surf()
		self.add_corps_surf()

	def size_pos(self):
		w,h = self.entete_size = 1,.1
		self.corps_size = w,1-h

	@Cache_error
	def add_entete_surf(self):
		self.entete_surf.clear_widgets()
		self.entete_surf.add_text(self.titre,size_hint = (.8,.45),
			text_color = self.sc.text_col1,halign = "center",
			underline = True)
		self.entete_surf.add_icon_but(icon ="printer",size_hint = (.1,.45),
			text_color = self.sc.black,info = 'IMP',on_press = self.impression)
		self.entete_surf.add_surf(self.periode_surf)
		self.entete_surf.add_text('Opérateur :',size_hint = (.12,.5),
			text_color = self.sc.text_col1)
		self.entete_surf.add_surf(liste_set(self,self.operateur,
			self.sc.get_devers_perso(),size_hint = (.3,.5),mult = 1,
			mother_fonc = self.set_operateur))

	def Get_this_list(self):
		...

# Méthode de gestion des actions au niveau des bouttons
	def set_operateur(self,info):
		self.operateur = info
		self.add_corps_surf()

	@Cache_error
	def impression(self,wid):
		obj = self.sc.imp_part_dic('Résumé')(self)
		entete = ['Numéro', 'date',"bénéficiaire","mode de paiement",
		"compte de sortie","compte bénéficiaires",
		'motif de décaissement',"montant décaissé"]
		wid_l = [.2,.11,.11,.11,.11,.12,.12,.12,]
		liste = self.Get_this_list()
		titre = f'Journal des Décaissements'
		info = f'Période : du {self.day1} au {self.day2}<br/>'
		if self.operateur:
			info += f'Opérateur : {self.operateur}<br/>'
		info += 'Agence TOKPOTA1'
		obj.Create_fact(wid_l,entete,liste,titre,info)

	def set_mont(self,wid,val):
		try:
			self.mont_dict[wid.info] = int(val)
		except ValueError:
			self.mother.error_text = "Montant non valide"
			self.mother.affiche_info()
		self.add_corps_surf()

	def mode_paie_set(self,info):
		if self.mode_paie:
			self.mode_paie = str()
			self.cmpt_paie = str()
			self.N_cmpt = str()
		else:
			self.mode_paie = info
		self.cmpte_trie()
		self.other_trie()
		self.add_corps_surf()

	def cmpt_paie_set(self,info):
		if self.cmpt_paie:
			self.cmpt_paie = str()
			self.N_cmpt = str()
		else:
			self.cmpt_paie = info
		self.cmpte_trie()
		self.add_corps_surf()

	def N_cmpt_paie_set(self,info):
		if self.N_cmpt:
			self.N_cmpt = str()
		else:
			self.N_cmpt = info
		self.cmpte_trie()
		self.add_corps_surf()

	def set_status(self,info):
		if self.status:
			self.status = str()
		else:
			self.status = info
		self.add_corps_surf()

	def set_agent(self,info):
		if self.agent:
			self.agent = str()
		else:
			self.agent = info
		self.add_corps_surf()

	def set_client(self,wid,val):
		self.client = val
		self.add_corps_surf()

class decaiss_surf(_list_surf_set):
	def __init__(self,mother,**kwargs):
		_list_surf_set.__init__(self,mother,
			titre = 'Décaissements',**kwargs)

	@Cache_error
	def add_corps_surf(self):
		liste = self.Get_this_list()
		entete = ['Numéro', 'date',"bénéficiaire","mode de paiement",
		"compte de sortie","compte bénéficiaires",
		'motif de décaissement',"montant décaissé",
		]
		wid_l = [.14,.12,.13,.12,.13,.12,.12,.12,]
		self.corps_surf.Creat_Table(wid_l,entete,liste,
			ent_size = (1,.065))

	def Get_this_list(self):
		date_list = self.get_date_list(self.day1, self.day2)
		liste = self.triage_complet(date_list)
		return liste

	@Cache_error
	def triage_complet(self,date_list):
		idents = list()
		for date in date_list:
			dic = self.sc.DB.Get_decaissements(date)
			idents.extend(dic.keys())
		return [i for i in map(self.Trie,idents) if i]

	def Trie(self,ident):
		dic = self.sc.DB.Get_this_decaissement(ident)
		if dic:
			return dic

		
class Trans_histo(_list_surf_set):
	def __init__(self,mother,**kwargs):
		_list_surf_set.__init__(self,mother,
			titre = "Transferts internes",**kwargs)
		self.mode_paie_e = str()
		self.cmpt_paie_e = str()
		self.N_cmpt_e = str()
		#self.add_all()

	@Cache_error
	def add_corps_surf(self):
		liste = self.triage_complet()
		entete = [i for i in transfert.keys()]
		wid_l = [1/len(entete)]*len(entete)
		self.corps_surf.Creat_Table(wid_l,entete,liste,
			ent_size = (1,.1))

	@Cache_error
	def triage_complet(self):
		liste = self.trie_par_date_et_type()
		liste = self.trie_par_montant(liste)
		liste = self.trie_par_mode_paie(liste)
		liste = self.trie_par_mode_paie_entrant(liste)
		liste = self.trie_par_agent(liste)
		liste = self.trie_client(liste)
		return liste

	def other_trie(self):
		self.other_surf.clear_widgets()
		self.other_surf.add_text('Mode de paiement entrant :',
			text_color = self.sc.text_col1,size_hint = (.2,1))
		self.other_surf.add_surf(liste_set(self,self.mode_paie_e,
			self.sc.virtual_mode,size_hint = (.175,1),
			mother_fonc = self.mode_paie_set_e,mult = 2))
		if self.mode_paie_e:
			cmpt_dict = self.sc.virtual_mode_dict.get(self.mode_paie_e,dict())
			liste = [i for i in cmpt_dict.keys()]
			self.other_surf.add_text('Compte entrant :',
				text_color = self.sc.text_col1,size_hint = (.08,1))
			self.other_surf.add_surf(liste_set(self,self.cmpt_paie_e,
				liste,size_hint = (.175,1),
				mother_fonc = self.cmpt_paie_set_e,mult = 2))
			if self.cmpt_paie_e:
				liste = [self.format_val(i) for i in cmpt_dict.get(self.cmpt_paie_e,list())]
				self.other_surf.add_text('N° de compte entrant :',
					text_color = self.sc.text_col1,size_hint = (.1,1))
				self.other_surf.add_surf(liste_set(self,self.N_cmpt_e,
					liste,size_hint = (.25,1),
					mother_fonc = self.N_cmpt_paie_set_e,mult = 1))

	def cmpte_trie(self):
		self.cmpt_surf.clear_widgets()
		self.cmpt_surf.add_text('Mode de paiement sortant:',
			text_color = self.sc.text_col1,size_hint = (.2,1))
		self.cmpt_surf.add_surf(liste_set(self,self.mode_paie,
			self.sc.virtual_mode,size_hint = (.175,1),
			mother_fonc = self.mode_paie_set,mult = 2))
		if self.mode_paie:
			cmpt_dict = self.sc.virtual_mode_dict.get(self.mode_paie,dict())
			liste = [i for i in cmpt_dict.keys()]
			self.cmpt_surf.add_text('Compte sortant :',
				text_color = self.sc.text_col1,size_hint = (.08,1))
			self.cmpt_surf.add_surf(liste_set(self,self.cmpt_paie,
				liste,size_hint = (.175,1),
				mother_fonc = self.cmpt_paie_set,mult = 2))
			if self.cmpt_paie:
				liste = [self.format_val(i) for i in cmpt_dict.get(self.cmpt_paie,list())]
				self.cmpt_surf.add_text('N° de compte sortant :',
					text_color = self.sc.text_col1,size_hint = (.1,1))
				self.cmpt_surf.add_surf(liste_set(self,self.N_cmpt,
					liste,size_hint = (.25,1),
					mother_fonc = self.N_cmpt_paie_set,mult = 1))

	def trie_par_date_et_type(self):
		date_list = self.get_date_list(self.day1,self.day2)
		liste = self.sc.DB.Get_transfert_list(date_list)
		return liste

	def trie_par_mode_paie(self,liste):
		L = list()
		for ope in liste:
			if self.mode_paie and ope["mode de paiement sortant"].lower() == self.mode_paie.lower():
				if self.cmpt_paie and ope['compte sortant'].lower() == self.cmpt_paie.lower():
					if self.N_cmpt and ope['N° compte sortant'].lower() == self.N_cmpt.lower():
						L.append(ope)
					elif not self.N_cmpt:
						L.append(ope)
				elif not self.cmpt_paie:
					L.append(ope)
			elif not self.mode_paie:
				L.append(ope)
		return L

	def trie_par_mode_paie_entrant(self,liste):
		L = list()
		for ope in liste:
			if self.mode_paie_e and ope["mode de paiement entrant"].lower() == self.mode_paie_e.lower():
				if self.cmpt_paie_e and ope['compte entrant'].lower() == self.cmpt_paie_e.lower():
					if self.N_cmpt_e and ope['N° compte entrant'].lower() == self.N_cmpt_e.lower():
						L.append(ope)
					elif not self.N_cmpt_e:
						L.append(ope)
				elif not self.cmpt_paie_e:
					L.append(ope)
			elif not self.mode_paie_e:
				L.append(ope)
		return L

	def trie_client(self,liste):
		L = [ope for ope in liste if self.client.lower() in ope["motif du transfert"].lower()]
		return L

# actions méthodes
	def mode_paie_set_e(self,info):
		if self.mode_paie_e:
			self.mode_paie_e = str()
			self.cmpt_paie_e = str()
			self.N_cmpt_e = str()
		else:
			self.mode_paie_e = info
		self.other_trie()
		self.add_corps_surf()

	def cmpt_paie_set_e(self,info):
		if self.cmpt_paie_e:
			self.cmpt_paie_e = str()
			self.N_cmpt_e = str()
		else:
			self.cmpt_paie_e = info
		self.other_trie()
		self.add_corps_surf()

	def N_cmpt_paie_set_e(self,info):
		if self.N_cmpt_e:
			self.N_cmpt_e = str()
		else:
			self.N_cmpt_e = info
		self.other_trie()
		self.add_corps_surf()

class add_type_compt(stack):
	def __init__(self,mother,txt_width = .15,
		val_wid = .1,info_h = 1,mult = 1.5,
		mother_fonc = None,**kwargs):
		stack.__init__(self,mother,**kwargs)
		self.mode_paie = mother.mode_paie
		self.cmpt_paie = mother.cmpt_paie
		self.N_cmpt = mother.N_cmpt
		self.txt_width = txt_width
		self.val_wid = val_wid
		self.info_h = info_h
		self.mult = mult
		self.mother_fonc = mother_fonc
		self.add_all()

	@Cache_error
	def Foreign_surf(self):
		self.clear_widgets()
		self.sc.Up_cmpt()
		self.add_text('Mode de paiement :', 
			size_hint = (self.txt_width,self.info_h),
			text_color = self.sc.text_col1)
		
		self.add_surf(liste_set(self,
			self.mode_paie,self.sc.virtual_mode,
			mother_fonc = self.set_mode_paie,
			size_hint = (self.val_wid,self.info_h),mult = self.mult))
		if self.mode_paie:
			compt_dict = self.sc.virtual_mode_dict.get(self.mode_paie)
			liste = [i for i in compt_dict.keys()]
			self.add_text('Comptes :', 
				size_hint = (self.txt_width,self.info_h),text_color = self.sc.text_col1)
			self.add_surf(liste_set(self,
				self.cmpt_paie,liste,mother_fonc = self.set_cmpt_paie,
				size_hint = (self.val_wid,self.info_h),mult = self.mult))
			if self.cmpt_paie:
				liste = compt_dict.get(self.cmpt_paie)
				self.add_text('N° de compte :', 
					size_hint = (self.txt_width,self.info_h),text_color = self.sc.text_col1)
				self.add_surf(liste_set(self,
					self.N_cmpt,liste,mother_fonc = self.set_n_cmpt_paie,
					size_hint = (self.val_wid,self.info_h),mult = self.mult))

# Gestion des actions des buttons
	def set_mode_paie(self,info):
		if self.mode_paie:
			self.mode_paie = str()
			self.cmpt_paie = str()
			self.N_cmpt = str()
		else:
			self.mode_paie = info
		self.mother.mode_paie = self.mode_paie
		self.mother.cmpt_paie = self.cmpt_paie
		self.mother.N_cmpt = self.N_cmpt
		if self.mother_fonc:
			self.mother_fonc(self)
		self.add_all()

	def set_cmpt_paie(self,info):
		if self.cmpt_paie:
			self.cmpt_paie = str()
			self.N_cmpt = str()
		else:
			self.cmpt_paie = info
		self.mother.cmpt_paie = self.cmpt_paie
		self.mother.N_cmpt = self.N_cmpt
		if self.mother_fonc:
			self.mother_fonc(self)
		self.add_all()

	def set_n_cmpt_paie(self,info):
		if self.N_cmpt:
			self.N_cmpt = str()
		else:
			self.N_cmpt = info
		self.mother.N_cmpt = self.N_cmpt
		if self.mother_fonc:
			self.mother_fonc(self)
		self.add_all()
