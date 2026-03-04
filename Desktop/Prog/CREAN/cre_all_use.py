from lib.davbuild import *
from General_surf import *

from ..CMPT.Commande import develop_cmd
from ..CMPT.general_obj2 import *
from datetime import datetime
import datetime as DATE_T

class Show_creance_surf(develop_cmd):
	def size_pos(self):
		parti1 = box(self,spacing = dp(10),size_hint = (1,.48),
			orientation = 'horizontal')
		parti2 = box(self,spacing = dp(10),size_hint = (1,.52),
			orientation = 'horizontal')
		self.TH_PLAN_D = dict()

		self.add_surf(parti1)
		self.add_surf(parti2)

		self.plan_surf = stack(self,size_hint = (.65,1),
			padding = dp(10),radius = dp(10),bg_color = self.sc.aff_col1,
			spacing = dp(5))
		self.penal_surf = stack(self,size_hint = (.35,1),
			padding = dp(10),radius = dp(10),bg_color = self.sc.aff_col1,
			spacing = dp(10))

		self.clt_part = stack(self,size_hint = (.45,1))
		self.art_part = stack(self,size_hint = (.55,1))

		parti1.add_surf(self.clt_part)
		parti1.add_surf(self.art_part)

		parti2.add_surf(self.plan_surf)
		parti2.add_surf(self.penal_surf)

		self.plan_date = self.day1
		self.plan_mont = float()

		self.date_liv = self.sc.get_today()
		self.date_ech = str()
		self.type_contra = str()
		self.form_paie = str()
		self.new_paie = False

		self.this_time_dict = {
			"Hebdomadaire":4,
			"Journalier":30,
			"Mensuelle":1,
		}
		self.this_form_dic = {
			"Hebdomadaire":"Semaines",
			"Journalier":'Jours',
			"Mensuelle":"Mois",
		}
		self.default_time = float()
		self.default_taux = 25

		self.type_definition = "Automatique"
		self.type_def_liste = ["Manuelle","Automatique"]

	@Cache_error
	def Foreign_surf(self):
		self.cmd_ident = self.mother.cmd_ident
		if self.cmd_ident:
			self.cmd_dict = self.sc.DB.Get_this_cmd(self.cmd_ident)
			self.TH_PLAN_D = self.cmd_dict.get('plan de paiements')
			self.This_client = self.cmd_dict.get('client')
			self.clt_dict = self.sc.DB.Get_this_clt(self.This_client)
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

	@Cache_error
	def add_plan_paie(self):
		liv_date = self.cmd_dict.get("plan de paiements")
		if not liv_date and self.check_access('définir date de livraison'):
			self.Definir_plan()
		else:
			self.plan_surf.clear_widgets()
			self.plan_surf.add_text('Plan de paiement de la facture',
				halign = 'center',text_color = self.sc.text_col1,
				font_size = "19sp",underline = True,
				size_hint = (.7,.07))
			self.plan_surf.add_icon_but(icon = 'printer',text_color = self.sc.black,
				on_press = self.Imp,size_hint = (.1,.07))

			if "écritures" in self.sc.DB.Get_access_of("Encaissements financier"):
				self.plan_surf.add_icon_but(icon = 'hand-coin-outline',
					text_color = self.sc.green,size_hint = (.1,.07),
					on_press = self.new_paie_set,)

			self.plan_surf.add_icon_but(icon = 'history',text_color = self.sc.text_col1,
				on_press = self.hist_part_set,size_hint = (.1,.07))

			this_h = .07
			liv_date = self.cmd_dict.get("date de traitement prévu")
			mont_ttc = self.cmd_dict.get('montant TTC')
			mont_p = self.cmd_dict.get('montant payé')
			
			plan_paiement_dic = self.cmd_dict.get('plan de paiements',dict())
			tab_list = self.get_plan_infos()
			entete = ('date prévue',"montant dû","date de paiement",
			"montant payé","montant restant")
			wid_l = .2,.2,.2,.2,.2
			
			Tab = Table(self,size_hint = (1,.8),padding = dp(5),
				radius = dp(5),bg_color = self.sc.aff_col3,
				exec_fonc = None,exec_key = 'date prévue')
			Tab.Creat_Table(wid_l,entete,tab_list,
				ent_size = (1,.145))
			self.plan_surf.add_surf(Tab)
			self.plan_surf.add_text_input('Montant payé :',
				(.15,this_h),(.15,this_h),self.sc.text_col1,
				bg_color = self.sc.aff_col2,readonly = True,
				default_text = self.format_val(mont_p),
				text_color = self.sc.text_col3)

			self.plan_surf.add_text_input('Reste à payer :',
				(.15,this_h),(.15,this_h),self.sc.text_col1,
				bg_color = self.sc.aff_col2,readonly = True,
				default_text = self.format_val(mont_ttc - mont_p),
				text_color = self.sc.text_col3)

	@Cache_error
	def Definir_plan(self):
		this_h = .09
		self.plan_surf.clear_widgets()
		self.plan_surf.add_text('Définition du plan de paiement de la facture',
			halign = 'center',text_color = self.sc.text_col1,
			font_size = "20sp",underline = True,
			size_hint = (1,.07))
		#if not self.type_definition:
		self.plan_surf.add_text('Choix de la définition du plan',
			text_color = self.sc.text_col1,size_hint = (.4,this_h))
		self.plan_surf.add_surf(liste_set(self,self.type_definition,
			self.type_def_liste,size_hint = (.5,this_h),
			mother_fonc = self.set_type_def,mult = 1))
		if self.type_definition == "Automatique":
			self.P1 = Periode_set(self,info = 'Date de livraison prévu'
				,one_part = True,size_hint = (.5,this_h),info_w = .2,
				exc_fonc = self.set_date_liv_)
			self.P2 = Periode_set(self,info = "Date du premier échéance",
				one_part = True,size_hint = (.5,this_h), info_w = .2,
				exc_fonc = self.set_date_ech,date_key = 'day2')
			self.plan_surf.add_surf(self.P1)
			if self.date_liv:
				self.plan_surf.add_surf(self.P2)

				if self.date_ech:
					self.plan_surf.add_text("Type de contrat",size_hint = (.2,this_h),
						text_color = self.sc.text_col1)
					self.plan_surf.add_surf(liste_set(self,self.type_contra,
						self.sc.DB.Get_types_contrats_list(),size_hint = (.8,this_h),
						mult = 1,mother_fonc = self.set_type_contra))
					if self.type_contra:
						self.form_paie = self.sc.DB.Get_types_contrats().get(self.type_contra)
						self.plan_surf.add_text_input('Forme de paiement',(.2,this_h),(.3,this_h),
							self.sc.text_col1,bg_color = self.sc.aff_col3,text_color = self.sc.text_col1,
							readonly = True,default_text = self.form_paie)
						if self.form_paie:
							self.default_time = self.this_time_dict.get(self.form_paie)
							self.plan_surf.add_text_input('Durée du contrat',(.2,this_h),
								(.1,this_h),self.sc.text_col1,text_color = self.sc.text_col1,
								bg_color = self.sc.aff_col3,on_text = self.set_default_time,
								default_text = str(self.default_time))
							self.plan_surf.add_text(self.this_form_dic.get(self.form_paie),
								text_color = self.sc.aff_col2,size_hint = (.2,this_h))

							self.plan_surf.add_text_input('Taux du premier déversement',(.2,this_h),
								(.1,this_h),self.sc.text_col1,text_color = self.sc.text_col1,
								bg_color = self.sc.aff_col3,on_text = self.set_default_taux,
								default_text = str(self.default_taux))

							self.plan_surf.add_text("%",
								text_color = self.sc.aff_col2,size_hint = (.2,this_h))
							self.plan_surf.add_padd((1,.0000001))

							self.plan_surf.add_button_custom('Définir',
								self.set_Date_liv,size_hint = (.3,this_h),
								padd = (.13,this_h),text_color = self.sc.aff_col1)
			if self.TH_PLAN_D:
				self.plan_surf.add_button_custom('Quitter',
					self.End_manuelle,size_hint = (.3,this_h),
					padd = (.13,this_h),bg_color = self.sc.red)
				self.plan_surf.add_padd((.13,this_h))
							
		elif self.type_definition == "Manuelle":
			plan_dic = self.TH_PLAN_D
			th_liste = [{"Date (format: JJ-MM-YYYY)":date,
			"Montant":self.format_val(d.get('montant dû'))} 
			for date,d in plan_dic.items()]

			self.plan_surf.add_button_custom("Terminé",self.End_manuelle,
				size_hint = (.1,this_h))
			self.tab = dynamique_tab(self,size_hint = (1,.7),
				bg_color = self.sc.aff_col3)
			self.plan_surf.add_surf(self.tab)
			wid_l = (.6,.4)
			entete = ["Date (format: JJ-MM-YYYY)",'Montant']
			self.tab.infos_list = th_liste
			self.tab.Creat_Table(wid_l,entete,self.up_mont_last)
			self.mont_last = box(self,size_hint = (1,.1),
				spacing = dp(10),orientation = 'horizontal')
			self.plan_surf.add_surf(self.mont_last)
			self.up_mont_last(self.tab.infos_list)

	def up_mont_last(self,liste):
		mont_T = float()
		plan_dic = dict()
		date_liste = list()
		for dic in liste:
			k = dic.get("Date (format: JJ-MM-YYYY)")
			v = dic.get('Montant')
			try:
				v = v.replace(' ','')
				v = float(v)
			except:
				self.sc.add_refused_error("Le montant n'est pas valide")
				return False
			mont_T += v
			k_l = k.split('-')
			if len(k_l) != 3:
				self.sc.add_refused_error("Le format de date n'est pas respecter")
				return False
			else:
				try:
					date = datetime.strptime(k,self.date_format)
					date_liste.append(date)
				except:
					self.sc.add_refused_error("La date n'est pas une date valide")
					return False
				else:
					#if date <= datetime.strptime(self.sc.get_today(),self.date_format):
					#	self.sc.add_refused_error('La date doit être supérieur ou égale à la date du jour')
					#	return False
					date_liste.append(date)
			plan_dic[date.strftime(self.date_format)] = {"montant dû":v,"montant payé":float(),"date":str(),
			"montant restant":v,"paiement associé":list()}
		date_liste.sort()
		if date_liste:
			day2 = date_liste[-1]
		else:
			day2 = datetime.strptime(self.sc.get_today(),self.date_format)
		to_day = datetime.strptime(self.sc.get_today(),self.date_format)
		d_time = (to_day - day2).days

		self.cmd_dict['plan de paiements'] = plan_dic
		self.cmd_dict["type de contrat"] = 'Inconnue'
		self.cmd_dict['date de fin contrat'] = day2.strftime(self.date_format)
		self.cmd_dict["plan de remboursement"] = "Personalisé"
		self.cmd_dict['durée du contrat'] = d_time
		self.mont_last.clear_widgets()
		self.excecute(self.sc.DB.Modif_this_cmd,self.cmd_dict)
		#self.sc.DB.Modif_this_cmd(self.cmd_dict)
		mont_ttc = self.cmd_dict.get('montant TTC')
		mont_p = self.cmd_dict.get('montant payé')
		mont_a_payer = mont_ttc - mont_p
		self.mont_last.add_text_input('Montant à payé',(1,1),(1,1),
			self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,default_text = self.format_val(mont_a_payer),
			readonly = True)
		self.mont_last.add_text_input('Total définie',(1,1),(1,1),
			self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,readonly = True,
			default_text = self.format_val(mont_T),
			)
		self.mont_last.add_text_input('Reste à définir',(1,1),(1,1),
			self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,readonly = True,
			default_text = self.format_val(mont_a_payer-mont_T),
			)

	def get_plan_infos(self):
		plan_paiement_dic = self.cmd_dict.get('plan de paiements',dict())
		paiem_list = self.cmd_dict.get('paiements',list())
		try:
			plan_paiement_dic = self.sort_plan_dict(plan_paiement_dic)
		except:
			self.sc.add_refused_error('Une erreur est survenue lors du trie du plan de paiement')
			plan_paiement_dic = dict()
		
		mont_l = list()
		for k,dic in plan_paiement_dic.items():
			if type(dic)!=dict:
				self.cmd_dict['plan de paiements'] = dict()
			else:
				d = {
					"date prévue":k,
					"montant dû":dic.get("montant dû"),
					"date de paiement":dic.get('date'),
					"montant payé":dic.get('montant payé'),
					"montant restant":dic.get('montant restant')
				}
				mont_l.append(d)
		return mont_l

	def sort_plan_dict(self,dic):
		keys = [i for i in dic]
		date_liste = [datetime.strptime(date,self.date_format) for date in keys]
		date_liste.sort()
		this_d_lis = [day.strftime(self.date_format) for day in date_liste]
		return {i:dic[i] for i in this_d_lis}

	@Cache_error
	def add_penel_surf(self):
		this_h = .09
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
			self.penal_surf.add_text_input(k,(.65,this_h),
				(.35,this_h),self.sc.text_col1,default_text = str(v),
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				readonly = True)
		
		self.penal_surf.add_padd((1,.01))
		
		status = self.cmd_dict.get('status de la commande')
		status_paie = self.cmd_dict.get('status du paiement')
		but_list = self.get_button_dict(status)
		but_surf = box(self,size_hint = (1,this_h*1.3),
			orientation = 'horizontal',padding = dp(5),
			spacing = dp(5),radius = dp(5),
			bg_color = self.sc.aff_col3)
		but_surf.rejette_cmd = self.rejette_cmd
		info = self.cmd_dict.get('id de la commande')
		if self.check_access("gestion cmds"):
			for but,but_fonc in but_list.items():
				but_surf.add_button(but,
					info = info,
					text_color = self.sc.aff_col3,
					bg_color = self.sc.green,
					on_press = but_fonc)
			if but_list:
				self.penal_surf.add_surf(but_surf)
		if status.lower() in ['en cours',"en traitement",'en attente']:
			if status.lower() == 'en traitement' and not self.cmd_dict.get('montant payé'):			
				self.modif_but()
			elif status.lower() != "en traitement":
				self.modif_but()

		self.penal_surf.add_padd((.066,this_h))
		self.penal_surf.add_button('Impression',
			text_color = self.sc.text_col3,bg_color = self.sc.orange,
			size_hint = (.4,this_h),on_press = self.impression)
		self.penal_surf.add_padd((.066,.1))
		if self.cmd_dict.get('montant TTC') > 0:
			if not self.cmd_dict.get('paiements'):
				self.penal_surf.add_button('Redéfinir le plan',
					text_color = self.sc.text_col3,bg_color = self.sc.red,
					size_hint = (.4,.1),on_press = self.redefinir)
				self.penal_surf.add_padd((.066,.1))
			self.penal_surf.add_padd((.066,.1))
			if not self.cmd_dict.get('montant payé') and self.cmd_dict.get('status de la commande') == "Livrée":
				self.penal_surf.add_button('Retour en stock',
					text_color = self.sc.text_col3,bg_color = self.sc.red,
					size_hint = (.4,.1),on_press = self.retour_en_stock)
				self.penal_surf.add_padd((.066,.1))

	@Cache_error
	def set_payement_day(self):
		mont_p = self.get_autre_m(self.cmd_dict.get('autre montant'))
		montant = self.cmd_dict.get('montant TTC')
		real_mont = montant - mont_p
		date_liv = self.date_liv
		j,m,y = [int(i) for i in date_liv.split('-')]
		first_mont = int(round(real_mont * self.default_taux/100)) + mont_p
		laste_mont = montant - first_mont

		plan_dic = {
			date_liv:first_mont,
		}
		j1,m1,y1 = [int(i) for i in self.date_ech.split('-')]
		depart = DATE_T.date(y1,m1,j1)
		nbr_d = int(self.default_time/7)
		ech_t = nbr_d * 3
		mont_jour = round(laste_mont/ech_t)
		while ech_t > 0:
			plan_dic,depart,laste_mont = self.Get_week_paie(
				depart,mont_jour,plan_dic,laste_mont)
			ech_t -= 1
		return plan_dic

	def Get_week_paie(self,depart,mont_jour,plan_dic,mont_t):
		while depart.weekday() not in (0,2,4):
			depart = depart + DATE_T.timedelta(days = 1)
		plan_dic[depart.strftime(self.date_format)] = mont_jour
		mont_t -= mont_jour
		depart = depart + DATE_T.timedelta(days = 2)
		return plan_dic,depart,mont_t

	def set_payement_week(self):
		mont_p = self.get_autre_m(self.cmd_dict.get('autre montant'))
		montant = self.cmd_dict.get('montant TTC')
		real_mont = montant - mont_p
		date_liv = self.date_liv
		j,m,y = [int(i) for i in date_liv.split('-')]
		first_mont = int(round(real_mont * self.default_taux/100)) + mont_p
		laste_mont = montant - first_mont

		plan_dic = {
			date_liv:first_mont,
		}
		mont_paie = round(laste_mont/float(self.default_time))
		j1,m1,y1 = [int(i) for i in self.date_ech.split('-')]
		depart = DATE_T.date(y1,m1,j1)
		for i in range(0,self.default_time):
			plan_dic[depart.strftime(self.date_format)] = mont_paie
			depart += DATE_T.timedelta(days = 7)
		return plan_dic

	def set_payement_month(self):
		mont_p = self.get_autre_m(self.cmd_dict.get('autre montant'))
		montant = self.cmd_dict.get('montant TTC')
		real_mont = montant - mont_p
		date_liv = self.date_liv
		j,m,y = [int(i) for i in date_liv.split('-')]
		first_mont = int(round(real_mont * self.default_taux/100)) + mont_p
		laste_mont = montant - first_mont

		plan_dic = {
			date_liv:first_mont,
		}
		mont_paie = round(laste_mont/float(self.default_time))
		j1,m1,y1 = [int(i) for i in self.date_ech.split('-')]
		depart = DATE_T.date(y1,m1,j1)
		for i in range(0,round(float(self.default_time))):
			plan_dic[depart.strftime(self.date_format)] = mont_paie
			depart += DATE_T.timedelta(days = 30)
		return plan_dic

	@Cache_error
	def set_hist_surf(self,obj_paie):
		this_dict = self.cmd_dict.get('plan de paiements')
		if this_dict:
			this_plan_d = this_dict.get(obj_paie)
			try:
				mont_ttc = self.cmd_dict.get('montant TTC')
				mont_p = self.cmd_dict.get('montant payé')
				montant = float(mont_ttc) - float(mont_p)
			except:
				try:
					montant = float(self.cmd_dict.get('montant TTC'))
				except:
					montant = 0
			if self.new_paie:
				srf = paiem_surf(self,.09,obj_paie,montant,info_w = .3,
					size_hint = (1,.9))
				self.plan_surf.clear_widgets()
				b = box(self,orientation = "horizontal",size_hint = (1,.09))
				b.add_text(f"Nouvelle paiement de l'échéance {obj_paie}",
					text_color = self.sc.text_col1,halign = 'center',
					underline = True)
				b.add_icon_but(icon = 'close',size_hint = (None,None),size = (dp(30),dp(30)),
					text_color  =self.sc.red,on_press = self.set_paiement,
					info = obj_paie)
				self.plan_surf.add_surf(b)
				self.plan_surf.add_surf(srf)
			elif not montant:
				self.sc.add_refused_error(f"Le montant n'est pas valide! montant = {self.montant}")
			else:
				h = .09
				self.plan_surf.clear_widgets()
				self.plan_surf.add_text(f"Historiques des paiements de la factures {self.cmd_dict.get('N°')}",
					text_color = self.sc.text_col1,size_hint = (.9,h),
					font_size = "16sp",halign = 'center')
				self.plan_surf.add_icon_but(icon = 'close',text_color = self.sc.red,
					size_hint = (.1,h),on_press = self.set_paiement)
				tab = Table(self,size_hint = (1,.9), 
					bg_color = self.sc.aff_col3,
					radius = dp(10),padding = dp(10),
					exec_key = 'id du paiement',exec_fonc = self.show_encai)
				liste = self.Up_liste_paie()
				entete = ("date","heure",'montant',"opérateur")
				wid_l = (.25,.25,.25,.25)
				tab.Creat_Table(wid_l,entete,liste)
				self.plan_surf.add_surf(tab)

	def Up_liste_paie(self):
		liste_paie = self.cmd_dict.get('paiements')
		th_liste = list()
		for ident in liste_paie:
			paie_dic = self.sc.DB.get_recette(ident)
			num = self.get_num(paie_dic.get('id du paiement'))
			paie_dic['Num'] = num
			th_liste.append(paie_dic)
		th_liste.sort(key = itemgetter("Num"))
		ordre = 0
		new_l = list()
		for dic in th_liste:
			ordre += 1
			dic["N° d'ordre"] = ordre
			new_l.append(dic)
		return new_l

	def get_num(self,num):
		if num:
			lis = num.split("N°")
			if lis:
				nu = lis[1]
				date,nu = nu.split('_')
				d,m,y = date.split("-")
				th_nu = f"{y}{m}{d}{nu}"
				return int(th_nu)
		return int()

	def Save_vente(self):
		return self.cmd_ident

	def init_table(self):
		self.mother.cmd_to_develop = str()
		self.mother.init_wid()

