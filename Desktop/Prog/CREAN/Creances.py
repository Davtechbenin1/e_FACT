#Coding:utf-8
"""
	Interfaces de gestion des créances client
"""

from lib.davbuild import *
from General_surf import *
from ..CLT.Clients import details_client

from ..CMPT.general_obj2 import recouv_show
from ..CMPT.Commande import develop_cmd
from datetime import datetime
import datetime as DATE_T
from .cre_surf1 import *
from .cre_surf2 import *
from .cre_all_use import paiem_surf
from ...Model_acc import Model_acc

class Creances(Model_acc):
	def Set_but_icon_info(self):
		self.but_dic = {
			"Créances en cours":Creances_encours,
			"Créances impayées":Creance_impayer,
			"Les retours en stocks":Fact_avoir,
			"Historique":Creances_general,
			"Echéances du jours":Ech_en_cours,
			#"Historique des échéances":Histo_echeance,
		}
		if self.sc.get_in_progress() < 0:
			self.but_dic = {
			#"Créances en cours":Creances_encours,
			#"Créances impayées":Creance_impayer,
			#"Les retours en stocks":Fact_avoir,
			"Historique":Creances_general,
			#"Echéances du jours":Ech_en_cours,
			#"Historique des échéances":Histo_echeance,
		}
		self.icon_dic = {
			"Historique": "file-document",       # document/facture
			"Les retours en stocks":"cart-remove",
			"Créances en cours": "cash-multiple",        # billets de banque
			"Créances impayées": "alert-circle",         # alerte
			"Echéances du jours": "calendar-today",      # calendrier
			"Historique des échéances": "chart-line",          # graphique financier
		}
		self.sc.DB.Partage_hist()
		self.creance_imp = self.sc.DB.Get_cmd_impayer()
		self.creance_enc = self.sc.DB.Get_cmd_encours()
		self.my_info_dict = {
			"Historique":len(self.sc.DB.get_fact_of(
				(self.sc.get_today(),))),
			"Les retours en stocks":len(self.sc.DB.get_fact_retour_of(
				(self.sc.get_today()))),
			"Créances en cours":len(self.creance_enc),
			"Créances impayées":len(self.creance_imp),
			"Echéances du jours":len(self._trie_echeance()),
			"Historique des échéances":str()
		}
		self.titre = 'Histogramme des Créances'
		self.data_dict = {
			"":int(),
			"Créances impayées":len(self.creance_imp),
			"Créances en cours":len(self.creance_enc),
		}
		self.y_label = self.data_dict.keys()
		self.cols = [
		self.sc.text_col1,self.sc.red,self.sc.black,self.sc.green
			]
		self.th_padd = 5

	def _trie_echeance(self):
		liste = list()
		all_cmd_dic = self.sc.DB.Get_cmd_non_sold()
		for cmd_dic in all_cmd_dic.values():
			cmd = self.edite_cmd(cmd_dic)
			if cmd:
				liste.append(cmd)
		return liste

	def edite_cmd(self,cmd_dic):
		if cmd_dic.get('status de la commande') == "Livrée":
			cmd_dic = dict(cmd_dic)
			plan_paie = cmd_dic.get("plan de paiements")
			th_day = datetime.strptime(self.sc.get_today(),self.date_format)
			montant_impay = float()
			nbre_impay = int()
			encoure = float()
			for date,dic in plan_paie.items():
				th_date = datetime.strptime(date,self.date_format)
				if th_day > th_date:
					if dic.get("montant restant"):
						nbre_impay += 1
						montant_impay += float(dic.get('montant restant'))
				elif th_day == th_date:
					encoure = dic.get('montant restant')
			if encoure or montant_impay > 0:
				cmd_dic["montant de l'échéance"] = encoure
				cmd_dic["échéance échus non payé"] = montant_impay
				cmd_dic["nombre d'impayé"] = nbre_impay
				cmd_dic["total à payer ce jours"] = encoure + montant_impay
				cmd_dic["PAYEE"] = str()
				cmd_dic["Num"] = int(self.Get_real_num(cmd_dic.get('N°')))
				clt_dic = self.sc.DB.Get_this_clt(cmd_dic.get('client'))
				cmd_dic['Code client'] = clt_dic.get('N°')
				cmd_dic['Nom du client'] = clt_dic.get('nom')
				cmd_dic["date d'achat"] = cmd_dic.get('date de livraison')
				cmd_dic["affiliation"] = str()#self.sc.DB.Get_this_association(clt_dic.get("association appartenue")).get('nom',str())
				cmd_dic["catégorie"] = cmd_dic.get('type de contrat')
				return cmd_dic
			else:
				return None
		return None

