#Coding:utf-8
"""
	Module de définition de l'interface des parties clés de la trésorerie
	comptable
"""
from lib.davbuild import *
from General_surf import *
from .trs_surf3 import *
from ..CREAN.cre_all_use import paiem_surf
from .old1 import *
from .general_obj2 import encaiss_show,decaiss_show

class show_details(stack):
	def __init__(self,mother,**kwargs):
		kwargs['bg_color'] = mother.sc.aff_col1
		stack.__init__(self,mother,**kwargs)
		self.radius = dp(10)

	@Cache_error
	def initialisation(self):
		self.type_cmpt = str()
		self.spacing = dp(10)
		self.padding = dp(10)
		self.type_cmpt_list = ["espèces","virtuelles","bancaires"]
		self.etat = "actif"
		self.etat_list = "actif","non actif"
		self.size_pos()

	def size_pos(self):
		h = .05
		self.add_text("Comptes de Trésorerie interne",
			size_hint = (.95,h),text_color = self.sc.text_col1,
			halign = 'center',underline = True,font_size = "19sp")
		self.add_icon_but(icon = "plus",text_color = self.sc.green,
			on_press = self.add_new_cmpt,size_hint = (.05,h))

		self.add_text('Type de comptes :',size_hint = (.12,h),
			text_color = self.sc.text_col1,)
		self.add_surf(liste_set(self,self.type_cmpt,self.type_cmpt_list,
			size_hint = (.15,h),mother_fonc = self.set_type_cmpt))

		self.add_text('Etat :',size_hint = (.08,h),
			text_color = self.sc.text_col1,)
		self.add_surf(liste_set(self,self.etat,self.etat_list,
			size_hint = (.1,h),mother_fonc = self.set_etat))

		self.tab = Table(self,size_hint = (1,.94),exec_fonc = self.details_cmpt,
			exec_key = 'N°',bg_color = self.sc.aff_col3)
		self.add_surf(self.tab)
		self.up_tab()

	@Cache_error
	def up_tab(self):
		entete = ("N° d'ordre","date de création","type de compte","libellé",
			"institutions","N° de compte","état","solde actuel")
		wid_l = (.07,.13,.11,.125,.125,.11,.15,.08,.1)
		liste = self.Get_cmpt_list()
		self.tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.055), 
			force_tire = False)

	def Get_cmpt_list(self):
		cmpt_list = self.sc.DB.Get_comptes_dict().values()
		liste = [i for i in map(self.trie,cmpt_list) if i]
		liste.sort(key = itemgetter("solde actuel"),reverse = True)
		liste = self.apply_num_ordre(liste,key = "N° d'ordre")
		return liste
		
	def trie(self,dic):
		num = int(self.Get_real_num(dic.get("N°")))
		dic["Real_num"] = num
		dic["état"] = "actif" if dic.get('actif') else "non actif"

		if self.etat:
			if dic.get('état') != self.etat:
				return None
		if self.type_cmpt and len(self.type_cmpt) > 4:
			if self.type_cmpt.lower()[:3] not in dic.get("type de compte").lower():
				return None
		solde = dic.get('solde actuel')
		try:
			solde = int(solde)
		except:
			solde = 0
		dic['solde actuel'] = solde
		return dic

# Gestion des actions des bouttons
	@Cache_error
	def details_cmpt(self,wid):
		info = wid.info
		th_surf = Details_info(self,info,bg_color = self.sc.aff_col1,
			radius = dp(10))
		self.add_modal_surf(th_surf,size_hint = (.6,.7),titre = "Détails du compte",
			pos_hint = {"x":.24,"y":.15})

	def set_type_cmpt(self,info):
		self.type_cmpt = info
		self.up_tab()

	def set_etat(self,info):
		self.etat = info
		self.up_tab()

	def add_new_cmpt(self,wid):
		self.save_surf = new_compte_surf(self,
			padding = [dp(50),dp(10),dp(50),dp(10)],
			spacing = dp(10),bg_color = self.sc.aff_col1)
		self.add_modal_surf(self.save_surf,size_hint = (.4,.5),
			titre = 'Nouveau compte de Trésorerie')

