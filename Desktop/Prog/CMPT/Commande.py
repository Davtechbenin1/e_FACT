#Coding:utf-8

from lib.davbuild import *
from .old import *

from .general_obj2 import recouv_show

from General_surf import *
from datetime import datetime
import datetime as DATE_T
from .Ventes import vente_article

class develop_cmd(box):
	def __init__(self,mother,**kwargs):
		box.__init__(self,mother,**kwargs)
		#self.orientation = 'horizontal'
		self.check_access = mother.check_access
		self.status_dic = {
			"En attente":{
				"Lancer le traitement":self.traite_cmd,
				"Accepter la commande":self.accept_cmd,
				"Rejettée la commande":self.rejete_cmd,
			},
			"En cours":{
				"Lancer le traitement":self.traite_cmd,
				"Rejettée la commande":self.rejete_cmd,
			},
			"En traitement":{
				"Livrée la commande":self.livre_cmd,
			},
			"Livrée":{
			},
			"Rejettée":{
				"Relancer la commande":self.accept_cmd,
			},
			"Annullée":{
				"Relancer la commande":self.accept_cmd,
			}
		}
		self.size_pos()

	@Cache_error
	def size_pos(self):
		parti1 = box(self,spacing = dp(10),size_hint = (1,.5),
			orientation = 'horizontal')
		parti2 = box(self,spacing = dp(10),size_hint = (1,.5),
			orientation = 'horizontal')

		self.add_surf(parti1)
		self.add_surf(parti2)

		self.plan_surf = stack(self,size_hint = (.45,1),
			padding = dp(10),radius = dp(10),bg_color = self.sc.aff_col1,
			spacing = dp(5))
		self.penal_surf = stack(self,size_hint = (.55,1),
			padding = dp(10),radius = dp(10),bg_color = self.sc.aff_col1,
			spacing = dp(10))

		self.clt_part = stack(self,size_hint = (.45,1))
		self.art_part = stack(self,size_hint = (.55,1))

		parti1.add_surf(self.clt_part)
		parti1.add_surf(self.art_part)

		parti2.add_surf(self.penal_surf)
		parti2.add_surf(self.plan_surf)

		self.plan_date = self.day1
		self.plan_mont = float()

	@Cache_error
	def Foreign_surf(self):
		self.cmd_ident = self.mother.cmd_to_develop
		if self.cmd_ident:
			self.cmd_dict = self.mother.part1_surf.all_cmd_dict.get(self.cmd_ident)
			self.clt_dict = self.sc.DB.Get_this_clt(self.cmd_dict.get('client'))
			self.add_clt_part()
			self.add_art_part()
			self.add_penel_surf()
			if self.cmd_dict.get("status du paiement").lower() != "soldée":
				self.add_plan_paie()
			else:
				self.plan_surf.clear_widgets()
				self.plan_surf.add_text('Cette facture est déjà soldée',
					text_color = self.sc.text_col1,halign = 'center',
					font_size = '20sp')
		else:
			self.clear_widgets()
			self.size_pos()

	def add_clt_part(self):
		self.clt_part.clear_widgets()
		part1 = stack(self,size_hint = (.4,1),
			spacing = dp(5))
		part1.add_image(self.clt_dict.get('img'),
			size_hint = (1,.7))
		part1.add_text(self.clt_dict.get('nom'),font_size = "20sp",
			halign = 'center',text_color = self.sc.text_col1,
			size_hint = (1,.2))
		sol = self.clt_dict.get('solde')
		part1.add_text_input("solde :",(.3,.1),(.6,.1),self.sc.text_col1,
			text_color = self.sc.text_col1, bg_color = self.sc.aff_col3,
			default_text = self.format_val(sol),readonly = True)
		self.clt_part.add_surf(part1)
		part2 = stack(self,size_hint = (.6,.98),
			spacing = dp(5))
		contact = {
			"Tel :":self.clt_dict.get('tel'),
			"whatsapp :":self.clt_dict.get('whatsapp'),
			"email :":self.clt_dict.get('email'),
		}
		adress = self.sc.DB.adresse_of(self.clt_dict.get('N°'))
		identite = {
			"type :":self.clt_dict.get('type'),
			"catégorie :" :self.clt_dict.get('catégorie'),
			"association appartenue :":self.clt_dict.get('association appartenue')
		}
		part2.add_text('Infos client',size_hint = (1,.1),
			text_color = self.sc.text_col1,halign = 'center',
			font_size = "18sp",underline = True)
		for k,v in contact.items():
			part2.add_text_input(k,(.4,.1),(.6,.1),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				default_text = str(v),readonly = True)
		part2.add_text('Addresse complète :',text_color = self.sc.text_col1,
			size_hint = (1,.1))
		part2.add_padd((.05,.1))
		part2.add_text(adress,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,size_hint = (.95,.13),
			radius = dp(10),padding_left = dp(5))
		for k,v in identite.items():
			part2.add_text_input(k,(.4,.1),(.6,.1),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				default_text = str(v),readonly = True)
		self.clt_part.add_surf(part2)

	def add_art_part(self):
		self.art_part.clear_widgets()
		h = .08
		self.art_part.add_text('Liste des articles',
			size_hint = (.9,h),text_color = self.sc.text_col1,
			underline = True,halign = 'center',
			font_size = '19sp')
		self.art_part.add_icon_but(icon = 'close',text_color = self.sc.red,
				on_press = self.Close,size_hint = (.1,h))

		art_t = Table(self,size_hint = (1,h*8.5),
			bg_color = self.sc.aff_col3,
			padding = dp(10),radius= dp(10))
		self.art_part.add_surf(art_t)
		art_dics = self.cmd_dict.get('articles')
		this_art_l = list()
		all_taxe = float()
		for dic in art_dics.values():
			
			this_art_l.append(dic)
			all_taxe += float(dic.get("Taxes"))
		entete = ['Désignation',"Quantité",
		'Prix de vente','Taxes',"Montant TTC"]
		wid_l = [.2,.2,.2,.12,.16]
		art_t.Creat_Table(wid_l,entete,this_art_l,
			ent_size = (1,.15),mult = .2)
		self.art_part.add_text_input('Totale des articles : ',
			(.3,h),(.1,h),self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col1,default_text = str(len(art_dics)),readonly = True)

		self.art_part.add_text_input('Montant des taxes : ',
			(.3,h),(.2,h),self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col1,default_text = self.format_val(all_taxe),readonly = True)
		m_ttc = self.cmd_dict.get('montant TTC')
		a_mont = self.sc.DB.Get_autre_mont_of(self.cmd_dict)
		mont_d = {
			"montant TTC":m_ttc - a_mont,
			"autres montants":a_mont,
			"Montant Totale": m_ttc,
		}
		this_B = box(self,size_hint = (1,h*2),
			orientation = "horizontal",padding = dp(5),
			radius = dp(5),bg_color = self.sc.aff_col3,
			spacing = dp(5))
		for k,v in mont_d.items():
			b = box(self,radius = dp(5),
				bg_color = self.sc.aff_col1)
			b.add_text(k,halign = 'center',
				text_color = self.sc.text_col1)
			b.add_text(self.format_val(v),
				text_color = self.sc.text_col3,
				bg_color = self.sc.aff_col2,
				halign = 'center')
			this_B.add_surf(b)
		self.art_part.add_surf(this_B)

	@Cache_error
	def add_plan_paie(self):
		self.plan_surf.clear_widgets()
		self.plan_surf.add_text('Plan de paiement de la facture',
			halign = 'center',text_color = self.sc.text_col1,
			font_size = "19sp",underline = True,
			size_hint = (.9,.07))
		self.plan_surf.add_icon_but(icon = 'printer',size_hint = (.1,.07),
			text_color = self.sc.black,on_press = self.Impres)

		this_h = .07
		liv_date = self.cmd_dict.get("date de traitement prévu")
		mont_ttc = self.cmd_dict.get('montant TTC')
		mont_p = self.cmd_dict.get('montant payé')
		
		if not liv_date and self.check_access('définir date de livraison'):
			self.plan_surf.add_surf(Periode_set(self,
				info = 'Date de livraison prévu :',one_part = True,
				size_hint = (1,this_h),info_w = .3))
			self.plan_surf.add_button_custom('Définir',
				self.set_Date_liv,size_hint = (.5,this_h),
				padd = (.25,this_h))
			self.plan_surf.add_padd((.25,this_h))
		else:
			plan_paiement_dic = self.cmd_dict.get('plan de paiements',dict())
			tab_list = self.get_plan_infos()
			entete = 'Date','Montant',"Status"
			wid_l = .3,.35,.35
			
			Tab = Table(self,size_hint = (1,.8),padding = dp(5),
				radius = dp(5),bg_color = self.sc.aff_col3)
			Tab.Creat_Table(wid_l,entete,tab_list,
				ent_size = (1,.08))
			self.plan_surf.add_surf(Tab)
		
		# Définition de pénalité de paiement
			self.plan_surf.add_text_input('Montant payé :',
				(.25,this_h),(.25,this_h),self.sc.text_col1,
				bg_color = self.sc.aff_col2,
				default_text = self.format_val(mont_p),
				text_color = self.sc.text_col3)

			self.plan_surf.add_text_input('Reste à payer :',
				(.25,this_h),(.25,this_h),self.sc.text_col1,
				bg_color = self.sc.aff_col2,
				default_text = self.format_val(mont_ttc - mont_p),
				text_color = self.sc.text_col3)

	@Cache_error
	def get_plan_infos(self):
		plan_paiement_dic = self.cmd_dict.get('plan de paiements',dict())
		paiem_list = self.cmd_dict.get('paiements',list())
		plan_paiement_dic = self.sort_plan_dict(plan_paiement_dic)
		
		plan_l = [(date,mont) for date,mont in plan_paiement_dic.items()]
		mont_l = list()
		self.mont_prevue = float()
		for tup in plan_l:
			date,mont = tup
			ind = plan_l.index(tup)
			status = "Non soldé"
			if len(paiem_list) > ind:
				this_ind = paiem_list[ind]
				info,IND = this_ind.split('N°')
				status = f"Soldé ce ({IND.split('_')[0]})"
			this_d = {
				"Date":date,
				"Montant":mont,
				"Status":status,
				"id":ind
			}
			self.mont_prevue += float(mont)
			mont_l.append(this_d)
		mont_l = self.sc.sorted_by_date(mont_l,key = "Date")
		return mont_l

	def sort_plan_dict(self,dic):
		keys = [i for i in dic]
		dates_list = [datetime.strptime(date,"%d-%m-%Y") for date in keys]
		dates_list.sort()
		this_d_lis = [day.strftime("%d-%m-%Y") for day in dates_list]
		return {i:dic[i] for i in this_d_lis}

	@Cache_error
	def add_penel_surf(self):
		this_h = .08
		self.penal_surf.clear_widgets()
		self.penal_surf.add_text('Information général sur la commande',
			text_color = self.sc.text_col1,halign = 'center',
			size_hint = (1,this_h),font_size = '19sp',underline = True)
		infos = {
			#"Identifiant de la commande" : self.cmd_dict.get('id de la commande'),
			"Status de la commande":self.cmd_dict.get('status de la commande'),
			"Status du paiement":self.cmd_dict.get('status du paiement'),
		}
		for k,v in infos.items():
			self.penal_surf.add_text_input(k,(.5,this_h),
				(.5,this_h),self.sc.text_col1,default_text = str(v),
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				readonly = True)
		self.penal_surf.add_text('Listes des paiements :',
			size_hint = (.2,this_h*1.5),text_color = self.sc.text_col1,
			)
		liste = self.cmd_dict.get('paiements')
		ind = 0
		for id_paie in liste:
			ind += 1
			self.penal_surf.add_button(str(ind)+'e',text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,size_hint = (.1,this_h),
				on_press = self.show_recouvr,info = id_paie)
		self.penal_surf.add_padd((1,.01))
		this_p = self.cmd_dict.get('paiement actuel')
		date,mont = str(),float()
		t_date,t_mont = str(),float()
		der_paie = self.sc.DB.Get_next_paie(self.cmd_dict)
		if der_paie:
			t_date,t_mont = der_paie
		if this_p:
			date,mont = self.sc.DB.Get_this_paie_date_mont(this_p)
		dic = {
			"Dernier paiement: ":(date,mont,"fait le"),
			"Prochain paiement: ":(t_date,t_mont,"prévu le"),
		}
		for k,v in dic.items():
			dic = {
				"Montant":v[1],
				"Date":v[0],
			}
			sep = v[-1]
			self.penal_surf.add_text_multi_input(k,(.35,this_h),
				(.25,this_h),self.sc.text_col1,dic,readonly = True,
				sep = sep,sep_w = .15)
		status = self.cmd_dict.get('status de la commande')
		status_paie = self.cmd_dict.get('status du paiement')
		but_list = self.get_button_dict(status)
		but_surf = box(self,size_hint = (1,this_h*1.5),
			orientation = 'horizontal',padding = dp(5),
			spacing = dp(5),radius = dp(5),
			bg_color = self.sc.aff_col3)
		but_surf.rejette_cmd = self.rejette_cmd
		info = self.cmd_dict.get('id de la commande')
		if self.check_access("gestion cmds"):
			for but,but_fonc in but_list.items():
				bg_col = self.sc.green
				if 'supprimer' in but.lower():
					bg_col = self.sc.red
				but_surf.add_button(but,
					info = info,
					text_color = self.sc.aff_col3,
					bg_color = bg_col,
					on_press = but_fonc)
			if but_list:
				self.penal_surf.add_surf(but_surf)
		if status.lower() in ['en cours',"en traitement",'en attente']:
			if status.lower() == 'en traitement' and not self.cmd_dict.get('montant payé'):
				self.modif_but()
			elif status.lower() != "en traitement":
				self.modif_but()
		self.penal_surf.add_padd((.066,.1))
		self.penal_surf.add_button('Impression',
			text_color = self.sc.aff_col3,bg_color = self.sc.aff_col2,
			size_hint = (.4,.1),on_press = self.impression)
		self.penal_surf.add_padd((.066,.1))
		if not self.cmd_dict.get('montant payé') and self.cmd_dict.get('status de la commande') == "Livrée":
			self.penal_surf.add_button('Retour en stock',
				text_color = self.sc.text_col3,bg_color = self.sc.red,
				size_hint = (.4,.1),on_press = self.retour_en_stock)
			self.penal_surf.add_padd((.066,.1))

	def get_button_dict(self,status):
		return self.status_dic[status]

	def init_table(self):
		self.mother.cmd_to_develop = str()
		self.mother.add_all()

	def modif_but(self):
		if self.check_access("modifier commande"):
			self.penal_surf.add_padd((.066,.1))
			self.penal_surf.add_button('Modifier la commande',
				text_color = self.sc.text_col3,bg_color = self.sc.aff_col2,
				size_hint = (.4,.1),on_press = self.mofid_cmd)
			self.penal_surf.add_padd((.066,.1))
			self.penal_surf.add_button('Supprimer la commande',
				text_color = self.sc.text_col3,bg_color = self.sc.red,
				size_hint = (.4,.1),on_press = self.supp_cmd)
			self.penal_surf.add_padd((.066,.1))