# Gestion des actions des buttons
	def show_encai(self,wid):
		ref = wid.info
		self.recouv_to_developp = ref
		obj = paie_show(self,bg_color = self.sc.aff_col1)
		self.add_modal_surf(obj,size_hint = (.7,.8))

	def Close(self,wid):
		self.mother.clear_widgets()
		self.mother.size_pos()
		self.mother.add_all()
		
	@Cache_error
	def Imp(self,wid):
		liste = self.get_plan_infos()
		obj = self.sc.imp_part_dic('Résumé')(self)
		entete = ['date prévue',"montant dû","date de paiement",
			"montant payé","montant restant"]
		wid_l = .25,.18,.19,.19,.19
		titre = "Fiche de plan de paiements"
		info = f"Client : {self.cmd_dict.get('client')}<br/>"
		info += f"Commande N° : {self.cmd_dict.get('id de la commande')}<br/>"
		obj.Create_fact(wid_l,entete,liste,titre,info)

	def set_default_taux(self,wid,val):
		wid.text = self.regul_input(wid.text)
		if wid.text:
			self.default_taux = float(wid.text)
		else:
			self.default_taux = 0

	def End_manuelle(self,wid):
		#self.cmd_dict['plan de paiements'] = self.TH_PLAN_D
		self.add_plan_paie()

	def set_type_def(self,info):
		self.type_definition = info
		self.Definir_plan()

	def back_to(self,wid):
		self.add_all()

	def new_paie_set(self,wid):
		self.new_paie = True
		self.set_hist_surf(self.sc.get_today())

	def set_paiement(self,wid):
		self.new_paie = False
		self.add_plan_paie()

	def hist_part_set(self,wid):
		self.new_paie = False
		self.set_hist_surf(self.sc.get_today())

	def set_Date_liv(self,wid):
		date_liv = self.date_liv
		try:
			if datetime.strptime(self.date_ech,self.date_format)<=datetime.strptime(date_liv,self.date_format):
				self.sc.add_refused_error('La date du premier échéance doit être supérieur à la date de livraison prévu.')
				return
			elif self.default_taux < 2:
				self.sc.add_refused_error('Le taux du premier déversement ne peut pas être Inférieur à 2%')
				return
				
			else:
				if self.form_paie == "Journalier":
					plan_dic = self.set_payement_day()
				elif self.form_paie == 'Hebdomadaire':
					plan_dic = self.set_payement_week()
				elif self.form_paie == "Mensuelle":
					plan_dic = self.set_payement_month()

				dates = [datetime.strptime(i,self.date_format) for i in plan_dic]
				fin_cont = max(dates).strftime('%d-%m-%Y')

				plan_d = dict()
				for k,v in plan_dic.items():
					d = {"montant dû":v,"montant payé":float(),"date":str(),
					"montant restant":v,"paiement associé":list()}
					plan_d[k] = d
				
				self.cmd_dict["plan de paiements"] = plan_d
				self.cmd_dict['date de traitement prévu'] = date_liv
				self.cmd_dict["type de contrat"] = self.type_contra
				self.cmd_dict['date de fin contrat'] = fin_cont
				self.cmd_dict["plan de remboursement"] = self.form_paie
				self.cmd_dict['durée du contrat'] = self.default_time
				self.cmd_dict['taux accompte'] = int(self.default_taux)
				self.excecute(self.sc.DB.Modif_this_cmd,self.cmd_dict)
				#self.sc.DB.Modif_this_cmd(self.cmd_dict)
				self.add_plan_paie()
				#self.sc.add_refused_error('Date de traitement définie, Plan de paiement aussi définie automatiquement')
		except:
			self.sc.add_refused_error('Erreur!! Veillez verrifier les informations saisies!')

	def set_default_time(self,wid,val):
		wid.text = self.regul_input(wid.text)
		if wid.text:
			self.default_time = round(float(wid.text))
		else:
			self.default_time = 0

	def redefinir(self,wid):
		if "écritures" in self.sc.DB.Get_access_of('Plan paiement'):
			self.TH_PLAN_D = self.cmd_dict.get('plan de paiements')
			self.cmd_dict['plan de paiements'] = dict()
			self.add_plan_paie()
		else:
			self.sc.add_refused_error("Impossible de continuer à cause d'une restriction système !! Parlez-en à votre supérieur hiérachique")

	def set_date_liv_(self):
		self.date_liv = self.day1
		self.Definir_plan()

	def set_date_ech(self):
		self.date_ech = self.day2
		self.Definir_plan()

	def set_type_contra(self,info):
		self.type_contra = info
		self.Definir_plan()

