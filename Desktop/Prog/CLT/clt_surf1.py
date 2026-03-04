#Coding:utf-8
"""
	Gestion des surfaces concernant la gestion singulier des clients
"""
from lib.davbuild import *
from General_surf import *
from ..CMPT.Compt_surf import developpe_compt
from ..CMPT.general_obj2 import recouv_show
import sys

class commandes(box):
	@Cache_error
	def initialisation(self):
		if self.mother.access_dic == "all":
			self.access_liste = "all"
		else:
			self.access_liste = self.mother.access_dic.get('Commandes')
		
		self.this_client = self.mother.this_client
		self.orientation = 'horizontal'
		self.status = str()
		self.paie = str()
		self.status_list = self.sc.Get_cmd_typ_list()
		self.paie_list = self.sc.Get_cmd_status_list()
		self.cmd_to_develop = str()
		self.size_pos()

	def size_pos(self):
		w,h = self.liste_size = .35,1
		self.aff_size = 1-w,h

		self.liste_surf = stack(self,size_hint = self.liste_size,
			padding = dp(10),spacing = dp(5),radius = [0,0,dp(10),0],
			bg_color = self.sc.aff_col1)
		self.aff_surf = developpe_compt(self,size_hint = self.aff_size,
			padding = dp(10),spacing = dp(5),radius = [0,0,0,dp(10)],
			bg_color = self.sc.aff_col1)

		self.add_surf(self.liste_surf)
		self.add_text('',bg_color = self.sc.sep,
			size_hint = (None,1),width = dp(1))
		self.add_surf(self.aff_surf)
	
	@Cache_error
	def Foreign_surf(self):
		self.add_liste_surf()
		self.add_aff_surf()	

	def add_liste_surf(self):
		h = .038
		self.liste_surf.clear_widgets()
		self.liste_surf.add_text('Listes des commandes',size_hint = (1,h),
			text_color = self.sc.text_col1,halign = 'center',underline = True)
		

		dic = {
			"Status :":(self.status,self.status_list,self.set_status),
			"Paiements :":(self.paie,self.paie_list,self.set_paie)
		}
		for k,tup in dic.items():
			txt,liste,fonc = tup
			self.liste_surf.add_text(k,text_color = self.sc.text_col1,
				size_hint = (.27,h))
			self.liste_surf.add_surf(liste_set(self,txt,liste,mother_fonc = fonc,
				size_hint = (.7,h),mult = 1,))
		self.liste_surf.add_surf(Periode_set(self,size_hint = (.6,h),
			exc_fonc = self.up_cmd_tab,info_w = .2))
		self.cmd_tab = Table(self,size_hint = (1,.82),bg_color = self.sc.aff_col3,
			padding = dp(10),radius = dp(10),exec_fonc = self.show_cmd_details,
			exec_key = "id de la commande")
		self.liste_surf.add_surf(self.cmd_tab)
		self.up_cmd_tab()

	@Cache_error
	def up_cmd_tab(self):
		entete = ("date d'émission","montant TTC","status de la commande")
		wid_l = [.3,.3,.4,]
		liste = self.Trie_infos()
		self.cmd_tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.07))

	def Trie_infos(self):
		cmds = self.this_client.get('commandes',list())
		liste = [self.sc.DB.Get_this_cmd(cmd_ident) for cmd_ident in cmds]
		dates_listes = self.get_date_list(self.day1,self.day2)
		liste = [i for i in liste if i]
		liste = [j for j in liste if j.get("date d'émission").split('.')[0] in dates_listes]
		liste = [j for j in liste if self.status.lower() in j.get('status de la commande').lower()]
		liste = [j for j in liste if self.paie.lower() in j.get('status du paiement').lower()]
		return liste

	def add_aff_surf(self):
		self.aff_surf.cmd_ident = self.cmd_to_develop
		self.aff_surf.add_all()

