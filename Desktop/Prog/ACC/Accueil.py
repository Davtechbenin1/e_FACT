#Coding:utf-8
"""
	Interface de définition de la surface de l'accueil. Nous avons
	une partie surpérieur pour la définition des buttons d'actions utile,
	un histogramme de vente dynamique et une surface de notification
"""
from lib.davbuild import *
from General_surf import *
import copy
from ..CMPT.Ventes import Ventes,Factures
from ..CMPT.stock import stock
from ..CLT.Clients import client_part
from ..CREAN.cre_all_use import *
from ..CMPT.trs_surf2 import *
from ..CREAN.cre_surf2 import *

from .Infos_aff import *

from lib.kivy_dav.draw import *

#schedule_once

class Accueil(box):
	@Cache_error
	def initialisation(self):
		self.size_pos()

	@Cache_error
	def Foreign_surf(self):
		self.aff_surf.add_all()

	def size_pos(self):
		self.clear_widgets()
		w,h = self.buts_size = 1,.1
		self.aff_size = w,1-h

		self.aff_surf = Aff_surf(self,
			bg_color = self.sc.aff_col1,
			radius = dp(10))
		self.add_surf(self.aff_surf)
	
# Gestion des actions des bouttons
	
class Aff_surf(float_l):
	from .rac_tab_handler import (close_info_surf,show_art_rup,show_art_ale,
		show_art_per,show_art_cri,show_client_debit,show_creance_en_cour,
		show_creance_imp,show_eche_du_jour,show_eche_imp)
	@Cache_error
	def initialisation(self):
		self.size_pos()
		#self.add_image('media/accueil.png',keep_ratio = False,
		#	size_hint = (1,1),pos_hint = (0,0))
		self.All_surf = stack(self,
			size_hint = (1,1),pos_hint = (0,0),
			padding = dp(20),spacing = dp(20))
		self.th_but_surf = box(self,size_hint = (1,.55),
			padding = dp(30),spacing = dp(30),
			orientation = "horizontal")

		self.histo_part = stack(self,size_hint = (1,.45),
			padding = dp(10), spacing = dp(40))
		
		self.All_surf.add_surf(self.th_but_surf)
		self.All_surf.add_surf(self.histo_part)
		
		self.add_surf(self.All_surf)
		
		self.mult = 0
		self.suspended = list()

		self.article_infos = dict()
		self.ventes_infos = dict()
		self.recettes_infos = dict()
#
	def size_pos(self):
		self.part_size = (.33,.15)

	@Cache_error
	def Set_histo_surf(self,*args):
		self.histo_part.clear_widgets()
		date_restant = self.sc.get_in_progress()
		#if date_restant <= 30:
		b = stack(self,size_hint = (.2,.4),
			height = dp(100),radius = dp(20),
			bg_color = self.sc.aff_col1)
		Get_border_surf(self.histo_part,b,self.sc.orange,
			)
		b.add_button(f"Il vous reste [color=#EE2343]{date_restant} Jours[/color] pour que votre abonnement actuelle prenne fin. Veillez renouveller avec seulement [b]4900F CFA le Mois[/b], comme soutient au [i][b]projet GSmart[/b][/i].!",
			halign = 'justify',bg_color = None,
			on_press = self.show_param,
			padding = dp(10))

		if self.info_dict:
			for part, dic in self.info_dict.items():
				if part not in self.suspended:
					if dic:
						txt = self.get_alert_info(part,len(dic))
						fonc,col,icon = self.get_alert_fonc(part)
						self.add_alerte_surf(part,txt,fonc,
							color = col,icon = icon)

	def add_alerte_surf(self,titre, info, fonc,color = None,
		icon = "information"):
		if not color:
			color = self.sc.red
		b = stack(self,size_hint = (.2,.4),spacing = dp(1),
			radius = dp(20),padding_top = dp(10),bg_color = self.sc.aff_col1)
		th_b = Get_border_surf(self.histo_part,b,color)
		th_b.add_icon_but(icon = icon,size_hint = (.1,None),
			size = (dp(30),dp(40)),text_color = color,)
		th_b.parent.part = titre
		th_b.add_text(titre, text_color = color,
			size_hint = (.8,None),height = dp(40),
			font_size = '15sp',valign = 'middle')
		th_b.add_icon_but(icon = 'close',on_press = self.close_info_surf,
			info = th_b.parent, size_hint = (.1,None),size = (dp(30),dp(30)))
		info_srf = th_b.add_button(info,text_color = self.sc.text_col1,
			valign = 'top',halign = 'left',
			bg_color = None,on_press = fonc,padding_left =dp(10),
			padding_right = dp(10))
		return info_srf

	def get_alert_info(self,part,qte):
		txt = "(Cliquez ici pour avoir le détails)"
		dic = {
			"Articles en ruptures":f"Vous avez actuellement {qte} articles en ruptures {txt}",
			"Stock critique":f"Vous avez actuellement {qte} articles dont le stock est critique {txt}",
			"Articles périmés":f"Vous avez actuellement {qte} articles périmés {txt}",
			"Articles en état d'alerte":f"Vous avez actuellement {qte} dont la date d'expiration est très proche {txt}",

			"Clients débiteurs":f"Il y a actuellement {qte} clients débiteurs dans la base {txt}", 
			"Créances en cours":f"Vous avez {qte} créance en cours. Contactez-les de temps en temps pour éviter les impayées {txt}",
			"Créances impayées":f"Alerte Critique. {qte} sont en impayées {txt}",
			"Echéances du jours":f"Aujourd'hui {qte} doit payer. Veillez les contacter {txt}",
			"Echéances non respectées":f"Il y a {qte} échéance non respectées. {txt}"
		}
		return dic.get(part,str())