# Méthodes de gestion des actions
	def Close(self,wid):
		try:
			self.mother.clear_widgets()
			self.mother.size_pos()
			self.mother.add_all()
		except:
			self.mother.add_all()

	@Cache_error
	def retour_en_stock(self,wid):
		ident = self.cmd_dict.get("id de la commande")
		self.cmd_dict = self.sc.DB.Get_this_cmd(ident)
		if self.cmd_dict and self.cmd_dict.get('status général') != "Commande retournée":
			self.sc.set_confirmation_srf(self.EX_ret_en_stk)
		else:
			self.sc.add_refused_error('Commande déjà retournée')
			self.mother.initialisation()

	@Cache_error
	def EX_ret_en_stk(self):
		#self.excecute(self.ret_en_stk)
		self.ret_en_stk()
		#self.sc.add_refused_error('Commande retournée')
		self.init_table()
		self.mother.initialisation()

	def ret_en_stk(self):
		ident = self.cmd_dict.get("id de la commande")
		cmd_dict = self.Get_this_cmd(ident)
		if cmd_dict and cmd_dict.get('status général') != "Commande retournée":
			cmd_dict['status de la commande'] = "Livrée"
			cmd_dict['status général'] = "Commande retournée"
			cmd_dict['date de livraison'] = self.sc.get_now()
			cmd_dict['date de traitement prévu'] = self.sc.get_today()
			date = cmd_dict.get("date d'émission")
			cmd_dict['montant TTC'] = - cmd_dict['montant TTC']
			autre_mont = cmd_dict.get('autre montant')
			arts = self.cmd_dict.get('articles')
			for dic in arts.values():
				vente = dic.get('ventes')
				vente = {k:-v for k,v in vente.items()}
				dic["ventes"] = vente
				dic['Taxes'] = -dic['Taxes']
				dic['Montant HT'] = -dic['Montant HT']
				dic['Montant TTC'] = -dic['Montant TTC']
			self.sc.DB.Modif_this_cmd(cmd_dict)
		else:
			self.sc.add_refused_error('Commande déjà retournée')

	def impression(self,wid):
		try:
			self.sc.Factures_impression(self.cmd_dict)
		except Exception as E:
			ERROR = traceback.format_exc()
			print(ERROR)
			self.sc.add_refused_error("Erreur inconnu")

	@Cache_error
	def Impres(self,wid):
		liste = self.get_plan_infos()
		obj = self.sc.imp_part_dic('Résumé')(self)
		entete = ["Date",'Montant',"Status"]
		wid_l = .3,.35,.35
		info = ""
		titre = "Fiche de plan de paiements"
		obj.Create_fact(wid_l,entete,liste,titre,info)

	@Cache_error
	def set_Date_liv(self,wid):
		date_liv = self.day1
		self.sc.day1 = self.sc.get_today()
		clt_nam = self.cmd_dict.get('client')
		mont = self.cmd_dict.get('montant TTC')
		plan_dic = self.sc.DB.Get_plan_paiement(clt_nam,mont,date_liv)
		self.cmd_dict["plan de paiements"] = plan_dic
		self.cmd_dict['date de traitement prévu'] = date_liv
		self.excecute(self.sc.DB.Modif_this_cmd,self.cmd_dict)
		self.add_plan_paie()
		self.sc.add_refused_error('Date de traitement définie, Plan de paiement aussi définie automatiquement')

	@Cache_error
	def traite_cmd(self,wid):
		ident = wid.info
		cmd_dict = self.cmd_dict
		cmd_dict['status de la commande'] = "En traitement"
		cmd_dict['type de facture'] = 'Facture'
		self.excecute(self.sc.DB.Modif_this_cmd,cmd_dict)
		self.sc.add_refused_error('Commande en cours de traitement')
		self.init_table()

	@Cache_error
	def accept_cmd(self,wid):
		ident = wid.info
		cmd_dict = self.cmd_dict
		cmd_dict['status de la commande'] = "En cours"
		self.excecute(self.sc.DB.Modif_this_cmd,cmd_dict)
		self.sc.add_refused_error('Commande Acceptée')
		self.init_table()

	@Cache_error
	def livre_cmd(self,wid):
		cmd_dict = self.cmd_dict
		if cmd_dict:
			self.real_cmd = self.sc.DB.Get_this_cmd(cmd_dict.get('N°'))
			if self.real_cmd['status de la commande'] != 'Livrée':
				self.sc.set_confirmation_srf(self.liv_th_cmd)
			else:
				self.sc.add_refused_error('Commande déjà livrée')
				self.init_table()
		else:
			self.sc.add_refused_error("Impossible de continuer à cause d'une restriction système !! Parlez-en à votre supérieur hiérachique")

	def liv_th_cmd(self):
		cmd_dict = self.cmd_dict
		if cmd_dict:
			real_cmd = self.real_cmd
			if real_cmd['status de la commande'] != 'Livrée':
				real_cmd['status de la commande'] = "Livrée"
				real_cmd['date de livraison'] = self.sc.get_now()
				real_cmd['date de traitement prévu'] = self.sc.get_today()
				date = real_cmd.get("date d'émission")
				#self.excecute(self._liv,real_cmd)
				self._liv(real_cmd)
				self.sc.add_refused_error('Commande définie comme livrée')
				self.init_table()
			else:
				self.sc.add_refused_error('Commande déjà livrée')
				self.init_table()

	def _liv(self,cmd_dict):
		self.sc.DB.Modif_this_cmd(cmd_dict)
		
	@Cache_error
	def supp_cmd(self,wid):
		cmd_dict = self.cmd_dict
		self.real_cmd = self.sc.DB.Get_this_cmd(cmd_dict.get('N°'))
		if self.real_cmd:
			if self.real_cmd.get('montant payé'):
				self.sc.add_refused_error("Impossible de supprimer une commande dont le paiement a commancé")
			else:
				self.sc.set_confirmation_srf(self.th_supp)
		
		
	def th_supp(self):
		self.excecute(self._supp_cmd,self.real_cmd)
		self.sc.add_refused_error('Commande Supprimer')
		self.init_table()


	def _supp_cmd(self,cmd_dict):
		ident = cmd_dict.get('id de la commande')
		date = ident.split("N°")[-1].split("_")[0]
		#self.sc.DB.Sup_histo_cmd(cmd_dict.get('N°'),cmd_dict.get('client'))
		self.sc.DB.Sup_this_cmd(date,ident)

	def rejete_cmd(self,wid):
		pass

	def modif_plan(self,wid):
		"""Pas de modification une définie"""
		pass

	@Cache_error
	def mofid_cmd(self,wid):
		if "écritures" in self.sc.DB.Get_access_of("Factures"):
			self.mother.close_modal()
			self.modif_surf = Modifier_cmd(self,self.cmd_dict)
			self.mother.add_modal_surf(self.modif_surf,
				size_hint = (.9,.9))
		else:
			self.sc.add_refused_error("Impossible de continuer à cause d'une restriction système !! Parlez-en à votre supérieur hiérachique")

	def BACK(self,wid):
		#self.mother.clear_widgets()
		self.mother.close_modal()
		self.mother.add_all()

	def show_recouvr(self,wid):
		self.clear_widgets()
		self.recouv_to_developp = wid.info
		self.add_surf(recouv_show(self,bg_color = self.sc.aff_col1))

	def rejette_cmd(self,ident):
		"Permet la gestion du rejet de commande"
		self.sc.add_refused_error('cliquer')

	def set_penalit(self,wid,val):
		try:
			float(val)
		except:
			if wid.text:
				wid.text = wid.text[:-1]
		else:
			self.cmd_dict['pénalité'] = float(val)

	def set_opt_penalit(self,wid,val):
		try:
			float(val)
		except:
			if wid.text:
				wid.text = wid.text[:-1]
		else:
			self.cmd_dict["options pénalité"] = float(val)

	def valid_penalite(self,wid):
		if self.cmd_dict.get('pénalité'):
			self.sc.add_refused_error('Information sur la pénalité ajouter')
			self.Up_cmd()
	
	def Up_cmd(self):
		T = Thread(target = self.sc.DB.Modif_this_cmd,
			args = (self.cmd_dict,))
		T.start()

	def set_plan_date(self):
		self.plan_date = self.day1

	def set_plan_mont(self,wid,val):
		try:
			val = float(val)
		except:
			if val:
				self.sc.add_refused_error("Le montant doit être un entier")
		else:
			self.plan_mont = float(val)

