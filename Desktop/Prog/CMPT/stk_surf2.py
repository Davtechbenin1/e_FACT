#Coding:utf-8
"""
	Gestion de la surface de gestion des autres parties
	du stock outre que la gestion des articles
"""
from .stk_surf import *

class Invent_hand(Appro_surf):
	def init_infos(self):
		self.magasin = self.sc.magasin
		self.article_dic = dict()
		self.article_name = str()
		self.curent_art_name = str()
		self.curent_art_ident = str()

		self.montant_total = float()
		self.taxes = float()

		self.curent_art_param = dict()
		self.motif = str()

		self.montant_srf = None

		self.magasin_list = [self.sc.magasin]

	def add_entete_surf(self):
		self.entete_surf.clear_widgets()
		self.entete_surf.add_text('Magasin',size_hint = (.07,1))
		self.entete_surf.add_surf(liste_set(self,self.magasin,
			self.magasin_list,
			mother_fonc = self.set_magasin,
			size_hint = (.15,1)))
		Get_border_input_surf(self.entete_surf,"Motif de l'inventaire",
			size_hint = (.3,1),border_col = self.sc.green,
			bg_color = self.sc.aff_col1,on_text = self.set_motif,
			)

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

			mag_id = self.sc.DB.Get_this_magasin(self.magasin).get("N°")

			curent_art_param = {
				"Désignation":curent_art.get('Désignation'),
				"N°":ident,
				"img":curent_art.get('img'),
				"stock précédent":curent_art.get("stocks").get(mag_id,
					{cond:float() for cond in art_conds.keys()}),
				"stock compté":{cond:float() for cond in art_conds.keys()},
				"prix de vente":curent_art.get('prix de vente'),
				"conditionnement":art_conds,
			}
			return curent_art_param
		return None

	def add_article_tab(self):
		self.add_paramet_srf()
		entete = ["Désignation","Stock précédent","Stock compté",'Différences',
		"Valeur monétaire"]
		wid_l = [.2,.25,.25,.2,.1]
		liste = self.get_th_article_list()
		self.article_tab.Creat_Table(wid_l,entete,list(liste),
			mult = .1)
		if self.montant_srf:
			self.montant_srf.text = self.format_val(self.montant_total)

	def add_paramet_srf(self):
		self.paramet_srf.clear_widgets()
		self.curent_art_param = self.set_curent_art_param()
		self.add_button_srf()
		h = dp(50)
		if self.curent_art_name:
			acht_dic = self.curent_art_param.get('stock compté')
			prix_ven = self.curent_art_param.get("stock précédent")
			for cond,qte in acht_dic.items():
				self.paramet_srf.add_text("stock compté du "+cond,
					size_hint = (.2,None),
					height = h, halign = 'right')
				self.paramet_srf.add_input(f"{cond}",
					placeholder = "Quantité",
					default_text = str(qte),
					size_hint = (.3,None),
					height = h,on_text = self.set_qte_achat)
				self.paramet_srf.add_text(f'stock précédent du {cond}',
					size_hint = (.2,None),
					height = h, halign = 'right')
				self.paramet_srf.add_input(f"{cond}",
					default_text = str(prix_ven.get(cond)),
					size_hint = (.3,None),height = h,
					on_text = self.set_prix_achat,
					readonly = True,placeholder = "Prix d'achat")

# Gestion des actions des boutons
	def _save_art_param(self):
		article_dic = dict(self.article_dic)
		invent_dic = self.sc.DB.Get_invent_format()
		invent_dic['magasin'] = self.sc.DB.Get_this_magasin(self.magasin).get('N°')
		invent_dic['motif'] = self.motif
		invent_dic['articles'] = article_dic
		montant_total = int()
		for art_d in article_dic.values():
			montant_total += art_d.get('Valeur monétaire',int())
		invent_dic["résultat de l'inventaire"] = montant_total
		self.sc.DB.Save_inventaire(invent_dic)
		self.init_infos()
		self.add_all()

	def add_art_param(self,wid):
		th_b = dict(self.curent_art_param)
		cond = th_b.get('conditionnement')
		qte = self.sc.DB.correct_stock(th_b.get('stock compté'),cond)
		vent = th_b.get("stock précédent")
		th_vent = th_b.get('prix de vente')
		
		diff = self.sc.DB.correct_stock(
			{key:(val-vent.get(key,int())) 
			for key,val in qte.items()},cond)
		th_b["Stock compté"] = self.sc.get_info_str(qte)
		th_b["Stock précédent"] = self.sc.get_info_str(vent)
		th_b['Différences'] = self.sc.get_info_str(diff)
		th_b['résultat'] = diff
		th_b['Valeur monétaire'] = self.get_montant(diff,th_vent)
		th_b['Montant'] = float()

		self.article_dic[th_b.get('N°')] = th_b
		self.article_list_srf.info = str()
		self.article_list_srf.add_all()
		self.curent_art_name = dict()
		self.add_article_tab()

	def set_motif(self,wid,val):
		self.motif = val

	def set_qte_achat(self,wid,val):
		cond = wid.info
		wid.text = self.regul_input(wid.text)
		self.curent_art_param["stock compté"][cond] = float(wid.text)