# Gestion des actions des buttons
	def set_status(self,info):
		self.status = info
		self.up_cmd_tab()

	def set_paie(self,info):
		self.paie = info
		self.up_cmd_tab()

	@Cache_error
	def show_cmd_details(self,wid):
		if self.check_access("détails"):
			if wid.info == self.cmd_to_develop:
				self.cmd_to_develop = str()
			else:
				self.cmd_to_develop = wid.info
			self.add_aff_surf()

class paiements(commandes):
	recouv_to_developp = str()
	@Cache_error
	def initialisation(self):
		if self.mother.access_dic == "all":
			self.access_liste = "all"
		else:
			self.access_liste = self.mother.access_dic.get('Paiements')
		self.this_client = self.mother.this_client
		self.orientation = 'horizontal'
		self.status = str()
		self.paie = str()
		self.status_list = self.sc.Get_cmd_typ_list()
		self.paie_list = self.sc.Get_cmd_status_list()
		self.cmd_to_develop = str()
		self.size_pos()

	def size_pos(self):
		w,h = self.liste_size = .35,1
		self.aff_size = 1-w,h

		self.liste_surf = stack(self,size_hint = self.liste_size,
			padding = dp(10),spacing = dp(5),radius = [0,0,dp(10),0],
			bg_color = self.sc.aff_col1)
		self.aff_surf = recouv_show(self,size_hint = self.aff_size,
			padding = dp(5),spacing = dp(5),radius = [0,0,0,dp(10)],
			bg_color = self.sc.aff_col1)

		self.add_surf(self.liste_surf)
		self.add_text('',bg_color = self.sc.sep,
			size_hint = (None,1),width = dp(1))
		self.add_surf(self.aff_surf)

	def add_liste_surf(self):
		h = .038
		self.liste_surf.clear_widgets()
		self.liste_surf.add_text('Listes des paiements',size_hint = (1,h),
			text_color = self.sc.text_col1,halign = 'center',underline = True)
		self.liste_surf.add_surf(Periode_set(self,size_hint = (.6,h),
			exc_fonc = self.up_cmd_tab,info_w = .2))

		self.cmd_tab = Table(self,size_hint = (1,.91),bg_color = self.sc.aff_col3,
			padding = dp(10),radius = dp(10),exec_fonc = self.show_cmd_details,
			exec_key = "id du paiement")
		self.liste_surf.add_surf(self.cmd_tab)
		self.up_cmd_tab()

	def up_cmd_tab(self):
		entete = ("date de paiement","montant payé","solde finale client")
		wid_l = [.3,.3,.4,]
		liste = self.Trie_infos()
		self.cmd_tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.07))

	def Trie_infos(self):
		paies = self.this_client.get('paiements',list())
		paies = self.trie_paie(paies)
		liste = [self.sc.DB.Get_this_paie_info(paie_ident) for paie_ident in paies]
		dates_listes = self.get_date_list(self.day1,self.day2)
		liste = [j for j in liste if j.get("date de paiement") in dates_listes]
		return liste

	def trie_paie(self,liste):
		return [i for i in liste if i]

	def add_aff_surf(self):
		self.aff_surf.init(self.cmd_to_develop)
		self.aff_surf.add_all()