class Modifier_cmd(box):
	def __init__(self,mother,cmd_dict,**kwargs):
		kwargs['padding'] = dp(10)
		kwargs['spacing'] = dp(10)
		kwargs['orientation'] = "horizontal"
		box.__init__(self,mother,**kwargs)

		self.cmd_dict = cmd_dict
		self.autres_montant = self.cmd_dict.get('autre montant')
		self.fact_show = True
		self.fact_to_developp = str()
		self.panier_dict = dict()
		self.check_access = self.mother.check_access

		self.set_qts_of = str()
		self.size_pos()

	@Cache_error
	def size_pos(self):
		self.vente_surf = This_vente_art(self,size_hint = (.65,1),
		bg_color = self.sc.aff_col1,spacing = dp(10),
		radius = dp(10),padding = dp(10))
		self.vente_surf.add_all()
		self.details_surf = This_Finalisation(self.vente_surf,
			size_hint = (.35,1),type_fact = "Facture",
			autres_montant = self.autres_montant,
			bg_color = self.sc.aff_col1,spacing = dp(10),
			radius = dp(10))

		self.add_surf(self.vente_surf)
		self.add_surf(self.details_surf)

class This_vente_art(vente_article):
	@Cache_error
	def size_pos(self):
		self.cmd_dict = self.mother.cmd_dict
		self.This_client = self.cmd_dict.get('client')
		self.magasin = "Général"
		self.type_fact = "Facture"
		self.lancer_imp = str()
		self.type_fact_list = ["Facture","Proforma"]
		art_list = self.cmd_dict.get('articles')
		clt_typ = self.sc.DB.Get_this_clt(self.This_client).get('catégorie')

		art_dicts = {art["Désignation"]:art for art in art_list}
		self.add_input_clt_set()

		self.this_clt_info = stack(self,size_hint = (.5,.12),
			spacing = dp(5))
		self.magasin_surf = stack(self,size_hint = (.4,.12),
			spacing = dp(5))

		self.new_clt_surf = New_clt_Def(self,size_hint = (.5,.4),
			spacing = dp(5))

		self.corps_surf = Vente_surf(self,size_hint = (1,.86))


	@Cache_error
	def add_entet_surf(self,*args):
		self.add_text('Client :',text_color = self.sc.text_col1,
			size_hint = (.08,.04))
		if not self.This_client:
			try:
				self.up_this_clt_surf()
			except:
				self.sc.add_refused_error("Impossible de modifier le client d'une commande déjà établit !")
				return
			if self.New_clt:
				self.new_clt_surf.add_all()
				self.add_surf(self.new_clt_surf)
			else:
				self.add_surf(self.input_clt_surf)
				self.add_button('Ajouter',size_hint = (.2,.04),
					text_color = self.sc.text_col3,bg_color = self.sc.green,
					on_press = self.Add_new_clt)

		if self.This_client:
			self.add_this_clt_info()
			self.add_surf(self.this_clt_info)
			self.Up_magasin_surf()
			self.add_surf(self.magasin_surf)
			self.corps_surf.clt_type = self.clt_type
			self.corps_surf.add_all()
			self.add_surf(self.corps_surf)