#
	def get_alert_fonc(self,part):
		fonc_dict = {
			"Articles en ruptures":(self.show_art_rup,self.sc.red,"alert"),
			"Stock critique":(self.show_art_cri,self.sc.green,"information"),
			"Articles périmés":(self.show_art_per,self.sc.red,"alert"),
			"Articles en état d'alerte":(self.show_art_ale,self.sc.green,"alert"),

			"Clients débiteurs": (self.show_client_debit,self.sc.orange,"alert"),
			"Créances en cours": (self.show_creance_en_cour,self.sc.green,"information"),
			"Créances impayées": (self.show_creance_imp,self.sc.red,"information"),
			"Echéances du jours": (self.show_eche_du_jour,self.sc.green,"alert"),
			"Echéances non respectées": (self.show_eche_imp,self.sc.orange,"information"),
		}
		return fonc_dict.get(part,None)

	@Cache_error
	def get_art_qte(self,art_dic):
		ident = self.sc.magasin
		cond_d = art_dic.get("conditionnement")
		stock = (art_dic.get('stocks',dict())).get(ident,{i:float() 
			for i in cond_d.keys()})
		return stock

	def repart_stock(self):
		stock_gene = self.sc.DB.Get_article_list_dict()
		art_en_rup = dict()
		art_nn_rup = dict()
		art_perime = dict()
		art_critiq = dict()
		for art_dic in stock_gene.values():
			seuil = float(art_dic.get("seuil d'approvisionnement"))
			qte_dic = self.get_art_qte(art_dic)
			qte_str = str()
			ven_str = str()
			
			qte = qte_dic.get(art_dic.get('stockage'),int())
			for k,v in qte_dic.items():
				qte_str+=f"[b][i]{v}[/b][/i] {k} "
			for k,v in art_dic.get('vente').items():
				ven_str+=f"[b][i]{v}[/b][/i] {k} "
			art_dic['reale stock'] = qte_str
			art_dic['Vente total'] = ven_str
			if 0 < qte <= seuil:
				art_nn_rup[art_dic.get('N°')] = art_dic
			elif qte <= float():
				art_en_rup[art_dic.get('N°')] = art_dic

		self.info_dict = {
			"Articles en ruptures":art_en_rup,
			"Stock critique":art_nn_rup,
			"Articles périmés":art_perime,
			"Articles en état d'alerte":art_critiq,
		}

	def repart_client(self):
		clients = self.sc.DB.get_client()
		clts = {dic.get('N°'):dic for dic in clients.values() 
			if dic.get("solde") > 0}
		self.info_dict["Clients débiteurs"] = clts

	def repart_creances(self):
		impayer = {dic.get("N°"):dic for dic in self.sc.DB.Get_cmd_impayer().values()}
		encours = {dic.get("N°"):dic for dic in self.sc.DB.Get_cmd_encours().values()}
		self.info_dict["Créances en cours"] = encours
		self.info_dict["Créances impayées"] = impayer

	def repart_echeances(self):
		self.eche_enc = dict()
		self.eche_imp = dict()
		all_cmds = self.sc.DB.Get_cmd_non_sold()
		for cmd_dic in all_cmds.values():
			self.edite_cmd(cmd_dic)
		self.info_dict["Echéances du jours"] = self.eche_enc
		self.info_dict['Echéances non respectées'] = self.eche_imp

	def edite_cmd(self,cmd_dic):
		if cmd_dic.get('status de la commande') == "Livrée":
			cmd_dic = dict(cmd_dic)
			plan_paie = cmd_dic.get("plan de paiements")
			th_day = datetime.strptime(self.sc.get_today(),self.date_format)
			montant_impay = float()
			nbre_impay = int()
			encoure = float()
			ind = 1
			#print(plan_paie)
			for date,dic in plan_paie.items():
				th_date = datetime.strptime(date,self.date_format)
				if th_day > th_date:
					if dic.get("montant restant"):
						nbre_impay += 1
						montant_impay += float(dic.get('montant restant'))
					else:
						ind += 1
				elif th_day == th_date:
					encoure = dic.get('montant restant')

			cmd_dic["montant de l'échéance"] = encoure
			cmd_dic["échéance échus non payé"] = montant_impay
			cmd_dic["nombre d'impayé"] = nbre_impay

			cmd_dic["Echéance N°"] = ind

			cmd_dic['Montant total de la commande'] = cmd_dic.get('montant TTC')
			cmd_dic['Montant total payé'] = cmd_dic.get('montant payé')
			cmd_dic['Montant total restant'] = cmd_dic.get('montant restant')

			cmd_dic["total à payer ce jours"] = encoure + montant_impay
			cmd_dic["PAYEE"] = str()
			
			clt_dic = self.sc.DB.Get_this_clt(cmd_dic.get('client'))
			cmd_dic['Code client'] = clt_dic.get('N°')
			cmd_dic['Nom du client'] = f"{clt_dic.get('nom')} {clt_dic.get('prénom')}".strip()
			cmd_dic["date d'achat"] = cmd_dic.get('date de livraison')
			#cmd_dic["affiliation"] = self.sc.DB.Get_this_association(clt_dic.get("association appartenue")).get('nom',str())
			cmd_dic["catégorie"] = cmd_dic.get('type de contrat')
			
			if encoure:
				self.eche_enc[cmd_dic.get('N°')] = cmd_dic
			if nbre_impay:
				self.eche_imp[cmd_dic.get('N°')] = cmd_dic

	@Cache_error
	def Foreign_surf(self,*args):
		#self.excecute(self.Aff_2)
		
		self.Aff_2()
	
	def Aff_2(self):
		self.Aff_1()
		self.sc.DB.Partage_hist()
		self.repart_stock()
		self.repart_client()
		self.repart_creances()
		self.repart_echeances()
		Clock.schedule_once(self.Set_histo_surf,2)
