#Coding:utf-8
"""
	Surface de gestion des différentes forme de paiements et 
	d'entrées.
"""
from .trs_surf3 import add_type_compt
from lib.davbuild import *
from General_surf import *

class paiement_surf(stack):
	def __init__(self,mother,info_h_hint,obj_paie,montant,
		info_w = .3,mother_fonc = None,penalite = float(),**kwargs):
		stack.__init__(self,mother,**kwargs)
		self.ifh = info_h_hint
		self.mother_fonc = mother_fonc
		self.objet_de_paiement = obj_paie
		typ,cmpt,n_cmpt = self.sc.DB.Get_paie_preference()
		self.mode_paie = typ
		self.cmpt_paie = cmpt
		self.N_cmpt = n_cmpt
		self.montant = montant
		self.num_recevant = str()
		self.reference = str()
		self.deposant = "Lui même"
		self.info_w = info_w
		self.penalite = penalite

		self.modif_mont = False

		self.cmpt_infos_dict = self.sc.DB.Get_comptes_dict()
		self.reinit()

	@Cache_error
	def reinit(self):
		self.clear_widgets()
		self.cmpt_surf = add_type_compt(self,
			size_hint = (1,self.ifh*3),
			info_h = .33,val_wid = 1-(self.info_w+.1),
			txt_width = self.info_w+.01,mult = 1,
			mother_fonc = self.Save_last_part)
		self.add_surf(self.cmpt_surf)
		self.last_infos = stack(self,size_hint = (1,self.ifh*8),
			spacing = dp(10),)
		self.add_surf(self.last_infos)
		self.add_last_infos()

	@Cache_error
	def Save_last_part(self,wid):
		if self.N_cmpt:
			T = Thread(target = self.sc.DB.Save_paie_preference,
				args = (self.mode_paie,self.cmpt_paie,self.N_cmpt))
			T.start()
		self.add_last_infos()

	@Cache_error
	def add_last_infos(self):
		self.cmpt_infos_dict = self.sc.DB.Get_comptes_dict()
		self.last_infos.clear_widgets()
		if self.cmpt_surf.mode_paie == "espèces":
			self.reference = f"Reglement du {self.sc.get_today()}"
		dic = {
			"Montant : ":self.format_val(self.montant),
			"Id de la transaction : ":self.reference,
			"Déposant : ":self.deposant,
			'Numéro de dépot :':self.num_recevant,
		}
		if self.N_cmpt:
			for k,v in dic.items():
				self.last_infos.add_text_input(k,
					(self.info_w,.15),(.5,.15),
					self.sc.text_col1,
					bg_color = self.sc.aff_col3,
					text_color = self.sc.text_col1,
					on_text = self.set_infos,
					default_text = v)

			self.last_infos.add_padd((.25,.25))
			self.last_infos.add_button(
				'Valider le paiement',
				size_hint = (.5,.2),
				text_color = self.sc.text_col3,
				bg_color = self.sc.aff_col2,
				on_press = self.add_paie)

	@Cache_error
	def valide_paie(self,cmd_ident):
		client = self.mother.This_client
		if not client:
			self.sc.DB.sc.add_refused_error('Le client est obligatoire')
			return False
		else:
			solde_p = self.sc.DB.Get_this_clt_solde(client)
			if not solde_p:
				solde_p = float()
			dic = self.sc.DB.Get_paiement_format()
			dic['montant payé'] = self.montant
			dic['id commande'] = cmd_ident
			dic['client'] = client
			dic['mode de paiement'] = self.mode_paie
			dic['objet de paiement'] = self.objet_de_paiement
			dic['compte accrédité'] = self.cmpt_paie
			dic['N° de compte accrédité'] = self.N_cmpt
			dic['opérateur'] = self.sc.get_curent_perso()
			dic['déposant'] = self.deposant
			dic['solde précédent client'] = solde_p
			dic['solde finale client'] = solde_p-self.montant
			dic['pénalité'] = self.penalite
			self.th_vl(dic)
			return dic['id du paiement']

	@Cache_error
	def th_vl(self,dic):
		self.sc.DB.Save_paiement(dic)
		self.Save_ecriture(dic)

	@Cache_error
	def Save_ecriture(self,dic):
		ecrit_dic = self.sc.DB.Get_encaissement_form()
		ecrit_dic["mode d'entrée"] = self.mode_paie
		ecrit_dic["compte d'entrée"] = f"{self.cmpt_paie}(_){self.N_cmpt}"
		ecrit_dic['montant encaissé'] =float(self.montant)
		ecrit_dic['référence'] = dic["id commande"]
		ecrit_dic['id de la transaction'] = self.reference
		ecrit_dic["motif d'encaissements"] = dic['objet de paiement']
		ecrit_dic['origine'] = self.mother.This_client
		self.sc.DB.Save_encaissements(ecrit_dic)