class Details_charger(stack):
	def __init__(self,mother,**kwargs):
		kwargs['bg_color'] = mother.sc.aff_col1
		self.typ_val = "Créances"
		self.typ_val_list = "Créances",
		self.charg_aff = str()

		self.this_definition = mother.sc.DB.Get_creance_fiche_general(mother.day1)
		stack.__init__(self,mother,**kwargs)
		self.info_liste_fonc = {
			"Livraion":self.sc.DB.Get_livraison_of,
			"Créances":self.sc.DB.Get_creance_fiche_of,
			"Echéances":self.sc.DB.Get_echeance_fiche_of
		}
		self.spacing = dp(10)
		self.mont_declarer = int()
		self.mont_recu = int()

	@Cache_error
	def initialisation(self):
		self.clear_widgets()
		self.th_cmpt = str()
		if "écritures" in self.sc.DB.Get_access_of('Encaissements financier'):
			
			h = .05

			dic = {
				"Type de validation":(self.typ_val,self.typ_val_list,self.set_typ_val),
				"Chargée d'affaires":(self.charg_aff,self.sc.get_all_charger(),
					self.set_charg_aff)
			}
			for k,tup in dic.items():
				self.add_text(k + " :",size_hint = (.12,h),
					text_color = self.sc.text_col1)
				txt,lis,fonc = tup
				self.add_surf(liste_set(self,txt,lis,mother_fonc = fonc,
					size_hint = (.12,h),mult = 2))
			if self.typ_val and self.charg_aff:
				self.add_surf(Periode_set(self,size_hint = (.2,h), info = 'Date de définition',
					info_w = .4,one_part = True,exc_fonc = self.Set_date))

				self.add_icon_but(icon = 'printer',size_hint = (.1,h),
					text_color = self.sc.black,on_press = self.Imprimer)

				self.th_tab = stack(self,size_hint = (1,.88),
					bg_color = self.sc.aff_col3,padding = dp(10),
					radius = dp(10))
				self.add_surf(self.th_tab)

				self.total_surf = stack(self,size_hint = (1,h),
					spacing = dp(10))
				self.add_surf(self.total_surf)
				self.Up_tab()
		else:
			self.sc.add_refused_error("Impossible de continuer à cause d'une restriction système !! Parlez-en à votre supérieur hiérachique")

	@Cache_error
	def Up_tab(self):
		entete = ("Nom du client","date d'émission",
			'montant de la commande','montant déjà payé',
			"montant restant","montant déclaré",
			"Montant reçu comptable","Observation")
		cont_list = ("Montant reçu comptable")
		wid_l = .15,.1,.13,.13,.13,.13,.13,.1
		fonc = self.info_liste_fonc.get(self.typ_val)
		if fonc:
			self.TH_def = this_def = fonc(self.charg_aff,self.day1)
			if self.typ_val == 'Créances':
				liste = self.set_Creance_tab(this_def)
				self.This_tab_info(entete,wid_l,liste,
					cont_list,fonc)
			elif self.typ_val == "Echéances":
				print(this_def)
		else:
			self.sc.add_refused_error('Type de validation non valide')

	def Set_date(self):
		self.this_definition = self.sc.DB.Get_creance_fiche_general(self.day1)
		self.Up_tab()

	@Cache_error
	def set_Creance_tab(self,this_def):
		crean_gene = self.this_definition
		liste = list()
		self.mont_declarer = int()
		self.mont_recu = int()
		for ident, info_d in this_def.items():
			moont_col = info_d.get("montant collectée")
			cmd_dic = self.sc.DB.Get_this_cmd(ident)
			clt_dic = self.sc.DB.Get_this_clt(cmd_dic.get('client'))
			this_dic = crean_gene.get(ident,dict())
			this_dic['N°'] = cmd_dic.get('N°')
			self.mont_declarer += float(moont_col)
			mont_r = this_dic.get('Montant reçu comptable',float())
			if not mont_r:
				mont_r = float()
			self.mont_recu += float(mont_r)
			this_dic['montant déclaré'] = moont_col
			this_dic['Nom du client'] = clt_dic.get('nom')
			this_dic['montant de la commande'] = this_def.get(ident,dict()).get('montant de la commande')
			this_dic['montant déjà payé'] = this_def.get(ident,dict()).get('montant déjà payé')
			this_dic['montant restant'] = this_def.get(ident,dict()).get("montant restant") 
			this_dic["date d'émission"] = this_def.get(ident,dict()).get("date d'émission")
			liste.append(this_dic)
		return liste

	def This_tab_info(self,entete,wid_l,liste,cont_list,fonc):
		self.th_tab.clear_widgets()
		ent_surf = box(self,size_hint = (1,.06),spacing = dp(1),
			padding = dp(1),orientation = 'horizontal',
			bg_color = self.sc.sep,)
		bg_CC = self.sc.orange
		for w,ent in zip(wid_l,entete):
			bg_color = self.sc.text_col1
			if ent == "montant déclaré":
				bg_color = bg_CC
			ent_surf.add_text(ent,size_hint = (w,1),
				text_color = bg_color,
				bg_color = self.sc.aff_col1,
				padding_left = dp(10))
		self.th_tab.add_surf(ent_surf)
		lenf = len(liste)
		h = dp(50)
		H = dp(1) + (lenf * (h+dp(1)))
		scr = scroll(self,size_hint = (1,.9),
			bg_color = self.sc.aff_col3)
		tab = stack(self,size_hint = (1,None),height = H,
			)
		for obj in liste:
			b = box(self,size_hint = (1,None),spacing = dp(1),
			padding = dp(1),orientation = 'horizontal',
			bg_color = self.sc.sep,height = h)
			for w,ent in zip(wid_l,entete):
				bg_color = self.sc.text_col1
				if ent == "montant déclaré":
					bg_color = bg_CC
				if ent in cont_list:
					read = False
					if self.day1 == self.sc.get_today():
						read = False
					N = f"{ent}((_)){obj.get('N°')}"
					b.add_input(N, text_color = self.sc.text_col1,
						bg_color = self.sc.aff_col3,size_hint = (w,1),
						default_text = self.format_val(obj.get(ent,str())),
						on_text = self.set_mont_comp,readonly = read)
				else:
					b.add_text(self.format_val(obj.get(ent,str())),
						text_color = bg_color,
						bg_color = self.sc.aff_col1,
						size_hint = (w,1),padding_left = dp(10))
			tab.add_surf(b)
		scr.add_surf(tab)
		self.th_tab.add_surf(scr)
		self.add_mont_total()

	@Cache_error
	def add_mont_total(self):
		self.total_surf.clear_widgets()
		self.Up_mont_recu()
		dic = {
			"Total recouvrit":len(self.TH_def),
			"Montant total déclaré":self.mont_declarer,
			"Montant total reçu comptable":self.mont_recu,
			"Observation total":(self.mont_recu - self.mont_declarer)
		}
		for k,v in dic.items():
			self.total_surf.add_text_input(k,(.1,1),(.08,1),
				self.sc.text_col1,text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,readonly = True,
				default_text = self.format_val(v))
		self.total_surf.add_button_custom('Confirmer le paiement',
			self.Conf_paie,text_color = self.sc.text_col1,
			bg_color = self.sc.green, size_hint = (.15,1))

	def Up_mont_recu(self):
		self.mont_recu = int()
		for num in self.this_definition:
			mont = self.this_definition.get(num,dict()).get("Montant reçu comptable")
			if not mont:
				mont = float()
			self.mont_recu += mont