class Details_info(stack):
	def __init__(self,mother,ident,**kwargs):
		self.cmpt_ident = ident
		self.compte_dict = mother.sc.DB.Get_this_compte(ident)
		self.mouvements = self.compte_dict.get('mouvements')
		self.ope_typ = str()
		self.ope_typ_list = "crédit",'débit'

		self.ope = str()
		#self.ope_list = (i.get("nom") for i in 
		#	mother.sc.DB.Get_all_perso().values())
		stack.__init__(self,mother,**kwargs)
		self.padding = dp(10)
		self.spacing = dp(10)

	@Cache_error
	def initialisation(self):
		h = .07
		info = self.Get_info_of(self.compte_dict)
		titre = f"Journal de mouvement du compte {info}"
		self.add_text(titre,size_hint = (.8,h),text_color = self.sc.text_col1,
			halign = 'center',underline = True,font_size = "18sp")
		self.add_button_custom('Modifier les infos',self.modif_compt,
			size_hint = (.15,h),text_color = self.sc.aff_col1)
		self.add_surf(Periode_set(self,size_hint = (.4,h),exc_fonc = self.Up_tab))
		dic = {
			"Type d'opération":(self.ope_typ,self.ope_typ_list,
				self.set_ope_typ),
			#"Opérateur":(self.ope,self.ope_list,self.set_ope)
		}
		for info,tup in dic.items():
			txt,lis,fonc = tup
			self.add_text(info,text_color = self.sc.text_col1,
				size_hint = (.15,h))
			self.add_surf(liste_set(self,txt,list(lis),
				mother_fonc = fonc,size_hint = (.25,h),mult = 1))

		self.Tab = Table(self,size_hint = (1,.9),bg_color = self.sc.aff_col3,
			exec_key = "N°",exec_fonc = self.show_mouv)
		self.add_surf(self.Tab)
		self.Up_tab()

	@Cache_error
	def Up_tab(self):
		date_liste = self.get_date_list(self.day1,self.day2)
		mouv_list = self.sc.DB.Get_mouvs_of(self.cmpt_ident,date_liste)
		entete = ("date","recettes",'dépenses',"solde final")
		mouv_list = [i for i in map(self.trie,mouv_list) if i]
		mouv_list.sort(key = itemgetter('Numéro'),
			reverse = True)

		wid_l = (.05,.1,.1,.1,.1,.1,.15,.1,.1,.1)
		mouv_list = self.apply_num_ordre(mouv_list,key = "N° d'ordre")
		self.Tab.Creat_Table(wid_l,entete,mouv_list,ent_size = (1,.09))

	def trie(self,dic):
		d,m,y = dic.get('date').split('-')
		num = int(f'{y}{m}{d}')
		dic["Numéro"] = num
		return dic

	def Get_info_of(self,dic):
		lib = dic.get("libellé")
		typ = dic.get("type de compte")
		ins = dic.get('institutions')
		num = dic.get('N° de compte')
		info = f"{lib} ({typ}: {ins} <{num}>)"
		return info

# Gestion des actions des bouttons
	@Cache_error
	def modif_compt(self,wid):
		obj = Modif_cmpt(self,bg_color = self.sc.aff_col1,
			radius = dp(10))
		self.add_modal_surf(obj,size_hint = (.4,.45),
			titre = 'Modification des informations du compte')

	def show_mouv(self,wid):
		ref = wid.info
		if ref:
			dic = self.sc.DB.Get_this_mouve(ref)
			self.recouv_to_developp = dic.get('référence')
			self.mouvement = dic
			obj = encaiss_show(self,radius = dp(10),
				bg_color = self.sc.aff_col1,
				padding = dp(10),spacing = dp(10))

			if obj.paie_dict:
				self.add_modal_surf(obj,size_hint = (.8,.9),
					titre = "Affichage de l'encaissement")
			else:
				obj = decaiss_show(self,radius = dp(10),
					bg_color = self.sc.aff_col1,
					padding = dp(10),spacing = dp(10))
				if obj.paie_dict:
					self.add_modal_surf(obj,size_hint = (.4,.45),

					titre = "Affichage du décaissement")
				else:
					self.sc.add_refused_error('Référence du paiement non valide')
		else:
			self.sc.add_refused_error('Référence du paiement non trouvé')

	def set_ope_typ(self,info):
		self.ope_typ = info
		self.Up_tab()

	def set_ope(self,info):
		self.ope = info
		self.Up_tab()