class Magasin_hand(box):
	def initialisation(self):
		self.size_pos()
		self.init_infos()

	def size_pos(self):
		self.clear_widgets()
		self.liste_magasin_srf = stack(self,size_hint = (1,.6),
			bg_color = self.sc.aff_col3,radius = [0,0,dp(30),dp(30)],
			padding = dp(30),spacing = dp(30))
		Get_border_surf(self,self.liste_magasin_srf,
			self.sc.green)
		self.buttons_part_srf = stack(self,size_hint = (1,.4),
			bg_color = self.sc.aff_col1,spacing = dp(30),
			padding = dp(30))
		self.add_surf(self.buttons_part_srf)

	def Foreign_surf(self):
		self.init_infos()
		self.add_liste_magasin_srf()
		self.add_button_part_srf()

	def init_infos(self):
		self.all_magasin_dic = self.sc.DB.Get_general_dict()
		self.but_dic = {
			"Transfert entre magasins":'plus',
			"Stocks par magasins":'plus',
			"Historique des transferts":'history'
		}

	def add_liste_magasin_srf(self):
		h = .25
		self.liste_magasin_srf.clear_widgets()
		for dic in self.all_magasin_dic.values():
			bo = float_l(self,size_hint = (.2,h),
				bg_color = self.sc.aff_col1,
				radius = dp(10))
			Get_border_surf(self.liste_magasin_srf,bo,
				self.sc.orange)
			th_b = box(self,padding = dp(10))
			th_b.add_text(dic.get('nom'),text_color = self.sc.green,
				size_hint = (1,.33),halign = "center",bold = True,
				italic = True, font_size = "17sp")
			th_b.add_text(f"""Nbre d'arcticles: [b][i]{self.format_val(
				dic.get("nombre d'articles"))}[/b][/i]""",
				font_size = "15sp",size_hint = (1,.33))
			th_b.add_text(f"""Valeur monétaire: [b][i]{self.format_val(
				dic.get("valeur monétaire"))}[/b][/i]""",
				font_size = "15sp",size_hint = (1,.33))
			bo.add_surf(th_b)
			bo.add_button("",bg_color = None,
				on_press = self.show_magasin,
				info = dic.get('nom'))

		bo = box(self,size_hint = (.2,h),
			bg_color = self.sc.aff_col1,
			radius = dp(10),orientation = 'horizontal')
		Get_border_surf(self.liste_magasin_srf,bo,
			self.sc.orange)
		bo.add_icon_but(icon = "plus",size_hint = (None,None),
			size = (dp(30),dp(30)),on_press = self.new_magasin,
				font_size = "24sp")
		bo.add_button("Nouveau magasin",halign = 'left',
			bold = True,italic = True,font_size = '15sp',
			on_press = self.new_magasin)


	def add_button_part_srf(self):
		self.buttons_part_srf.clear_widgets()
		h = .3
		for txt,icon in self.but_dic.items():
			bo = box(self,size_hint = (.2,h),
				bg_color = self.sc.aff_col1,
				radius = dp(10),orientation = 'horizontal')
			Get_border_surf(self.buttons_part_srf,bo,
				self.sc.orange)
			bo.add_icon_but(icon = icon,size_hint = (None,None),
				size = (dp(30),dp(30)),on_press = self.show_part,
				font_size = "24sp")
			bo.add_button(txt,halign = 'left',
				bold = True,italic = True,font_size = '15sp',
				on_press = self.show_part)