#
	def Aff_1(self):
		date_liste = self.sc.get_7_days()
		self.set_infos(date_liste)
		fic_lis = self.get_pic(date_liste)
		#self.add_part_button(fic_lis,0)
		Clock.schedule_once(partial(self.add_part_button,fic_lis),.1)

	def get_pic(self,date_liste):
		fic1 = get_fig_plot_of([self.ventes_infos.get('Crédit',dict()),
			self.ventes_infos.get('Comptant',dict())],
			[self.get_day_only(date) for date in date_liste],
			"Historique des ventes",str(),'Montant total vendu',
			("Crédit","Comptant"),col_dict = {"Crédit":"red",'Comptant':'green'})
		fic2 = get_fig_hist_of([self.recettes_infos],
			[self.get_day_only(date) for date in date_liste],
			"Historique des recettes",str(),"",
			label = 'Recettes')

		
		return fic1,fic2

	def add_part_button(self,fics,dt):
		self.th_but_surf.clear_widgets()
		for fic in fics:
			self.th_but_surf.add_image(fic)

	def set_infos(self, date_liste):
		all_dic = dict()
		template = {			
			"montant total": 0.0,
		}

		cache_articles = {}

		for th_date in date_liste:
			cmd_infos = self.sc.DB.Get_all_commandes(th_date)
			#print(cmd_infos)
			for num in cmd_infos.keys():
				cmd_dic = self.sc.DB.Get_this_cmd(num)
			#	print(cmd_dic)
			#	print()
				if cmd_dic.get('status de la commande') != "Livrée":
					continue

				date = cmd_dic.get("date d'émission")
				this_date_d = all_dic.get(date, copy.deepcopy(template))
				this_date_d["date"] = date
				this_date_d['DATE'] = datetime.strptime(date,self.date_format)

				for art in cmd_dic.get('articles', []).values():
					art_name = art.get('Désignation')

					art_d = cache_articles.get(art_name)
					if not art_d:
						art_d = self.sc.DB.Get_this_article(art_name)
						cache_articles[art_name] = art_d
					if art_d:
						# Quantité
						qte = self.sc.DB.acurate_stock(art_d.get('vente'),
							art_d.get('conditionnement'))
						th_q = self.article_infos.setdefault(art_name,0)
						th_q += qte
						self.article_infos[art_name] = th_q

				status = cmd_dic.get("status de la facture")
				status_dic = self.ventes_infos.setdefault(status,{})
				th_date_of = self.get_day_only(date)
				montant = status_dic.setdefault(th_date_of,0)
				montant += cmd_dic.get('montant TTC')
				status_dic[th_date_of] = montant

		all_paie_liste = self.sc.DB.Get_all_paiement_of(date_liste)
		for paie_dic in all_paie_liste.values():
			date = paie_dic.get("date")
			th_date_of = self.get_day_only(date)
			day_mont = self.recettes_infos.setdefault(th_date_of,0)
			day_mont += paie_dic.get('montant')
			self.recettes_infos[th_date_of] = day_mont

	def get_day_only(self,date):
		j,m,y = date.split('-')
		day = f"{j}-{m}"
		return day

	def add_rac_tab(self,entete,wid_l,liste,titre):
		def print_info(*args):
			info = 'Agence TOKPOTA1'
			obj = self.sc.imp_part_dic('Résumé')(self)
			obj.Create_fact(wid_l,entete,liste,
				titre,info)

		th_tab = Table(self)
		srf = box(self)
		b = box(self,orientation = 'horizontal',
			size_hint = (1,None),height = dp(30))
		b.add_icon_but(icon = 'printer',on_press = print_info,
			text_color = self.sc.black,size_hint = (None,1),
			size = (dp(30),dp(30)))
		b.add_button("Impression",on_press = print_info,
			bg_color = None,halign = 'left',
			text_color = self.sc.black)
		srf.add_surf(b)
		srf.add_surf(th_tab)
		
		self.add_modal_surf(srf,size_hint = (.8,.8),
			titre = titre)
		th_tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.08))
		#self.modal.open()