class Modif_cmpt(stack):

	@Cache_error
	def initialisation(self):
		h = .1
		self.padding = dp(10)
		self.spacing = dp(10)
		self.add_text("Modification des informations du compte",
			text_color = self.sc.text_col1, size_hint = (1,h),
			halign = 'center',underline = True,font_size = '18sp')

		self.cmpt_info = self.mother.compte_dict
		self.info_dic = {
			"libellé":self.cmpt_info.get('libellé'),
			"institutions":self.cmpt_info.get('institutions'),
			"N° de compte":self.cmpt_info.get('N° de compte'),
			"devise":self.cmpt_info.get('devise'),
		}
		self.etat = "actif"
		if not self.cmpt_info.get('actif'):
			self.etat = 'non actif'
		for k,v in self.info_dic.items():
			self.add_padd((.2,h))
			self.add_text_input(k,(.25,h),(.35,h),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				on_text = self.modif_info,default_text = str(v))
			self.add_padd((.2,h))
		self.add_padd((.2,h))
		self.add_text("Etat du compte",text_color = self.sc.text_col1,
			size_hint = (.25,h))
		self.add_surf(liste_set(self,self.etat,("actif",'non actif'),
			mult = 1,size_hint = (.35,h),mother_fonc = self.set_actif,
			))
		self.add_button_custom('Modifier les infos',self.modif_inf,
			size_hint = (.5,h),padd = (.25,h),text_color = self.sc.aff_col1)

	@Cache_error
	def modif_inf(self,wid):
		if self.check(self.info_dic):
			self.cmpt_info.update(self.info_dic)
			self.sc.DB.Update_this_compte(self.cmpt_info)
			self.mother.close_modal()
		else:
			self.sc.add_refused_error("Les informations sont obligatoires")

	def modif_info(self,wid,val):
		self.info_dic[wid.info] = val

	def set_actif(self,info):
		self.etat = info
		if self.etat == 'actif':
			self.cmpt_info['actif'] = True
		else:
			self.cmpt_info['actif'] = False

from Mobile.Prog.CMPT.trs_surf2 import (Decaissement_surf, 
	finance_histo, decaiss_surf, encaiss_srf)

class decaissement(box):
	def initialisation(self):
		self.size_pos()

	def size_pos(self):
		decaiss_srf = Decaissement_surf(self,size_hint = (.4,.6),
			pos_hint = (.3,.3),bg_color = self.sc.aff_col3,
			radius = dp(10),padding = dp(10))
		decaiss_srf.add_all()
		self.add_text("",size_hint = (1,.2))
		self.add_surf(decaiss_srf)
		self.add_text("",size_hint = (1,.2))

class desk_finance_histo(finance_histo):
	def size_pos(self):
		self.padding = [dp(250),dp(20),dp(250),dp(20)]
		self.spacing = dp(10)
		self.hist_size = (1,.9)
		self.curent_surf = encaiss_srf(self,
			size_hint = self.hist_size)
	
	def add_entete_part(self):
		h = .04
		self.add_surf(Periode_set(self,size_hint = (.4,h),
			exc_fonc = self.trie_this_curent))
		self.add_text('Mouvement ',size_hint = (.1,h))
		self.add_surf(liste_set(self,self.th_part,
			['recettes','dépenses'],
			mother_fonc = self.choose_mouv,
			size_hint = (.2,h)))


	"""
	def __init__(self,mother,**kwargs):
		kwargs['orientation'] = "horizontal"
		kwargs['spacing'] = dp(1)
		box.__init__(self,mother,**kwargs)
		self.size_pos()

		self.motif = str()
		self.benef = str()
		self.mode_paie = str()
		self.cmpt_paie = str()
		self.N_cmpt = str()
		self.moyen_paie = str()
		self.ident_paie = str()
		self.montant = int()
		self.part1_surf = Decaissement_surf(self,size_hint = self.part1_size,
			spacing = dp(10),padding = dp(10),radius = [dp(10),0,0,dp(10)],
			bg_color = self.sc.aff_col1)
		self.part2_surf = decaiss_surf(self,radius = [0,dp(10),dp(10),0],
			padding = dp(10),size_hint = self.part2_size,
			bg_color = self.sc.aff_col1,)
		self.part2_surf.add_all()
		if "écritures" in self.sc.DB.Get_access_of('Décaissements'):
			self.add_surf(self.part1_surf)
			self.add_text("",size_hint = (None,1),width = dp(1),
			bg_color = self.sc.sep)
		self.add_surf(self.part2_surf)

	def size_pos(self):
		w,h = self.part1_size = .3,1
		self.part2_size = 1-w,h

	"""