# Gestion des actions des boutons
	def show_magasin(self,wid):
		self.th_magasin = self.all_magasin_dic.get(wid.info)
		srf = Show_Magasin(self,bg_color = self.sc.aff_col1)
		self.add_modal_surf(srf,size_hint = (.3,.4),
			titre = self.th_magasin.get("N°"))

	def new_magasin(self,wid):
		srf = New_Magasin(self,bg_color = self.sc.aff_col1)
		self.add_modal_surf(srf,size_hint = (.3,.4),
			titre = "Nouveau magasin")

	def show_part(self,wid):
		if wid.info == "Transfert entre magasins":
			srf = transfert_entre_mag(self,bg_color = self.sc.aff_col1)
		elif wid.info == "Stocks par magasins":
			srf = stock_par_magasin(self,bg_color = self.sc.aff_col1)
		elif wid.info == "Historique des transferts":
			srf = trans_history_hand(self,bg_color = self.sc.aff_col1)
		else:
			srf = box(self)
		srf.add_all()
		self.add_modal_surf(srf,size_hint = (.8,.85),
		titre = wid.info)

class Show_Magasin(stack):
	def initialisation(self):
		h = .15
		self.padding = dp(10)
		self.spacing = dp(10)
		self.th_magasin = self.mother.th_magasin
		self.add_text('nom',size_hint = (.3,h*.7),
			)
		Get_border_input_surf(self,'nom',(.6,h*.8),
			border_col = self.sc.orange,
			bg_color = self.sc.aff_col1,
			on_text = self.set_mag_nom,
			default_text = self.th_magasin.get("nom"),
			placeholder = "Nom du magasin")
		self.add_icon_but(icon = "content-save-alert",
			size_hint = (.1,h),on_press = self.modif_mag,
			text_color = self.sc.orange,
			)
		
		self.add_text("Nbres d'articles",size_hint = (.3,h*.7))
		Get_border_input_surf(self,'nom',(.68,h*.7),
			border_col = self.sc.green,
			bg_color = self.sc.aff_col1,
			on_text = self.set_mag_nom,
			readonly = True,
			default_text = self.th_magasin.get(
				"nombre d'articles"))
		self.add_padd((.02,h))
		
		self.add_text("Valeur monétaire",size_hint = (.3,h*.7))
		Get_border_input_surf(self,'nom',(.68,h*.7),
			border_col = self.sc.green,
			bg_color = self.sc.aff_col1,
			on_text = self.set_mag_nom,
			readonly = True,
			default_text = self.th_magasin.get(
				"valeur monétaire"))
		self.add_padd((.02,h*.7))
		
		self.add_text("Stocks général",size_hint = (1,h*.7),
			valign = 'bottom',bold = True,italic = True)
		self.add_padd((.025,h*.7))
		stk_gene = self.get_quantite_total()
		if not stk_gene:
			b = Get_border_surf(self,box(self,size_hint = (.95,h*1.5),
				bg_color = self.sc.aff_col1,radius = dp(20),
				padding = dp(10)),self.sc.green)
			b.add_text(self.sc.get_info_str(
					stk_gene),
				valign = "top")
		
			self.add_padd((.3,h))
			self.add_button('Supprimer',text_color = self.sc.white,
				bg_color = self.sc.red,on_press = self.delete,
				info = self.th_magasin.get('N°'),
				size_hint = (.4,h*.8))
		else:
			b = Get_border_surf(self,box(self,size_hint = (.95,h*2),
				bg_color = self.sc.aff_col1,radius = dp(20),
				padding = dp(10)),self.sc.green)
			b.add_text(self.sc.get_info_str(
					stk_gene),
				valign = "top")

	def get_quantite_total(self):
		article_liste = self.th_magasin.get('listes des articles')
		mag_ident = self.th_magasin.get('N°')
		stk_gene = {}
		if article_liste:
			for num in article_liste:
				art_d = self.sc.DB.Get_this_article(num)
				stk = art_d.get("stocks").get(mag_ident)
				for cond,val in stk.items():
					th_val = stk_gene.setdefault(cond,int())
					th_val+=val
					stk_gene[cond] = th_val
		return stk_gene

# Gestion des actions des bouttons
	def set_mag_nom(self,wid,val):
		if val:
			self.th_magasin["nom"] = val

	def modif_mag(self,wid):
		self.sc.set_confirmation_srf(self._modif_mag)

	def _modif_mag(self):
		self.sc.DB.Save_magasin(self.th_magasin)
		self.mother.close_modal()

	def delete(self,wid):
		self.sc.set_confirmation_srf(self._delete)

	def _delete(self):
		self.sc.DB.delete_magasin(self.th_magasin)
		self.mother.close_modal()

