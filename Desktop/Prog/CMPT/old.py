from lib.davbuild import *
from General_surf import *
from .general_obj2 import recouv_show
from .old1 import *
from .stk_surf import *
import time

class Vente_surf(Appro_surf):
	def initialisation(self):
		self.spacing = dp(10)
		self.padding = dp(10)
		self.size_pos()
		self.init_infos()
		self.set_taxes = True
		self.valide_here = False
		self.montant_srf = None

	def size_pos(self):
		self.clear_widgets()
		self.article_srf = stack(self,size_hint = (.4,.3))
		self.paramet_srf = stack(self,size_hint = (.5,.3),
			padding = dp(10),spacing = dp(10),radius = dp(10),
			bg_color = self.sc.aff_col1)
		self.button_srf = stack(self,size_hint = (.1,.3))
		self.article_tab = Table(self,size_hint = (1,.63),
			bg_color = self.sc.aff_col3,exec_fonc = self.modify_art,
			exec_key = "Désignation")
		self.add_surf(self.article_srf)
		Get_border_surf(self,self.paramet_srf,
			self.sc.green)
		self.add_surf(self.button_srf)
		self.add_surf(self.article_tab)

	def Foreign_surf(self):
		self.add_article_srf()
		self.add_article_tab()

	def add_article_tab(self):
		self.add_paramet_srf()
		entete = ["Désignation","Quantité","Prix de vente",
			'Montant HT',"Taxes","Montant TTC"]
		wid_l = [.25,.15,.2,.15,.1,.15]
		liste = self.get_th_article_list()
		self.article_tab.Creat_Table(wid_l,entete,list(liste),
			mult = .2)
		if self.montant_srf:
			self.montant_srf.text = self.format_val(self.montant_total)

	def add_paramet_srf(self):
		self.paramet_srf.clear_widgets()
		self.curent_art_param = self.set_curent_art_param()
		self.add_button_srf()
		h = dp(40)
		if self.curent_art_name:
			acht_dic = self.curent_art_param.get('ventes')
			prix_ven = self.curent_art_param.get("prix de vente")
			for cond,qte in acht_dic.items():
				self.paramet_srf.add_text(cond,
					size_hint = (.2,None),
					height = h, halign = 'right')
				self.paramet_srf.add_input(f"{cond}",
					placeholder = "Quantité",
					default_text = str(qte),
					size_hint = (.3,None),
					height = h,on_text = self.set_qte_achat)
				self.paramet_srf.add_text(f'prix du {cond}',
					size_hint = (.2,None),
					height = h, halign = 'right')
				self.paramet_srf.add_input(f"{cond}",
					default_text = str(prix_ven.get(cond)),
					size_hint = (.3,None),height = h,
					on_text = self.set_prix_achat,
					placeholder = "Prix de vente")

	def set_curent_art_param(self):
		if self.curent_art_name:
			curent_art = self.sc.DB.Get_this_article(self.curent_art_name)

			if not curent_art:
				return

			ident = curent_art.get('N°')
			curent_art_param = self.article_dic.get(ident,dict())
			if curent_art_param:
				return curent_art_param

			art_conds = curent_art.get('conditionnement')

			mag_id = self.sc.magasin #self.sc.DB.Get_this_magasin(self.magasin).get("N°")
			
			curent_art_param = {
				"Désignation":curent_art.get('Désignation'),
				"N°":curent_art.get('N°'),
				"img":curent_art.get('img'),
				"ventes":{cond:float() for cond in art_conds.keys()},
				"prix de vente":curent_art.get(
					"prix de vente",{cond:float() 
					for cond in art_conds.keys()}),
			}
			return curent_art_param
		return None

	def get_th_article_list(self):
		self.montant_total = float()
		for dic in self.article_dic.values():
			self.montant_total += dic.get("Montant TTC")
		return self.article_dic.values()