class liste_ecriture(stack):
	def __init__(self,mother,**kwargs):
		kwargs['bg_color'] = mother.sc.aff_col1
		kwargs["padding"] = dp(10)
		kwargs["radius"] = dp(10)
		stack.__init__(self,mother,**kwargs)
		self.day1 = self.sc.day1
		self.day2 = self.sc.day2
		self.operateur = str()
		self.lettrage = str()
		self.typ_ope = str()
		self.motif = str()

		self.Alle_pe = dict()

	@Cache_error
	def Foreign_surf(self):
		self.clear_widgets()
		self.add_entete_surf()

	@Cache_error
	def add_entete_surf(self):
		h = .04
		self.add_text('Historique des opérations financiers en général',
			text_color = self.sc.text_col1,size_hint = (.9,h),
			halign = 'center',underline = True)
		self.add_icon_but(icon = 'printer',text_color = self.sc.black,
			on_press = self.Impression,size_hint = (.05,h))
		self.add_surf(Periode_set(self,size_hint = (.4,h),exc_fonc = self.add_corps_surf,
			info = 'Période des opérations :',info_w = .3))
		self.add_padd((.1,h))
		self.add_text_input('Tier par motifs :',(.1,h),(.3,h),self.sc.text_col1,
			text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
			on_text = self.set_motif_info,default_text = self.motif,
			placeholder = 'Motifs ici')
		dic = {
			"Trier par type d'opérations :":[self.typ_ope,['débit','crédit'],self.set_type],
			"Trier par opérateur :":[self.operateur,self.sc.get_devers_perso(),self.set_ope]
		}
		for k,tup in dic.items():
			self.add_text(k,text_color = self.sc.text_col1,
				size_hint = (.15,h))
			txt,lis,fonc = tup
			self.add_surf(liste_set(self,txt,lis,mother_fonc = fonc,
				size_hint = (.23,h),mult = 1))
			self.add_padd((.1,h))

		self.corps_surf = Table(self,size_hint = (1,.88),
			bg_color = self.sc.aff_col3,padding = dp(10),
			radius = dp(10))
		self.add_surf(self.corps_surf)
		self.add_corps_surf()
	
	@Cache_error
	def add_corps_surf(self):
		liste = self.Triage_operation()
		entete_l = ["N",'date et heure',"motif",'référence',
			"débit","crédit","opérateur","mode de paiement",
			"info du compte","solde après opération"]
		width_l = [.04,.12,.12,.12,.1,.1,.1,.1,.1,.1]
		self.corps_surf.Creat_Table(width_l,entete_l,
			liste,ent_size = (1,.065),ligne_h = .07)

	@Cache_error
	def Triage_operation(self):
		date_list = self.get_date_list(self.day1,self.day2)
		self.NUM = 0
		liste = self.sc.DB.Get_mouvs_dict(date_list).values()
		liste = [i for i in map(self.Trie_info,liste) if i]
		return liste

	def Trie_info(self,dic):
		if not dic:
			return dict()
			
		if self.motif:
			if self.motif.lower() not in dic.get('motif').lower():
				return False
		if self.typ_ope:
			if not dic.get(self.typ_ope):
				return False
		if self.operateur:
			if not dic.get('opérateur').lower() != self.operateur.lower():
				return False
		self.NUM += 1
		ref = dic.get('référence')
		cmp_n = dic.get('N° Compte')
		cmpt_d = self.sc.DB.Get_this_compte(cmp_n)
		mode = cmpt_d.get('type de compte')
		inst = cmpt_d.get('institutions')
		n = cmpt_d.get('N° de compte')
		NN = inst+f" ({n})"
		dic['info du compte'] = NN
		dic['mode de paiement'] = mode
		dic['solde après opération'] = dic.get('solde final')
		dic['date et heure'] = dic.get('date')+'\n'+dic.get('heure')
		dic['N'] = self.NUM
		return dic