class New_Magasin(Show_Magasin):
	def initialisation(self):
		h = .15
		self.padding = dp(10)
		self.spacing = dp(10)
		self.th_magasin = dict()
		self.add_padd((1,.25))
		self.add_text('nom',size_hint = (.3,h),
			)
		Get_border_input_surf(self,'nom',(.6,h),
			border_col = self.sc.orange,
			bg_color = self.sc.aff_col1,
			on_text = self.set_mag_nom,
			placeholder = "Nom du magasin")
		th_b = self.add_icon_but(icon = "content-save",
			size_hint = (.1,h),on_press = self.modif_mag,
			text_color = self.sc.orange,
			)
		self.sc.set_default_button(th_b)

	def _modif_mag(self):
		dic = self.sc.DB.Get_magasin_format()
		dic['nom'] = self.th_magasin.get('nom')
		self.sc.DB.Save_magasin(dic)
		self.mother.initialisation()
		self.mother.close_modal()
	
class transfert_entre_mag(Appro_surf):
	def init_infos(self):
		self.magasin1 = self.sc.magasin
		self.magasin2 = self.sc.DB.Get_magasin_list()[-1]
		self.article_dic = dict()
		self.article_name = str()
		self.curent_art_name = str()
		self.curent_art_ident = str()

		self.montant_total = float()
		self.taxes = float()

		self.curent_art_param = dict()
		self.motif = str()

		self.montant_srf = None

		self.magasin_list = self.sc.DB.Get_magasin_list()

	def add_entete_surf(self):
		self.entete_surf.clear_widgets()
		self.entete_surf.add_text("Magasin source",size_hint = (.1,1))
		self.entete_surf.add_surf(liste_set(self,self.magasin1,
			self.magasin_list,
			mother_fonc = self.set_magasin1,
			size_hint = (.15,1)))
		self.entete_surf.add_text("Magasin destination",size_hint = (.1,1))
		self.entete_surf.add_surf(liste_set(self,self.magasin2,
			self.magasin_list,
			mother_fonc = self.set_magasin2,
			size_hint = (.15,1)))
		Get_border_input_surf(self.entete_surf,"Motif du transfert",
			size_hint = (.3,1),border_col = self.sc.green,
			bg_color = self.sc.aff_col1,on_text = self.set_motif,
			)

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

			mag_id = self.sc.DB.Get_this_magasin(self.magasin1).get("N°")

			curent_art_param = {
				"Désignation":curent_art.get('Désignation'),
				"N°":ident,
				"img":curent_art.get('img'),
				"stock actuel":curent_art.get("stocks").get(mag_id,
					{cond:float() for cond in art_conds.keys()}),
				"prix de vente":curent_art.get('prix de vente'),
				"conditionnement":art_conds,
				"destockage":{cond:float() for cond in art_conds.keys()},
			}
			return curent_art_param
		return None

	def add_article_tab(self):
		self.add_paramet_srf()
		entete = ["Désignation","Destockage","Stock restant",'Montant']
		wid_l = [.3,.3,.3,.1]
		liste = self.get_th_article_list()
		self.article_tab.Creat_Table(wid_l,entete,list(liste),
			mult = .1)
		if self.montant_srf:
			self.montant_srf.text = self.format_val(self.montant_total)

	def add_paramet_srf(self):
		self.paramet_srf.clear_widgets()
		self.curent_art_param = self.set_curent_art_param()
		self.add_button_srf()
		h = dp(50)
		if self.curent_art_name:
			acht_dic = self.curent_art_param.get('destockage')
			prix_ven = self.curent_art_param.get("stock actuel")
			for cond,qte in acht_dic.items():
				self.paramet_srf.add_text(cond,
					size_hint = (.2,None),
					height = h, halign = 'right')
				self.paramet_srf.add_input(f"{cond}",
					placeholder = "Quantité",
					default_text = str(qte),
					size_hint = (.3,None),
					height = h,on_text = self.set_qte_achat)
				self.paramet_srf.add_text(f'stock actuel du {cond}',
					size_hint = (.2,None),
					height = h, halign = 'right')
				self.paramet_srf.add_input(f"{cond}",
					default_text = str(prix_ven.get(cond)),
					size_hint = (.3,None),height = h,
					on_text = self.set_prix_achat,
					readonly = True,placeholder = "stock actuel")