# Gestion des actions des bouttons
	def add_art_param(self,wid):
		th_b = dict(self.curent_art_param)
		qte = th_b.get('ventes')
		vent = th_b.get("prix de vente")
		montant = self.get_montant(qte,vent)
		qte_str = self.sc.get_info_str(qte)
		if not qte_str and th_b.get('N°') in self.article_dic:
			self.article_dic.pop(th_b.get('N°'))
		else:
			th_b["Quantité"] = qte_str
			th_b["Prix de vente"] = self.sc.get_info_str(vent)
			th_b['Montant HT'] = montant
			th_b["Taxes"] = self.taxes
			th_b["Montant TTC"] = montant + self.taxes
			self.article_dic[th_b.get('N°')] = th_b
		self.article_list_srf.info = str()
		self.article_list_srf.add_all()
		self.curent_art_name = dict()
		self.add_article_tab()
		self.mother.finition_srf.add_all()
		self.Update_total_surf()

	def Get_aff_list(self):
		return self.article_dic

	def Update_total_surf(self):
		self.mother.finition_srf.total_mont_srf.text = self.format_val(
			self.Get_total())

	def Get_total(self):
		montant = int()
		for th_b in self.article_dic.values():
			th_b = dict(th_b)
			qte = th_b.get('ventes',dict())
			vent = th_b.get("prix de vente",dict())
			montant += self.get_montant(qte,vent)
		autre_mont = self.mother.finition_srf.autres_montant
		montant += self.get_autre_m(autre_mont)
		return montant

	def Get_all_infos(self):
		nbre_art = len(self.article_dic)
		qte_str = str()
		taxes = int()
		mont_ht = int()
		qte_dict = dict()
		for name,art_d in self.article_dic.items():
			vente_dic = art_d.get('ventes')
			prix_vent = art_d.get('prix de vente')

			for k,v in vente_dic.items():
				qte_t = qte_dict.setdefault(k,int())
				qte_t += float(v)
				qte_dict[k] = qte_t
			mont_ht += float(art_d.get('Montant HT'))
			taxes += float(art_d.get('Taxes'))
			
		for th_k,th_v in qte_dict.items():
			qte_str += f' {th_k} {th_v}'
		dic = {
			"Nombre d'articles :":nbre_art,
			"Quantités Totals :":qte_str,
			"montant hors taxes :":mont_ht,
			"montant des taxes :":taxes,
		}
		return dic

	def _save_art_param(self):
		...

	def set_qte_achat(self,wid,val):
		cond = wid.info
		wid.text = self.regul_input(wid.text)
		self.curent_art_param["ventes"][cond] = float(wid.text)

	def set_prix_achat(self,wid,val):
		cond = wid.info
		wid.text = self.regul_input(wid.text)
		self.curent_art_param["prix de vente"][cond] = float(wid.text)
	