# Méthode de gestion des actions des boutons
	@Cache_error
	def Impression(self,wid):
		# Définition de la méthode d'impression et d'envoie de la corps_surf
		obj = self.sc.imp_part_dic('Résumé')(self)
		liste = self.Triage_operation()
		entete = ['date et heure',"motif",'référence',
		"débit","crédit","opérateur","mode de paiement",
		"info du compte","solde après opération"]
		wid_l = [.17,.11,.11,.11,.1,.1,.1,.1,.1]
		titre = 'Journal des entrées et sorties financiers'
		info = f'Période : du {self.day1} au {self.day2}<br/>'
		if self.typ_ope:
			info += f"Type d'opération : {self.typ_ope}<br/>"
		if self.operateur:
			info += f'Opérateur : {self.operateur}<br/>'
		if self.motif:
			info += f"Motifs : {self.motif}<br/>"
		
		info += 'Agence TOKPOTA1'
		obj.Create_fact(wid_l,entete,liste,titre,info)
	

	def set_type(self,info):
		self.typ_ope = info
		self.add_corps_surf()

	def set_ope(self,info):
		self.operateur = info
		self.add_corps_surf()

	def set_motif_info(self,wid,val):
		self.motif = val
		self.add_corps_surf()

class encaiss_en_attente(box):
	def initialisation(self):
		self.orientation = 'horizontal'
		self.n_encais = "Non encaissé"
		self.padding = dp(1)
		self.spacing = dp(1)
		self.encaisse_liste = "Non encaissé","Déjà encaissé"
		self.size_pos()

	def size_pos(self):
		w,h = self.fact_n_encai_size = .7,1
		self.hist_part_size = 1-w,h

		self.fact_n_surf = stack(self,size_hint = self.fact_n_encai_size,
			padding = dp(10), spacing = dp(5),bg_color = self.sc.aff_col1,
			radius = [dp(10),0,0,dp(10)])
		self.histo_surf = stack(self,size_hint = self.hist_part_size,
			padding = dp(10), spacing = dp(15),bg_color = self.sc.aff_col1,
			radius = [0,dp(10),dp(10),0])

		self.add_surf(self.fact_n_surf)
		self.add_text("",size_hint = (None,1),width = dp(1),
			bg_color = self.sc.sep)
		self.add_surf(self.histo_surf)

	@Cache_error
	def Foreign_surf(self):
		self.add_fact_n_surf()
		self.add_histo_surf()

	@Cache_error
	def add_fact_n_surf(self):
		h = .04
		self.fact_n_surf.clear_widgets()
		self.fact_n_surf.add_text('Encaissements des factures',text_color = self.sc.text_col1,
			halign = 'center',size_hint = (.8,h),underline = True,font_size = '18sp')
		self.fact_n_surf.add_icon_but(icon = 'printer',text_color = self.sc.black,
			size_hint = (None,h),size = (dp(50),dp(50)),on_press = self.impression)
		self.fact_n_surf.add_surf(Periode_set(self,size_hint = (.4,h),
			exc_fonc = self.set_periode))

		self.fact_n_surf.add_text("nature d'encaissement :",text_color = self.sc.text_col1,
			size_hint = (.2,h))
		self.fact_n_surf.add_surf(liste_set(self,self.n_encais,self.encaisse_liste,
			size_hint = (.4,h),mult = 1,mother_fonc = self.set_n_encaisse))

		self.tab = Table(self,size_hint = (1,.9),exec_fonc = self.show_cmd,
			exec_key = "id de la commande",bg_color = self.sc.aff_col3,
			padding = dp(10))
		self.fact_n_surf.add_surf(self.tab)
		self.Up_table()

	@Cache_error
	def add_histo_surf(self):
		h = .05
		self.histo_surf.clear_widgets()
		self.histo_surf.add_text('Résumé générique',size_hint = (1,h),
			text_color = self.sc.text_col1,halign = 'center',font_size = "18sp",
			underline = True)
		for k,v in self.get_infos().items():
			self.histo_surf.add_text_input(f'{k} :',(.5,h),(.45,h),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				default_text = self.format_val(v),readonly = True)

	@Cache_error
	def Up_table(self):
		entete = ("date d'émission","Nom du client","montant réel"
			,'autres montants',
			"montant payé","nature d'encaissement","auteur")
		wid_l = (.16,.18,.12,.12,.12,.12,.12)
		liste = self.Trie_cmd()
		self.tab.Creat_Table(wid_l,entete,liste,
			ent_size = (1,.075),)

	def Trie_cmd(self):
		periode = self.get_date_list(self.day1,self.day2)
		liste_cmd = self.sc.DB.Get_factures_enc(periode)
		liste_cmd = [i for i in filter(self.trie_gene,liste_cmd)]
		return liste_cmd

	def get_infos(self):
		periode = self.get_date_list(self.day1,self.day2)
		liste_cmd = self.sc.DB.Get_factures_enc(periode)
		liste_encais = [i for i in filter(lambda cmd: True if 
			cmd.get("nature d'encaissement","Non encaissé") == 'Déjà encaissé'
			else False, liste_cmd)]

		liste_n_encais = [i for i in filter(lambda cmd: True if 
			cmd.get("nature d'encaissement","Non encaissé") == 'Non encaissé'
			else False, liste_cmd)]

		mont_comptant = float()
		mont_credit = float()
		if liste_encais:
			mont_comptant = sum([cmd.get("montant TTC") for cmd in liste_encais 
				if cmd.get('status de la facture') == 'Comptant'])
			mont_credit = sum([cmd.get("montant TTC") for cmd in liste_encais 
				if cmd.get('status de la facture',"Crédit") == 'Crédit'])
		dic = {
			"Factures total encaissé":len(liste_encais),
			"Factures total non encaissé":len(liste_n_encais),
			'Montant des factures au comptant':mont_comptant,
			'Montant des factures au crédit':mont_credit,
		}
		return dic

	def trie_gene(self,cmd):
		if self.n_encais:
			if self.n_encais.lower() != cmd.get("nature d'encaissement",'Non encaissé').lower():
				return False
		return True

	def def_encaise_set(self,cmd_ob):
		h = .1
		self.surf_encai = stack(self,padding = [dp(50),dp(10),dp(10),dp(10)], spacing = dp(10),
			bg_color = self.sc.aff_col1)
		self.mode_enc = "Comptant"
		mode_liste = 'Comptant','Crédit'

		if cmd_ob.get("nature d'encaissement","Non encaissé") == "Déjà encaissé":
			self.surf_encai.add_text(f"""La commande {cmd_ob.get('id de la commande')} à
				déjà été encaissé et placé au {cmd_ob.get('status de la facture')}""",
				text_color = self.sc.black,halign = 'center',size_hint = (1,.8),
				font_size = '20sp')
		else:
			self.surf_encai.add_text("mode d'encaissement :",size_hint =(.3,h),
				text_color = self.sc.text_col1,padding_left = dp(10))
			self.surf_encai.add_surf(liste_set(self,self.mode_enc,mode_liste,size_hint = (.6,h),
				mult = 1,mother_fonc = self.set_encaisse_mode))
			self.Aff_s = stack(self,size_hint = (1,.8))
			self.surf_encai.add_surf(self.Aff_s)
			self.aff_paiement_part()

		self.add_modal_surf(self.surf_encai,size_hint = (.5,.5),
			titre = f"Encaissement de la facture {cmd_ob.get('id de la commande')}")

	@Cache_error
	def aff_paiement_part(self):
		self.Aff_s.clear_widgets()
		if self.cmd_dict:
			if self.mode_enc == 'Comptant':
				mont_p = self.cmd_dict.get('montant TTC') - self.cmd_dict.get('montant payé')
				plan_d = self.cmd_dict.get("plan de paiements")
				if not plan_d:
					plan_d = {
						self.sc.get_today():{
							"montant dû":self.cmd_dict.get('montant TTC'),
							"montant payé":float(),
							"date":self.sc.get_today(),
							"montant restant":self.cmd_dict.get('montant TTC'),
							"paiement associé":list()}
					}
				date = [d for d in plan_d.keys()][0]
				self.This_client = self.cmd_dict.get('client')
				self.cmd_ident = self.cmd_dict.get("N°")
				self.paie_surf_ob = this_paie_dict(self,
				.08,date,mont_p,size_hint = (1,1),padding = dp(10))
				self.Aff_s.add_surf(self.paie_surf_ob)
			elif self.mode_enc == 'Crédit':
				self.Aff_s.add_padd((.3,.14))
				self.Aff_s.add_button('Valider au crédit',size_hint = (.4,.14),
					on_press = self.Save_credit)
			else:
				pass
	