# Gestion des actions des boutons
	def _save_art_param(self):
		if not self.motif:
			transf_dic = self.sc.DB.Get_transfert_formt()
			mag1_ident = self.sc.DB.Get_this_magasin(self.magasin1).get('N°')
			mag2_ident = self.sc.DB.Get_this_magasin(self.magasin2).get('N°')
			transf_dic['magasin source'] = mag1_ident
			transf_dic['magasin destination'] = mag2_ident
			transf_dic['motif'] = self.motif
			article_dic = dict(self.article_dic)
			transf_dic['articles'] = article_dic
			montant_total = int()
			qte_dict = dict()
			for art_d in article_dic.values():
				montant_total += art_d.get('Montant',int())

				qte = art_d.get('destockage')
				for k,v in qte.items():
					val = qte_dict.setdefault(k,int())
					val += v
					qte_dict[k] = val
			
			transf_dic["valeur monétaire"] = montant_total
			transf_dic['quantités'] = qte_dict
			self.sc.DB.Save_transfert_magasin(transf_dic)
			self.init_infos()
			self.add_all()
		else:
			self.sc.add_refused_error("Le motif est obligatoire")

	def add_art_param(self,wid):
		th_b = dict(self.curent_art_param)
		qte = th_b.get('destockage')
		qte_act = th_b.get("stock actuel")
		vent = th_b.get("prix de vente")
		th_b["Destockage"] = self.sc.get_info_str(qte)
		th_b["Stock restant"] = self.sc.get_info_str(
			self.get_stk_rest(qte_act,qte,th_b.get('conditionnement')))
		th_b['Montant'] = self.get_montant(qte,vent)
		self.article_dic[th_b.get('N°')] = th_b
		self.article_list_srf.info = str()
		self.article_list_srf.add_all()
		self.curent_art_name = dict()
		self.add_article_tab()

	def get_stk_rest(self, stk_act, deskt, cond):
		stk_rest = {key:(val - deskt.get(key)) 
			for key,val in stk_act.items()}
		return self.sc.DB.correct_stock(stk_rest,cond)

	def set_motif(self,wid,val):
		self.motif = val

	def set_magasin1(self,info):
		self.magasin1 = info

	def set_magasin2(self,info):
		self.magasin2 = info

	def set_qte_achat(self,wid,val):
		cond = wid.info
		wid.text = self.regul_input(wid.text)
		self.curent_art_param["destockage"][cond] = float(wid.text)

class stock_par_magasin(art_list):
	def size_pos(self):
		self.entete_surf = stack(self,size_hint = (1,.045),
			spacing = dp(10),
			bg_color = self.sc.aff_col1)
		self.corps_surf = Table(self,size_hint = (1,.95),
			bg_color = self.sc.aff_col3,radius = dp(10),
			exec_fonc  = self.on_show_art,
			exec_key = 'nom',padding = dp(10))
		self.add_surf(self.entete_surf)
		self.add_surf(self.corps_surf)

	@Cache_error
	def add_entete(self):
		h = 1
		self.entete_surf.clear_widgets()
		self.entete_surf.add_text('Magasins :',size_hint = (.07,h),
			text_color = self.sc.text_col1)
		self.entete_surf.add_surf(liste_set(self,self.magasin,
			self.sc.DB.Get_magasin_list(),orientation = 'H',
			size_hint = (.12,h),mult = 2,
			mother_fonc = self.set_magasin))
		
		b = box(self,radius = dp(10),
			bg_color = self.sc.aff_col3,
			orientation = 'horizontal',
			padding = dp(5),size_hint = (.25,1))
		b = Get_border_surf(self.entete_surf,b,self.sc.green)
		b.add_icon_but(icon = 'magnify',
			text_color = self.sc.black,
			size_hint = (None,h),size = (dp(30),dp(1)))
		b.add_input("Search",
			text_color = self.sc.text_col1,
			default_text = self.Search_text,
			bg_color = self.sc.aff_col3,
			size_hint = (.9,1),
			placeholder = "Le nom de l'article",
			on_text = self.setting_search_txt)
		self.entete_surf.add_icon_but(icon = 'printer',
			size_hint = (.03,h),
			size = (dp(30),dp(30)),text_color = self.sc.black,
			on_press = self.Impression)

	@Cache_error
	def Impression(self,wid):
		obj = self.sc.imp_part_dic('Résumé')(self)
		liste = self.Get_this_art_list_()
		entete = ["Désignation","Stock actuel",
			"Stock compté"]
		wid_l = [.35,.35,.3]
		info = str()
		if self.magasin:
			info += f'Magasin : {self.magasin}<br/>'
		titre = f"Fiche de stock"
		obj.Create_fact(wid_l,entete,liste,titre,info)