class Finalisation_surf(stack):
	def __init__(self,mother,autres_montant = dict(),
		type_fact = "Facture",**kwargs):
		self.valide = str()
		stack.__init__(self,mother,**kwargs)
		self.padding = dp(10)
		self.type_fact = type_fact
		self.autres_montant = autres_montant
	
	@Cache_error
	def initialisation(self):
		self.motif_paiement = 'Paiement au comptant'
		self.payer_ = "Non"
		self.TTC = str()
		self.montant = float()
		self.type_fact_list = 'Facture',"Proforma"
		self.type_fact = "Facture"
		self.autres_montant = dict()
		self.size_pos()
		self.Set_T()

	@Cache_error
	def Foreign_surf(self):
		self.set_infos_part()
		self.autre_mont_surf.mother_fonc = self.mother.vente_surf.corps_surf.Update_total_surf
		self.autre_mont_surf.add_all()

	@Cache_error
	def size_pos(self):
		self.clear_widgets()
		self.add_text('Finalisation de la commandes en cours',
			text_color = self.sc.green,halign = 'center',
			size_hint = (1,.04),underline = True)
		self.Total_surf = box(self,size_hint = (1,.1),
			orientation = 'horizontal',padding = dp(10))
		
		self.infos_part = stack(self,size_hint = (1,.2),
			padding_left = dp(10),spacing = dp(5))
		self.autre_mont_surf = autre_montan_set(self,size_hint = (1,.25),
			)
		self.autre_mont_surf.autres_montant = self.autres_montant
		self.autre_mont_surf.mont_select_list = [i for i in self.autres_montant.keys()]
		
		self.add_surf(self.Total_surf)
		self.add_surf(self.infos_part)
		self.add_text("Les autres montants accessoires",size_hint = (1,.04),
			text_color = self.sc.text_col1,halign = 'center',underline = True)
		self.add_surf(self.autre_mont_surf)
		#self.add_text('Valider directement la commande?',size_hint = (.4,.05),
		#	text_color = self.sc.text_col1)
		#self.add_surf(liste_set(self,self.valide,("Oui","Non"),
		#	size_hint = (.5,.05),mult = 1, mother_fonc = self.set_valide))
		self.last_part = stack(self,size_hint = (1,.045),
			)
		self.last_part.add_padd((.066,1))
		self.last_part.add_button('Sauvegarder',
				size_hint = (.4,1),text_color = self.sc.aff_col1,
				bg_color = self.sc.green, on_press = self.Valid_vente)
		self.last_part.add_padd((.066,1))

		self.last_part.add_button('Livrée directement',
				size_hint = (.4,1),text_color = self.sc.aff_col1,
				bg_color = self.sc.orange, on_press = self.Impression)
		self.add_surf(self.last_part)

		self.infos___p = box(self,size_hint = (1,.08))
		self.add_surf(self.infos___p)

	def up_infos___p(self):
		solde = self.mother.vente_surf.clt_dict.get('solde')
		self.infos___p.clear_widgets()
		if solde and solde > 0:
			self.infos___p.add_text('Cet client à une créance non soldé en cours',
				text_color = self.sc.red,font_size = '20sp',
				halign = "center")
		elif solde and solde < 0:
			self.infos___p.add_text('Cet client doit avoir une commande non livrées en cours',
				text_color = self.sc.orange,font_size = '20sp',
				halign = "center")

	def Set_T(self,*args):
		self.Total_surf.clear_widgets()
		self.Total_surf.add_text('',size_hint = (.3,1))
		self.total_mont_srf = self.Total_surf.add_text(str(),
			size_hint = (.4,1),halign = 'center',radius = dp(25),
			bg_color = self.sc.aff_col3,text_color = self.sc.black,
			font_size = "20sp")
		self.Total_surf.add_text('',size_hint = (.3,1))

	@Cache_error
	def set_infos_part(self):
		self.infos_part.clear_widgets()
		h = .25
		self.TTC = total = self.mother.vente_surf.corps_surf.Get_total()
		infos_dic = self.mother.vente_surf.corps_surf.Get_all_infos()
		qte_str = infos_dic.get("Quantités Totals :")
		infos_dic['Montant TTC :'] = total
		for k ,v in infos_dic.items():
			if k!= "Quantités Totals :":
				val = self.Get_format_val(v)
				self.infos_part.add_text_input(k,(.3,h),
					(.2,h),self.sc.text_col1,text_color = self.sc.text_col1,
					bg_color = self.sc.aff_col1,default_text = val,
					readonly = True)
		self.infos_part.add_text_input("Quantités Totals :",(.3,h),
			(.7,h),self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col1,default_text = qte_str,
			readonly = True)
		self.infos_part.add_text('Type de la facture :',text_color = self.sc.text_col1,
			size_hint = (.3,h))
		self.infos_part.add_surf(liste_set(self,self.type_fact,self.type_fact_list,
			size_hint = (.7,h),mult = 1, mother_fonc = self.set_type_fact))
		try:
			self.up_infos___p()
		except:
			pass

	def get_montant(self):
		self.montant = self.mother.vente_surf.corps_surf.Get_total()
		self.montant += self.get_autre_m(self.autres_montant)

	@Cache_error
	def Save_vente(self,imp = False):
		"""
			Doit retourner l'id de la commande
		"""
		self.mont = self.mother.vente_surf.corps_surf.Get_total()
		self.mont += self.get_autre_m(self.autres_montant)
		self.selected_client = self.mother.vente_surf.This_client
		self.th_art_list = self.mother.vente_surf.corps_surf.Get_aff_list()

		self.magasin = self.mother.vente_surf.magasin
		
		if not self.selected_client:
			self.sc.add_refused_error('Le client est obligatoire')
			return False
		
		elif not self.th_art_list:
			self.sc.add_refused_error('Impossible de sauvegarder une commande vide!')
			return False

		elif not self.type_fact:
			self.sc.add_refused_error('Le type de la facture doit être définie')
			return False

		else:
			self.sc.set_confirmation_srf(self._Save)
			
			return True

	def _Save(self):
		self.excecute(self.SAVE)
		self.initialisation()
		self.autres_montant = dict()
		self.mother.vente_surf.clear_widgets()
		self.mother.vente_surf.size_pos()
		self.mother.vente_surf.add_all()
		self.mother.add_all()
		self.fermetture()

	def _Save_imp(self):
		#self.excecute(self.SAVE)
		self.SAVE()
		self.initialisation()
		self.autres_montant = dict()
		self.mother.vente_surf.clear_widgets()
		self.mother.vente_surf.size_pos()
		self.mother.vente_surf.add_all()
		self.mother.add_all()
		self.fermetture()
		try:
			self.sc.Factures_impression(self.commande_dic)
		except Exception as E:
			ERROR = traceback.format_exc()
			print(ERROR)
			self.sc.add_refused_error("Erreur inconnu")
		
	def Set_total_surf(self):
		self.autres_montant = self.autre_mont_surf.autres_montant

	def fermetture(self):
		pass

	def SAVE(self):
		selected_client = self.selected_client.strip()
		mont = self.mont
		format_cmd = dict()
		if self.type_fact == "Facture":
			status_cmd = 'En traitement'
			status_paye = "Non Soldée"
			trait_date = self.sc.get_today()
		else:
			status_cmd = 'En cours'
			status_paye = "Non Soldée"
			trait_date = str()
		if self.valide.lower() == "oui":
			status_cmd = 'Livrée'
			format_cmd['date de livraison'] = self.sc.get_now()

		format_cmd['client'] = self.sc.DB.Get_this_clt_num(selected_client)
		format_cmd['montant TTC'] = mont
		format_cmd['magasin'] = self.magasin
		format_cmd['type de facture'] = self.type_fact
		format_cmd['autre montant'] = self.autre_mont_surf.autres_montant
		format_cmd['articles'] = self.th_art_list#self.mother.corps_surf.Get_aff_list()
		format_cmd['status de la commande'] = status_cmd
		format_cmd['status du paiement'] = status_paye
		format_cmd['date de traitement'] = trait_date
		format_cmd['provenance'] = "Bureau"
		format_cmd['auteur'] = self.sc.get_curent_perso()
		format_cmd["provenance d'origine"] = "Bureau"
		format_cmd["auteur d'origine"] = self.sc.get_curent_perso()
		format_cmd['plan de paiements'] = {self.sc.get_today():{
			"montant dû":mont,"montant payé":float(),"date":str(),
			"montant restant":mont,"paiement associé":list()
		}}
		self.commande_dic = format_cmd
		self.sc.DB.Save_cmd(format_cmd)