# méthodes de gestion des actions
	def Set_last_part(self,wid):
		self.add_last_infos()

	@Cache_error
	def add_paie(self,wid):
		if not self.N_cmpt:
			self.sc.DB.sc.add_refused_error("Vous devez renseigner les informations du compte à accréditer")
		elif not self.montant:
			self.sc.DB.sc.add_refused_error("Le montant ne peut pas être null")
		elif not self.reference:
			self.sc.DB.sc.add_refused_error("La référence représente l'Id de la transaction. c'est obligatoire")
		elif not self.num_recevant:
			self.sc.DB.sc.add_refused_error("Le numéro de la transaction es important")
		else:
			Conf_s = Confirmation(self,bg_color = self.sc.aff_col1)
			Conf_s.add_all(self.th_add_paie)
			self.add_modal_surf(Conf_s,size_hint = (.3,.3))

	@Cache_error
	def th_add_paie(self):
		cmd_ident = self.mother.Save_vente()
		if not cmd_ident:
			pass
		else:
			ret = self.valide_paie(cmd_ident)
			if ret:
				self.sc.add_refused_error(f"Le compte {self.N_cmpt} de {self.cmpt_paie} est accréditer de {self.montant}")
				self.sc.DB.Save_paiement_of_this(cmd_ident,ret,self.montant)
				
			self.mother.mother.add_all()

	def set_infos(self,wid,val):
		if "montant" in wid.info.lower():
			wid.text = self.regul_input(wid.text)
			if wid.text:
				self.montant = float(wid.text)
			else:
				self.montant = float()
	
		elif 'id de la' in wid.info.lower():
			self.reference = val

		elif "déposant" in wid.info.lower():
			self.deposant = val

		elif 'numéro de dépot' in wid.info.lower():
			self.num_recevant = val