class This_Finalisation(Finalisation_surf):
	@Cache_error
	def initialisation(self):
		self.check_access = self.mother.check_access
		self.motif_paiement = 'Paiement au comptant'
		self.payer_ = "Non"
		self.TTC = str()
		self.montant = float()
		self.type_fact_list = 'Facture',"Proforma"
		self.type_fact = "Facture"
		self.begin_mont = {k:v for k,v in self.mother.cmd_dict.get("autre montant").items()}
		self.autres_montant = self.mother.cmd_dict.get("autre montant")

		self.size_pos()
		self.add_all()

	def up_paiement(self):
		self.get_montant()
		self.payement_surf.clear_widgets()
		self.payement_surf.add_padd((.12,.1))
		self.payement_surf.add_button('Modifier la commande',
			size_hint = (.35,.11),text_color = self.sc.text_col3,
			bg_color = self.sc.green, on_press = self.Valid_vente)
		self.payement_surf.add_padd((.05,.1))
		self.payement_surf.add_button('Annullée la modification',
			size_hint = (.35,.11),text_color = self.sc.text_col3,
			bg_color = self.sc.red, on_press = self.Quitter)

	def fermetture(self):
		self.Quitter(self)

	def Quitter(self,wid):
		self.mother.mother.mother.BACK(wid)
		self.mother.mother.mother.mother.add_all()

	@Cache_error
	def Save_vente(self):
		self.cmd_dict = self.mother.cmd_dict
		mont = self.mother.corps_surf.Get_total()
		mont += self.get_autre_m(self.autres_montant)
		
		paie_sta = "Non Soldée"
		cmd_sta = self.cmd_dict.get('status de la commande')
		format_cmd = self.sc.DB.Get_cmd_format()
		fille_id = format_cmd.get('id de la commande')
		L = ('paiements','montant payé','paiement actuel','date de traitement',
			'date de livraison',"provenance d'origine","auteur d'origine",
			'date de traitement prévu','options pénalité',"plan de paiements",
			'pénalité','client',)
		self.cmd_dict["commande modifiée"] = fille_id
		for k in L:
			format_cmd[k] = self.cmd_dict[k]

		format_cmd['plan de paiements'] = self.Get_curent_plan(
			self.cmd_dict.get('montant payé'),
			self.cmd_dict.get('paiements'),
			mont,
			)
		if self.type_fact == "Facture":
			status_cmd = 'En traitement'
		else:
			status_cmd = 'En cours'
		if self.valide.lower() == "oui":
			status_cmd = 'Livrée'
		T = time.time()
		self.excecute(self.SAVE,format_cmd,mont,status_cmd,paie_sta)
		print(T-time.time())

		
		return format_cmd.get('id de la commande')