# Gestion des actions des méthodes
	def get_art_info(self,art_d):
		th_d = dict()
		nbr_qte = art_d.get('nbre_par_qté')
		if not nbr_qte:
			nbr_qte = 1
		nbr_qte = int(nbr_qte)
		th_d['N°'] = art_d.get('N°')
		th_d['Famille'] = art_d.get('famille')
		th_d['Désignation'] = art_d.get('nom').replace('_',' ')
		th_d['Activitée récente'] = art_d.get('dernier activité')
		th_d['Stock actuel'] = art_d.get("reale stock")
		th_d['Vente total'] = art_d.get("Vente total")
		return th_d

	def show_param(self,wid):
		self.sc.th_root.Aff_surf.menu_in_action = "Upgrade"
		self.sc.th_root.Aff_surf.add_all()




class Th_info_surf(stack):
	@Cache_error
	def initialisation(self):
		self.liste = (text1,text2,text3)
		self.curent_ = self.sc.curent_info_show
		if self.curent_ >= len(self.liste):
			self.sc.curent_info_show = 0
			self.curent_ = 0

		self.txt = self.liste[self.curent_]
		W = len(self.txt) * dp(10)
		#print(W)
		self.my_sur = stack(self,size_hint = (None,1),
			width = W)
		self.my_sur.add_text(self.txt,text_color = self.sc.text_col1,
			width = dp(10),padding_left = dp(20),
			font_size = "17sp")
		self.add_surf(self.my_sur)
		Clock.schedule_interval(self.add_text_of,.05)

	def add_text_of(self,*args):
		try:
			self.my_sur.x-=2
			
			self.sc.curent_seek += .25
			if self.sc.curent_seek >= len(self.txt):
				self.sc.curent_seek = 0
				self.sc.curent_info_show += 1
				self.curent_ += 1
				if self.curent_ >= len(self.liste):
					self.sc.curent_info_show = 0
					self.curent_ = 0
				self.txt = self.liste[self.curent_]
				W = len(self.txt) * dp(10)
				self.my_sur.clear_widgets()
				self.my_sur.x = 0
				self.my_sur.width = W
				self.my_sur.add_text(self.txt,
					text_color = self.sc.text_col1,
					width = dp(10),padding_left = dp(20),
					font_size = "17sp")
		except:
			...


	