class decaisse_paie(stack):
	def __init__(self,mother,height,motif,reference,back_fonc,
		montant = float(),modif_mont = False,mother_fonc = None,**kwargs):
	#
		stack.__init__(self,mother,**kwargs)
		self.th_h = height
		self.motif = motif
		self.back_fonc = back_fonc
		self.reference = reference
		self.montant = montant
		self.modif_mont = modif_mont
		self.reception = str()
		self.mother_fonc = mother_fonc

		self.cate_benef = str()
		self.cate_liste = ['Partenaires','Personnel',"Fournisseurs",
		"Déversements","Autres"]
		self.benef = str()
		self.id_paie = str()

		liste = self.sc.DB.Get_paie_preference()
		self.typ,self.cmpt,self.n_cmpt = liste
		self.mode_paie,self.cmpt_paie,self.N_cmpt = liste
		self.mode_recp = self.typ
		self.mode_recp_list = ['espèces','virtuelle','virement bancaire',
		"chèque bancaire"]
		if self.mode_recp not in self.mode_recp_list:
			self.mode_recp = str()

		self.init()

	@Cache_error
	def init(self):
		self.clear_widgets()
		self.add_text("Surface de décaissement",halign= 'center',
			text_color = self.sc.text_col1, size_hint = (.8,self.th_h),
			underline = True)
		if self.back_fonc:
			self.add_icon_but(icon = 'close',text_color = self.sc.red,
				on_press = self.back_fonc,size_hint = (.2,self.th_h))
		self.add_paie_info()
		self.parts()

	@Cache_error
	def Foreign_surf(self):
		self.init()

	@Cache_error
	def add_paie_info(self):
		self.cmpt_surf = add_type_compt(self,
			size_hint = (1,None),height = dp(120),
			info_h = .33,val_wid = .6,
			txt_width = .33,mult = 1,
			mother_fonc = self.Save_last_part)
		self.add_surf(self.cmpt_surf)
		self.parts_surf = stack(self,size_hint = (1,.7),spacing = dp(5))
		self.add_surf(self.parts_surf)

	@Cache_error
	def parts(self):
		self.parts_surf.clear_widgets()
		h = self.th_h + .01
		if self.n_cmpt:
			self.parts_surf.add_text('Catégorie de bénéficiaire',
				size_hint = (.3,h),text_color = self.sc.text_col1)
			self.parts_surf.add_surf(liste_set(self,self.cate_benef,
				self.cate_liste,size_hint = (.7,h),mult = 1,
				mother_fonc = self.set_cate_benef))
			if self.cate_benef:
				self.th_benf_liste = self.get_benef_list()
				self.parts_surf.add_text('Bénéficiaire',
					size_hint = (.3,h),text_color = self.sc.text_col1)
				if self.th_benf_liste == False:
					self.parts_surf.add_input("Bénéficiaire",size_hint = (.6,h),
						text_color = self.sc.text_col1, bg_color = self.sc.aff_col3,
						on_text = self.set_ben,default_text = self.benef)
				else:
					self.parts_surf.add_surf(liste_set(self,self.benef,
						self.th_benf_liste,size_hint = (.7,h),mult = 1,
						mother_fonc = self.set_benef))
				self.parts_surf.add_text_input('Receptionnaire',
					(.3,h),(.6,h),self.sc.text_col1,text_color = self.sc.text_col1,
					bg_color = self.sc.aff_col3,on_text = self.set_recep,
					default_text = self.reception)
			
				if self.cate_benef != 'Déversements':
					self.parts_surf.add_text('moyens de reception :',
						size_hint = (.3,h),text_color = self.sc.text_col1)
					self.parts_surf.add_surf(liste_set(self,self.mode_recp,
						self.mode_recp_list,size_hint = (.6,h),
						mother_fonc = self.set_mode_recp,mult = 1))
				else:
					self.mode_recp = "espèces"
				self.set_mode_recp_surf()
			
	@Cache_error	
	def get_benef_list(self):
		if self.cate_benef == 'Partenaires':
			return self.sc.DB.Get_all_partenaires_list()
		elif self.cate_benef == 'Fournisseurs':
			return self.sc.Get_fourn_list()
		elif self.cate_benef == 'Personnel':
			return self.sc.get_devers_perso()
		else:
			return False

	def set_mode_recp_surf(self):
		h = self.th_h + .01
		if self.mode_recp:
			if self.mode_recp == 'espèces':
				self.cmt_bene = "espèces"
			else:
				self.part_dic = {
					"institutions":str(),
					"numéro de compte":str(),
					"id de la transaction":str(),
				}
				for k,v in self.part_dic.items():
					self.parts_surf.add_text_input(k,(.3,h),(.6,h),self.sc.text_col1,
						text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
						on_text = self.set_part_info)

			self.parts_surf.add_text_input('montant',(.3,h),(.6,h),self.sc.text_col1,
				text_color = self.sc.text_col1, bg_color = self.sc.aff_col3,
				on_text = self.set_mont,readonly = not self.modif_mont,
				default_text = self.montant)
			self.parts_surf.add_padd((1,.02))
			
			self.parts_surf.add_button_custom("Valider le décaissement",
				self.valide_paie,size_hint = (.4,h),padd = (.3,h),
				text_color = self.sc.text_col1)