class contrat(box):
	@Cache_error
	def initialisation(self):
		self.orientation = "horizontal"
		self.clear_widgets()
		self.add_text("",size_hint = (.1,1))
		self.contrat_surf = stack(self,size_hint = (.8,1),
			padding = dp(10))
		self.add_surf(self.contrat_surf)
		self.add_text("",size_hint = (.1,1))
		self.this_client = self.mother.this_client
		self.type_contrat = str()
		self.typ_cont_list = ("Contrat de vente",
			"Formulaire de demande d'information",)

		self.add_contact_surf()

	@Cache_error
	def add_contact_surf(self):
		h = .045
		self.contrat_surf.clear_widgets()
		self.contrat_surf.add_text('Document a édité :',size_hint = (.2,h),
			text_color = self.sc.text_col1,)
		self.contrat_surf.add_surf(liste_set(self,self.type_contrat,
			self.typ_cont_list,mother_fonc = self.set_typ_cont,
			size_hint = (.8,h),mult = 1))
		self.cont_s = stack(self,size_hint = (1,.95),padding = dp(10),
			spacing = dp(10))
		self.contrat_surf.add_surf(self.cont_s)

		if self.type_contrat:
			self.add_clt_info()

	@Cache_error
	def add_clt_info(self):
		h = .05
		self.cont_s.clear_widgets()
		self.clt_infos = self.this_client.get('infos_document',dict())
		list_info = ("Num_client","date_enrégistrement","nom_client",
			"prénom_client","date_naissance","lieu_naissance","nationalité_client",
			"profession_client","maison_client","Ville_client","quartier_client",
			'numéro_client','whatsapp_client',"type_pièce_identité","num_pièce_identité",
			"date_de_délivrance","lieu_de_délivrance","date_expiration",)
		if not self.clt_infos:
			self.clt_infos["Num_client"] = self.this_client.get('N°')
			self.clt_infos["date_enrégistrement"] = self.this_client.get("date d'enregistrement")
			self.clt_infos["nom_client"] = self.this_client.get('nom')
			self.clt_infos["prénom_client"] = str()
			self.clt_infos['maison_client'] = self.this_client.get("maison")
			self.clt_infos['quartier_client'] = self.this_client.get("quartier")
			self.clt_infos['Ville_client'] = self.this_client.get("ville")
			self.clt_infos['numéro_client'] = self.this_client.get("tel")
			self.clt_infos['whatsapp_client'] = self.this_client.get("whatsapp")
		for k in list_info:
			v = self.clt_infos.get(k,str())
			self.cont_s.add_text_input(k,(.22,h),(.28,h),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				on_text = self.set_clt_infos,default_text = str(v))
		self.cont_s.add_padd((1,.00001))
		self.cont_s.add_button_custom("Suivant",self.save_clt_info,
			text_color = self.sc.text_col3,bg_color = self.sc.orange,
			size_hint = (.4,h),padd = (.3,h))

	@Cache_error
	def add_avaliseur_info(self):
		h = .05
		self.cont_s.clear_widgets()
		self.avaliseur_info = self.this_client.get('infos_avaliseur',dict())
		list_info = ("nom_avaliseur","prénom_avaliseur",'date_naissance_avaliseur',
			"lieu_naissance_avaliseur","nationalité_avaliseur","profession_avaliseur",
			"maison_avaliseur","ville_avaliseur","quartier_avaliseur","numéro_avaliseur",
			"whatsapp_avaliseur")
		for k in list_info:
			v = self.avaliseur_info.get(k,str())
			self.cont_s.add_text_input(k,(.22,h),(.28,h),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				on_text = self.set_avaliseur_infos,default_text = str(v))
		self.cont_s.add_padd((1,.00001))

		self.cont_s.add_button_custom("Suivant",self.save_avaliseur_info,
			text_color = self.sc.text_col3,bg_color = self.sc.orange,
			size_hint = (.4,h),padd = (.3,h))

	@Cache_error
	def Add_infos_comp(self):
		h = .05
		self.cont_s.clear_widgets()
		self.info_suplem = self.this_client.get('infos_compt_demande',dict())
		list_info = ("activité_client","Site_de_vente","besoin_client",
			"montant_vente","recette_client","revenu_mensuelle_client")
		txt = "information_complémentaire"
		for k in list_info:
			v = self.info_suplem.get(k,str())
			self.cont_s.add_text_input(k,(.22,h),(.28,h),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				on_text = self.set_infos_sup,default_text = str(v))
		self.cont_s.add_padd((1,.00001))
		self.cont_s.add_text('information_complémentaire',text_color = self.sc.text_col1,
			size_hint = (.3,h))
		self.cont_s.add_input("information_complémentaire",
			text_color = self.sc.text_col1,size_hint = (.6,h*6),
			on_text = self.set_infos_sup,bg_color = self.sc.aff_col3,
			multiline = True,
			default_text = self.info_suplem.get('information_complémentaire',str()))

		self.cont_s.add_button_custom("Valider",self.save_info_suple,
			text_color = self.sc.text_col3,bg_color = self.sc.orange,
			size_hint = (.4,h),padd = (.3,h))