# Gestion des actions de commandes
	def set_encaisse_mode(self,info):
		self.mode_enc = info
		self.aff_paiement_part()

	def Save_vente(self):
		mont_p = self.cmd_dict.get('montant TTC') - self.cmd_dict.get('montant payé')
		self.cmd_dict['status de la facture'] = 'Comptant'
		self.cmd_dict["nature d'encaissement"] = "Déjà encaissé"
		#self.excecute(self.sc.DB.Modif_this_cmd,self.cmd_dict)
		self.sc.DB.Modif_this_cmd(self.cmd_dict)
		self.close_modal(self)
		return self.cmd_dict.get('id de la commande')

	def Save_credit(self,wid):
		self.cmd_dict["status de la facture"] = 'Crédit'
		self.cmd_dict["nature d'encaissement"] = "Déjà encaissé"
		#self.sc.DB.Save_encaiss_of(self.cmd_dict)
		self.excecute(self.sc.DB.Save_encaiss_of,self.cmd_dict)
		self.close_modal(wid)

	def set_periode(self):
		self.add_histo_surf()
		self.Up_table()

	def set_n_encaisse(self,info):
		self.n_encais = info
		self.Up_table()

	@Cache_error
	def impression(self,wid):
		obj = self.sc.imp_part_dic('Résumé')(self)
		liste = self.Trie_cmd()
		entete = ["date d'émission","Nom du client","montant réel",'autres montants',"status du paiement",
			"montant payé","nature d'encaissement","auteur"]
		wid_l = [.17,.12,.12,.11,.12,.12,.12,.12]
		titre = 'Encaissements de factures'
		info = f'Période : du {self.day1} au {self.day2}<br/>'
		if self.n_encais:
			info += f"Nature l'encaissement : {self.n_encais}<br/>"
		
		info += 'Agence TOKPOTA1'
		obj.Create_fact(wid_l,entete,liste,titre,info)

	def show_cmd(self,wid):
		info = wid.info
		if "écritures" in self.sc.DB.Get_access_of('Encaissements'):
			self.cmd_dict = self.sc.DB.Get_this_cmd(info)
			self.def_encaise_set(self.cmd_dict)
		else:
			self.sc.add_refused_error("Impossible de continuer à cause d'une restriction système !! Parlez-en à votre supérieur hiérachique")