class paiem_surf(box):
	def __init__(self,mother,h,obj_paie,montant,info_w = .3,
		**kwargs):
		box.__init__(self,mother,**kwargs)
		self.obj_paie = obj_paie
		self.montant = montant
		self.orientation = "horizontal"

		self.add_all()

	@Cache_error
	def initialisation(self):
		self.clear_widgets()
		self.padding = dp(10)
		self.spacing = dp(10)
		self.montant_dic = dict()
		self.reference_dic = dict()
		self.this_pai_list = list()
		self.size_pos()

	def size_pos(self):
		h = dp(40)
		self.Tresorerie_part = box(self,bg_color = self.sc.aff_col1,
			radius = dp(10),padding = dp(10),spacing = dp(10),
			size_hint = (.7,1))
		b = box(self,size_hint = (1,None),height = dp(30),
			orientation = 'horizontal')
		b.add_text("Choisi le compte de trésorerie affecté",
			text_color = self.sc.text_col1,halign = 'center',
			underline = True,font_size = "16sp")
		b.add_icon_but(icon = "content-save",text_color = self.sc.orange,
			size_hint =(None,1),size = (dp(30),1),
			on_press = self.save_paie)
		self.Tresorerie_part.add_surf(b)
		self.Compte_surf = scroll(self)
		self.Tresorerie_part.add_surf(self.Compte_surf)
		self.montant_part = box(self,bg_color = self.sc.aff_col3,
			radius = dp(10),padding = dp(10),spacing = dp(10),
			size_hint = (.3,1))

		self.add_surf(self.Tresorerie_part)
		self.add_surf(self.montant_part)

	@Cache_error
	def Foreign_surf(self):
		self.add_Tress_part()
		self.add_montant_part()

	def add_Tress_part(self):
		h = dp(40)
		self.Compte_surf.clear_widgets()
		self.Get_compt_info()
		H = (h+dp(5))*len(self.Paie_cmt_dict)
		st = stack(self,size_hint = (1,None),height = H,
			spacing = dp(10))
		self.Compte_surf.add_surf(st)
		for info in self.Paie_cmt_dict:
			read = True
			txt_col = self.sc.text_col1
			bg_col = self.sc.aff_col3
			if info in self.this_pai_list:
				read = False
				txt_col = self.sc.green
				bg_col = self.sc.green
			b = box(self,size_hint = (1,None),spacing = dp(10),
				height = h,bg_color = self.sc.aff_col1,
				radius = dp(10),orientation = "horizontal")
			b.add_button('',size_hint = (None,None),width = dp(20),
				height = dp(20),on_press = self.set_cmpt,info = info,
				bg_color = bg_col,pos_hint = (0,.25))
			b.add_button(info,size_hint = (.45,1),on_press = self.set_cmpt,
				info = info,bg_color = self.sc.aff_col1,
				halign = "left",text_color = txt_col)
			b.add_input(info,default_text = str(self.montant_dic.get(info,str())),
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				padding_left = dp(10),readonly = read,on_text = self.set_mont_dic,
				placeholder = "Montant",size_hint = (.2,1))
			b.add_input(info,default_text = str(self.reference_dic.get(info,str())),
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				padding_left = dp(10),readonly = read,on_text = self.set_ref_dic,
				placeholder = "Déposant/Référence",size_hint = (.25,1))
			st.add_surf(b)

	def add_montant_part(self):
		h = .1
		self.montant_part.clear_widgets()
		b = box(self,size_hint = (1,h*2.5),padding = dp(10),
			radius = dp(10),bg_color = self.sc.aff_col1)
		b.add_text_input("Montant restant de la facture",(1,.45),(1,.55),
			self.sc.text_col1, bg_color = self.sc.aff_col3,
			text_color = self.sc.text_col1,
			default_text = self.format_val(self.montant),
			readonly = True,text_halign = 'center',
			halign = "center")
		self.montant_part.add_surf(b)
		b1 = box(self,size_hint = (1,h*2.5),padding = dp(10),
			radius = dp(10),bg_color = self.sc.aff_col1)
		b1.add_text('Montant payé',size_hint = (1,.45),
			text_color = self.sc.text_col1,halign = 'center')
		self.mont_paye = b1.add_text(str(),size_hint = (1,.55),
			text_color = self.sc.text_col1,halign = 'center')
		self.montant_part.add_surf(b1)

		b2 = box(self,size_hint = (1,h*2.5),padding = dp(10),
			radius = dp(10),bg_color = self.sc.aff_col1)
		b2.add_text('Montant restant',size_hint = (1,.45),
			text_color = self.sc.text_col1,halign = 'center')
		self.mont_rest = b2.add_text(str(),size_hint = (1,.55),
			text_color = self.sc.text_col1,halign = 'center')
		self.montant_part.add_surf(b2)
		
	def Get_compt_info(self):
		liste = self.sc.DB.Get_comptes_dict()
		self.Paie_cmt_dict = dict()
		for ident,dic in liste.items():
			if dic.get('actif'):
				Num = dic.get('N° de compte')
				inst = dic.get('institutions')
				typ = dic.get('type de compte')
				info = f"{typ} : {inst}({Num})"
				self.Paie_cmt_dict[info] = ident