# Gestion des actions des bouttons
	def set_clt_infos(self,wid,val):
		self.clt_infos[wid.info] = val

	def set_avaliseur_infos(self,wid,val):
		self.avaliseur_info[wid.info] = val

	def set_typ_cont(self,info):
		self.type_contrat = info
		self.add_contact_surf()

	def set_infos_sup(self,wid,val):
		self.info_suplem[wid.info] = val

	@Cache_error
	def save_clt_info(self,wid):
		self.this_client['infos_document'] = self.clt_infos
		self.excecute(self.sc.DB.Update_client,self.this_client)
		#self.sc.DB.Update_client(self.this_client)
		if self.type_contrat == "Formulaire de demande d'information":
			self.add_avaliseur_info()
	
	@Cache_error
	def save_avaliseur_info(self,wid):
		self.this_client['infos_avaliseur'] = self.avaliseur_info
		self.excecute(self.sc.DB.Update_client,self.this_client)
		#self.sc.DB.Update_client(self.this_client)
		if self.type_contrat == "Formulaire de demande d'information":
			self.Add_infos_comp()

	@Cache_error
	def save_info_suple(self,wid):
		self.this_client['infos_compt_demande'] = self.info_suplem
		self.excecute(self.sc.DB.Update_client,self.this_client)
		#self.sc.DB.Update_client(self.this_client)
		dic = dict()
		dic.update(self.clt_infos)
		dic.update(self.avaliseur_info)
		dic.update(self.info_suplem)
		fic = os.path.abspath(f"./media/{dic.get('nom_client')}.docx")
		try:
			self.sc.Generer_doxs(os.path.abspath("./media/DEMANDE.docx"),
				fic,dic)
			self.open_link(fic)
			self.sc.add_refused_error('Document généré')
			self.add_all()
		except:
			self.sc.add_refused_error('Vous avez un document word du même nom ouvert')

class histo_act_client(stack):
	@Cache_error
	def initialisation(self):
		h = .04
		self.padding = dp(10)
		self.spacing = dp(10)
		self.this_client = self.mother.this_client
		self.add_text("Historique d'actions du client",
			text_color = self.sc.text_col1,halign = 'center',
			underline = True,size_hint = (.6,h))
		self.add_surf(Periode_set(self,size_hint = (.33,h),
			exc_fonc = self.Trie_visite,info_w = .2))
		self.add_icon_but(icon = "printer",text_color = self.sc.black,
			on_press = self.impression,size_hint = (.05,h))
		self.ths_v_tab = Table(self,size_hint = (1,.95),
			bg_color = self.sc.aff_col3,padding = dp(10),
			radius = dp(10))
		self.add_surf(self.ths_v_tab)
		self.Trie_visite()

	def Trie_visite(self):
		wid_l = .2,.2,.2,.2,.2
		entete = "date","solde de départ","achats","paiements",'solde final'
		liste = self.get_histo_list()
		self.ths_v_tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.05))

	def get_histo_list(self):
		date_liste = self.get_date_list(self.day1,self.day2)
		all_histo = self.this_client.get('historique du solde',dict())
		liste = list()
		if all_histo:
			for date in date_liste:
				dic = all_histo.get(date)
				if dic:
					dic['date'] = date
					liste.append(dic)
		return liste

# Gestion des actions
	def impression(self,wid):
		...