#
	def SAVE(self,format_cmd,mont,status_cmd,paie_sta):
		format_cmd['client'] = self.sc.DB.Get_this_clt_num(format_cmd.get("client"))
		format_cmd['montant TTC'] = mont
		format_cmd['articles'] = self.mother.corps_surf.Get_aff_list()
		format_cmd['status de la commande'] = status_cmd
		format_cmd['status du paiement'] = paie_sta
		format_cmd['provenance'] = "Bureau"
		format_cmd['magasin'] = self.mother.magasin
		format_cmd['type de facture'] = self.type_fact
		format_cmd['auteur'] = self.sc.get_curent_perso()
		format_cmd['autre montant'] = self.autres_montant

		format_cmd['commande mère'] = self.cmd_dict.get('id de la commande')
		format_cmd['date et heur de modification'] = self.sc.get_now()

		#self.sc.DB.sup_autre_m(self.cmd_dict,self.begin_mont)
		self.sc.DB.Modif_this_cmd(self.cmd_dict)
		self.sc.DB.Sup_histo_cmd(self.cmd_dict.get('N°'),self.cmd_dict.get('client'))
		self.sc.DB.Save_cmd(format_cmd)

	def Get_curent_plan(self,mont_pay,paiements,mont_t):
		plan = dict()
		reste = mont_t - mont_pay
		if mont_pay:
			plan[self.sc.get_today()] = {"montant dû":mont_pay,"montant payé":mont_pay,
			"date":self.sc.get_today(),"montant restant":0,"paiement associé":paiements}
		if reste:
			date = datetime.strptime(self.sc.get_today(),self.date_format) + DATE_T.timedelta(days = 2)
			plan[date.strftime(self.date_format)] = {"montant dû":reste,"montant payé":float(),"date":str(),
				"montant restant":reste,"paiement associé":list()}
		return plan