# méthodes de gestion des actions
	def set_valide(self,info):
		self.valide = info

	def set_autre_mont(self,liste):
		self.autres_montant = {d.get('Désignation'):d.get("Montant") 
			for d in liste if d}

	@Cache_error
	def Valid_vente(self,wid):
		self.valide = "non"
		ind = self.Save_vente()

	def Impression(self,wid):
		self.valide = "oui"
		self.Save_vente(True)
		
		"""
		
		clas = self.sc.imp_part_dic('Factures')
		clas.cmd_dic = self.commande_dic
		self.Popup_impression(clas)
		"""

	def back(self,wid):
		pass

	def Modif_motif(self,wid,val):
		self.motif_paiement = val

	def modif_paye(self,info):
		self.payer_ = info
		self.modif_infosss()

	def set_type_fact(self,info):
		self.type_fact = info

class New_clt_Def(stack):
	def initialisation(self):
		self.choix = str()
		self.charger_aff = str()
		self.clt_name = self.mother.search_infos
		
	@Cache_error
	def Foreign_surf(self):
		h = .055
		self.dic1 = {
			"nom":self.clt_name,
			"tel":str(),
			"whatsapp":str(),
			"IFU":str(),
		}
		self.dic_p = {
			"type":'particulier',
			"catégorie":'standart',
		}
		self.clear_widgets()
		#print(self.sc.DB.Get_client_format('particulier').get('N°'))
		b = box(self,orientation = 'horizontal',size_hint = (1,None),
			height = dp(35))
		b.add_text('Nouveau client',text_color = self.sc.text_col1,
			halign = 'center',underline = True,font_size = '17sp')
		b_ = box(self,size_hint = (None,1),width = dp(35))
		b_.add_close_but(self.BACK,text_color = self.sc.red)
		b.add_surf(b_)
		self.add_surf(b)
		if "écritures" in self.sc.DB.Get_access_of('Clients'):
			self.add_text_input("Date d'enrégistrement ",(.3,h),
				(.6,h),self.sc.text_col1,
				bg_color = self.sc.aff_col1,
				text_color = self.sc.text_col1,
				default_text = self.sc.get_today(),
				readonly = True,font_size = '20sp')
			for k,v in self.dic1.items():
				self.add_text_input(k,(.3,h),(.6,h),
					self.sc.text_col1,bg_color = self.sc.aff_col3,
					text_color = self.sc.text_col1,on_text = self.set_infos,
					default_text = v,)
			
			self.add_button_custom('Ajouter',self.set_new_clt,
				size_hint = (.5,h),padd = (.25,h),
				text_color = self.sc.aff_col1)

	def up_liste_surf(self):
		liste = [i for i in self.sc.get_all_charger() if self.choix.lower() in i.lower()]
		self.liste_surf.list_info = liste
		self.liste_surf.add_all()

# Méthode de gestion des actions
	def set_infos(self,wid,val):
		self.dic1[wid.info] = val

	def set_new_clt(self,wid):
		if self.dic1["nom"]:
			clt_dict = dict(self.dic1)
			clt_dict['nom'] = clt_dict['nom'].replace(".","")
			if self.charger_aff:
				clt_dict["chargé d'affaire"] = self.charger_aff
			ret = self.sc.DB.Save_client(clt_dict)
			if not ret:
				self.sc.add_refused_error("Un client de même nom existe déjà")
			else:
				self.mother.This_client = clt_dict.get("nom")
				self.mother.New_clt = False
				self.mother.add_all()
		else:
			self.sc.add_refused_error('Le nom est obligatoire')

	def BACK(self,wid):
		self.mother.New_clt = False
		self.mother.add_all()

	def set_typ (self,info):
		self.dic_p["type"] = info
	
	def set_choix(self,wid,val):
		self.choix = val
		self.up_liste_surf()

	def set_choix_def(self,info):
		self.choix = info
		self.charger_aff = info