# Gestion des actions des boutton
	@Cache_error
	def Imprimer(self,wid):
		obj = self.sc.imp_part_dic('Fiche')(self)
		entete = ("Nom du client","date d'émission",
			'montant de la commande','montant déjà payé',
			"montant restant","montant déclaré",
			"Montant reçu comptable","Observation")
		total_ent = ("montant déclaré","Montant reçu comptable","Observation")
		wid_l = .15,.1,.13,.13,.13,.13,.13,.1
		titre = "Fiche de recouvrements journaliers"
		liste = self.set_Creance_tab(self.TH_def)
		info = f'Date : {self.day1}<br/>'
		if self.charg_aff:
			info += f"Chargé d'affaire : {self.charg_aff}<br/>"
		
		info += 'Agence TOKPOTA1'
		obj.Create_fact(wid_l,entete,liste,titre,info,total_ent)


	@Cache_error
	def Conf_paie(self,wid):
		if self.typ_val == "Créances" and self.day1 == self.sc.get_today():
			if not self.this_definition:
				self.sc.add_refused_error("Veillez renseigner les montants reçus au niveau de la comptabilité !")
				return
			h = .06
			dic = {
				"Total déclaré":len(self.TH_def),
				"Total Confirmer":len(self.this_definition),
				"Montant total déclaré":self.mont_declarer,
				"Montant total reçu comptable":self.mont_recu,
				"Observation total":(self.mont_recu - self.mont_declarer)
			}
			self.pass_conf = str()
			#self.sc.DB.Get_all_perso()
			perso_obj = self.sc.DB.Get_this_perso(self.sc.get_curent_perso())
			self.curent_pass = perso_obj.get('mot de pass')
			self.Conf_surf = stack(self,padding = dp(10),spacing = dp(10),
				bg_color = self.sc.aff_col1)
			self.Conf_surf.add_text('Veillez Confirmer les informations pour procéder au encaissements automatiques',
				size_hint = (.9,h),text_color = self.sc.text_col1,
				halign = "center", underline = True)
			self.Conf_surf.add_icon_but(icon = 'close',text_color = self.sc.red,
				on_press = self.close_modal,size_hint = (.1,h))
			for k,v in dic.items():
				self.Conf_surf.add_padd((.05,h))
				self.Conf_surf.add_text_input(k,(.3,h),(.45,h),
					self.sc.text_col1, text_color = self.sc.text_col1,
					bg_color = self.sc.aff_col1,readonly = True,
					default_text = self.format_val(v))
				self.Conf_surf.add_padd((.2,h))

			cmpt_lis = self.cmpt_list().keys()
			self.Conf_surf.add_padd((.05,h))
			self.Conf_surf.add_text('Choisi le compte payement',
				text_color = self.sc.text_col1,size_hint = (.3,h))
			self.Conf_surf.add_surf(liste_set(self,self.th_cmpt,list(cmpt_lis),"V",
				size_hint = (.65,.05),mother_fonc = self.set_cmpt,
				mult = 4))

			self.Conf_surf.add_padd((.05,h))
			self.Conf_surf.add_text_input('Confirmer votre mot de pass pour continuer',
				(.3,h),(.45,h),self.sc.text_col1, text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3, on_text = self.conf_pass,password = True)
			self.Conf_surf.add_padd((.2,h))

			self.last_surf = stack(self,size_hint = (1,h),spacing = dp(10))
			self.Conf_surf.add_surf(self.last_surf)
			self.Conf_last_surf()
			self.add_modal_surf(self.Conf_surf,size_hint = (.4,.8))
			self.initialisation()
		else:
			self.sc.add_refused_error('Action Impossible!\nImpossible de modifier une informations antérieur!',
				halign = 'left')

	def cmpt_list(self):
		liste = self.sc.DB.Get_comptes_dict()
		self.Paie_cmt_dict = dict()
		for ident,dic in liste.items():
			if dic.get('actif'):
				Num = dic.get('N° de compte')
				inst = dic.get('institutions')
				typ = dic.get('type de compte')
				info = f"{typ} : {inst}({Num})"
				self.Paie_cmt_dict[info] = ident
		return self.Paie_cmt_dict

	def Conf_last_surf(self):
		self.last_surf.clear_widgets()
		if self.curent_pass == self.pass_conf:
			if self.th_cmpt:
				self.last_surf.add_button_custom('Procéder au encaissements de fond',
					self.Confirme_pass,size_hint = (.6,1),padd = (.2,1),
					bg_color = self.sc.orange, text_color = self.sc.text_col1)
			else:
				self.sc.add_refused_error("Le compte de paiement est obligatoir")

	def set_cmpt(self,info):
		self.th_cmpt = info

	def conf_pass(self,wid,val):
		self.pass_conf = val
		self.Conf_last_surf()

	@Cache_error
	def Confirme_pass(self,wid):
		nom = self.charg_aff
		date = self.sc.get_today()
		mont = self.mont_recu
		if self.sc.DB.Save_details_journe(nom,date,mont):
			if self.curent_pass == self.pass_conf:
				self.sc.add_refused_error('début des recouvrements')
				self.sc.DB.Save_creance_fiche_general(self.this_definition,self.day1)
				for cmd_num ,dic in self.this_definition.items():
					self.This_client = self.sc.DB.Get_this_clt(self.sc.DB.Get_this_cmd(cmd_num).get("client")).get("nom")
					obj_paie = paiem_surf(self,.05,f"Confirmation de paiement du {self.sc.get_today()}",
						dic.get("Montant reçu comptable"))
					obj_paie.custum_add_paie(self.Paie_cmt_dict.get(self.th_cmpt),
						dic.get("Montant reçu comptable"),self.charg_aff,
						cmd_num,self.sc.get_today())

				self.sc.add_refused_error('Recouvrements Terminer')
				self.close_modal()

			else:
				self.sc.add_refused_error('Mot de pass incorrect!')
				self.Conf_last_surf()
		else:
			self.sc.add_refused_error("Action Impossible! Vous avez déjà éffectuer un paiement cette journée pour ce chargé d'affaire")

	def set_mont_comp(self,wid,info):
		#if self.day1 == self.sc.get_today():
		info = wid.info.split('((_))')
		wid.text = self.regul_input(wid.text)
		if len(info) == 2 and wid.text:
			part,num = info
			num_dic = self.this_definition.get(num,dict())
			num_dic[part] = float(wid.text)
			mont_tt = float(self.TH_def[num]["montant collectée"])
			self.this_definition[num] = num_dic
			self.this_definition[num]['montant déclaré'] = mont_tt
			self.this_definition[num]["Observation"] = (float(wid.text) - 
				mont_tt)
			self.add_mont_total()
		
	def set_typ_val(self,info):
		self.typ_val = info

		self.initialisation()

	def set_charg_aff(self,info):
		self.charg_aff = info
		self.initialisation()