# Gestion des actions des bouttons
	@Cache_error
	def valide_paie(self,wid):
		if not self.reception:
			self.sc.add_refused_error('Le réceptionnaire est obligatoire')
			return False
		if not self.montant:
			self.sc.add_refused_error("Le montant ne peut être nul")
			return False
		if not self.benef:
			self.sc.add_refused_error('Le bénéficiaire est obligatoire')
			return False
		if self.mode_recp == "espèces":
			self.id_paie = 'dépôt à vue'
			self.cmt_bene = "espèces"
		elif self.mode_recp:
			self.cmt_bene = (self.part_dic.get("institutions") + 
				f"(_){self.part_dic.get('numéro de compte')}")
			self.id_paie = self.part_dic.get("id de la transaction")
		else:
			self.sc.add_refused_error("Le mode de reception n'est pas définie")
			return False

		Conf_s = Confirmation(self,bg_color = self.sc.aff_col1)
		Conf_s.add_all(self.th_valide_paie)
		self.add_modal_surf(Conf_s,size_hint = (.3,.3))

	@Cache_error
	def th_valide_paie(self):
		decaiss_for = self.sc.DB.Get_decaissement_form()
		decaiss_for["bénéficiaire"] = self.benef
		decaiss_for["type de bénéficiaires"] = self.cate_benef
		decaiss_for["compte bénéficiaires"] = self.cmt_bene
		decaiss_for["compte de sortie"] = self.cmpt+f"(_){self.n_cmpt}"
		decaiss_for["motif de décaissement"] = self.motif
		decaiss_for["référence"] = self.reference
		decaiss_for["montant décaissé"] = self.montant
		decaiss_for["mode de sortie"] = self.mode_paie
		decaiss_for["mode de reception"] = self.mode_recp
		decaiss_for["id de la transaction"] = self.id_paie
		self.excecute(self.sc.DB.Save_decaissement,decaiss_for)
		self.this_decaiss_info = decaiss_for
		if self.mother_fonc:
			self.mother_fonc(self)

	def set_part_info(self,wid,info):
		self.part_dic[wid.info] = info

	def set_recep(self,wid,info):
		self.reception = info

	def set_mode_recp(self,info):
		self.mode_recp = info
		self.parts()

	def set_mont(self,wid,info):
		wid.text = self.regul_input(wid.text)
		if wid.text:
			self.montant = float(wid.text)
		else:
			self.montant = float()

	def set_cate_benef(self,info):
		self.cate_benef = info
		self.parts()

	def set_benef(self,info):
		self.benef = info

	def set_ben(self,wid,info):
		self.benef = info

	def Save_last_part(self,wid):
		self.typ = self.cmpt_surf.mode_paie
		self.cmpt = self.cmpt_surf.cmpt_paie
		self.n_cmpt = self.cmpt_surf.N_cmpt
		self.parts()

class dever_paie(decaisse_paie):
	@Cache_error
	def th_valide_paie(self):
		decaiss_for = self.sc.DB.Get_decaissement_form()
		decaiss_for["bénéficiaire"] = "Compte général"
		decaiss_for["type de bénéficiaires"] = "Interne"
		decaiss_for["compte bénéficiaires"] = "Interne(_)CAISSE GENE"
		decaiss_for["compte de sortie"] = self.cmpt+f"(_){self.n_cmpt}"
		decaiss_for["motif de décaissement"] = f"Déversements du {self.sc.get_today()}"
		decaiss_for["montant décaissé"] = self.montant
		decaiss_for["mode de sortie"] = self.mode_paie
		decaiss_for["mode de reception"] = self.mode_paie
		decaiss_for["id de la transaction"] = str()
		self.excecute(self.sc.DB.Save_decaissement,
			decaiss_for,False)
		self.this_decaiss_info = decaiss_for
		if self.mother_fonc:
			self.mother_fonc(self)

	@Cache_error
	def valide_paie(self,wid):
		Conf_s = Confirmation(self,bg_color = self.sc.aff_col1)
		Conf_s.add_all(self.th_valide_paie)
		self.add_modal_surf(Conf_s,size_hint = (.3,.3))

		