class this_paie_dict(paiem_surf):
	#"""
	@Cache_error
	def th_add_paie(self):
		all_mont = float()
		for info in self.this_pai_list:
			cmp_ident = self.Paie_cmt_dict.get(info)
			if cmp_ident:
				mont = float(self.montant_dic.get(info))
				all_mont += mont
		if int(all_mont) == int(self.mother.cmd_dict.get("montant TTC")):
			cmd_ident = self.mother.Save_vente()
			if cmd_ident:
				for info in self.this_pai_list:
					cmp_ident = self.Paie_cmt_dict.get(info)
					if cmp_ident:
						mont = float(self.montant_dic.get(info))
						if mont:
							ref_dep = self.reference_dic.get(info)
							if not ref_dep:
								ref_dep = '/'
							liste = ref_dep.split("/")
							if liste:
								self.deposant = liste[0]
								self.reference = liste[-1]
							else:
								self.deposant,self.reference = 0,0

							cmd_ident = self.mother.cmd_ident
							if mont < 0:
								if "écritures" in self.sc.DB.Get_access_of("Annuller un recouvrement"):
									...
								else:
									self.sc.add_refused_error("Vous ne pouvez pas annuller un recouvrement. Informer votre supérieur!")
									return
							ret = self.valide_paie(cmd_ident,mont,cmp_ident)
							if ret:
								self.sc.DB.Save_paiement_of_this(cmd_ident,
									ret,mont,self.obj_paie)
			self.mother.close_modal()
			self.mother.add_all()
		else:
			self.sc.add_refused_error("Pour une facture au comptant, le montant doit être égale au montant de la facture!")
			return

	#"""