class trans_history_hand(box):
	def initialisation(self):
		self.size_pos()
		self.motif_trans = str()
		self.magasin_src = str()
		self.magasin_des = str()

	def size_pos(self):
		self.entete_surf = stack(self,size_hint = (1,.06),
			padding = dp(5),spacing = dp(10))
		self.history_tab = Table(self,size_hint = (1,.94),
			exec_key = "N°",exec_fonc = self.show_transfert_det)
		self.add_surf(self.entete_surf)
		self.add_surf(self.history_tab)

	def Foreign_surf(self):
		self.add_entete_surf()
		self._trie_tab()

	def add_entete_surf(self):
		h = 1
		self.entete_surf.clear_widgets()
		self.entete_surf.add_surf(Periode_set(self,size_hint = (.25,1),
			exc_fonc = self._trie_tab))
		self.entete_surf.add_text('Magasin source :',size_hint = (.09,h),
			text_color = self.sc.text_col1)
		self.entete_surf.add_surf(liste_set(self,
			self.magasin_src,
			self.sc.DB.Get_magasin_list(),
			size_hint = (.11,h),
			mother_fonc = self.set_magasin_src))

		self.entete_surf.add_text('Magasin destination :',size_hint = (.09,h),
			text_color = self.sc.text_col1)
		self.entete_surf.add_surf(liste_set(self,
			self.magasin_des,
			self.sc.DB.Get_magasin_list(),
			size_hint = (.11,h),
			mother_fonc = self.set_magasin_des))

		Get_border_input_surf(self.entete_surf,
			"Trier par motif de transfert",size_hint = (.3,1),
			border_col = self.sc.green,bg_color = self.sc.aff_col1,
			on_text = self.set_motif_trans,
			default_text = self.motif_trans)

	def trie_tab(self):
		lis = list(self.tranf_list_by_date)
		liste = [i for i in map(self.trie,lis) if i]
		entete = ["date","nombres d'articles","Quantités",
		"valeur monétaire","Magasin source",'Magasin destination',
		"motif"]
		wid_l = [.15,.1,.2,.15,.15,.15,.15]
		self.history_tab.Creat_Table(wid_l,entete,liste,
			mult = .15,ent_size = (1,.06))

	def trie(self,dic):
		mag = dic.get('magasin source')
		mag_name_src = self.sc.DB.Get_this_magasin(mag
			).get('nom').lower()
		mag = dic.get('magasin destination')
		mag_name_des = self.sc.DB.Get_this_magasin(mag
			).get('nom').lower()
		dic['Magasin source'] = mag_name_src
		dic['Magasin destination'] = mag_name_des
		dic["nombres d'articles"] = len(dic.get('articles'))
		dic['Quantités'] = self.sc.get_info_str(dic.get("quantités"))
		if self.magasin_src:
			if not self.magasin_src.lower() == mag_name_src:
				return None
		if self.magasin_des:
			if not self.magasin_des.lower() == mag_name_des:
				return None
		if self.motif_trans:
			if self.motif_trans.lower() not in dic.get('motif'):
				return None
		return dic


	def get_transf_list_by_date(self):
		date_liste = self.sc.get_date_list(self.day1,
			self.day2)
		_all_dict = [list(self.sc.DB.Get_all_trans_of(date
			).values()) for date in date_liste]
		all_list = list()
		for lis in _all_dict:
			all_list.extend(lis)
		self.tranf_list_by_date = all_list

	def _trie_tab(self):
		self.get_transf_list_by_date()
		self.trie_tab()


# Gestion des actions buttons
	def show_transfert_det(self,wid):
		info = wid.info
		transf_dic = self.sc.DB.get_this_transfert(info)
		article_dic = transf_dic.get('articles')
		entete = ["Désignation","Destockage","Stock restant","Montant"]
		wid_l = [.3,.3,.2,.2,]
		Tab = Table(self,mult = .15)
		Tab.Creat_Table(wid_l,entete,list(article_dic.values()),
			ent_size = (1,.09))
		self.add_modal_surf(Tab,size_hint = (.6,.6),
			show_close = False)

	def set_magasin_src(self,info):
		self.magasin_src = info
		self.trie_tab()

	def set_magasin_des(self,info):
		self.magasin_des = info
		self.trie_tab()

	def set_motif_trans(self,wid,val):
		self.motif_trans = val
		self.trie_tab()