# Gestion des actions des bouttons
	def valide_paie(self,cmd_ident,montant,cmp_ident):
		self.th_cmd_dic = self.sc.DB.Get_this_cmd(cmd_ident)
		#print(self.th_cmd_dic)
		cmpt_dic = self.sc.DB.Get_this_compte(cmp_ident)
		client = self.th_cmd_dic.get('client')
		dic = dict()
		dic['montant'] = montant
		dic['id commande'] = cmd_ident
		dic['client'] = client
		dic['comptes'] = cmp_ident
		dic['motif'] = "Règlement factures"
		dic['opérateur'] = self.sc.get_curent_perso()
		dic['référence'] = self.deposant
		self.sc.DB.save_recette(**dic)

		return True

	def Save_ecriture(self,dic,cmpt_dic,montant):
		...
	
	def save_paie(self,wid):
		self.sc.set_confirmation_srf(self.th_add_paie)
	
	@Cache_error
	def th_add_paie(self):
		for info in self.this_pai_list:
			cmp_ident = self.Paie_cmt_dict.get(info)
			if cmp_ident:
				mont = self.montant_dic.get(info)
				if mont:
					mont = float(mont)
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
		
		try:
			self.mother.close_modal()
		except AttributeError:
			self.mother.add_all()

	@Cache_error
	def custum_add_paie(self,cmp_ident,mont,deposant,
		cmd_ident,obj_paie):
		self.obj_paie = obj_paie
		if cmp_ident:
			self.deposant = deposant
			self.reference = deposant
		
			if mont < 0:
				if "écritures" in self.sc.DB.Get_access_of("Annuller un recouvrement"):
					...
				else:
					self.sc.add_refused_error("Vous ne pouvez pas annuller un recouvrement. Informer votre supérieur!")
					return
			ret = self.valide_paie(cmd_ident,mont,cmp_ident)
			
	def set_mont_dic(self,wid,val):
		wid.text = self.regul_input(wid.text)
		if wid.text:
			self.montant_dic[wid.info] = float(wid.text)
		else:
			self.montant_dic[wid.info] = 0

		self.up_mont_part()

	def up_mont_part(self):
		v = float()
		for k in self.this_pai_list:
			kk = self.montant_dic.get(k,float())
			if kk:
				v += float(kk)
		self.mont_paye.text = self.format_val(v)
		rest = self.montant - v
		if rest > 0:
			self.mont_rest.color = self.sc.red
		else:
			self.mont_rest.color = self.sc.green
		self.mont_rest.text = self.format_val(rest)

	def set_ref_dic(self,wid,val):
		self.reference_dic[wid.info] = val

	def set_cmpt(self,wid):
		info = wid.info
		if info in self.this_pai_list:
			self.this_pai_list.remove(info)
			self.up_mont_part()

		else:
			self.this_pai_list.append(info)
			self.up_mont_part()
		self.add_Tress_part()
