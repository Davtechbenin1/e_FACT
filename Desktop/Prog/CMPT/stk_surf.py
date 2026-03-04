#Coding:utf-8
"""
	Défintion d'objet Général à utiliser uniquement
	pour le module de gestion du stock

	La gestion du stock doit prendre en compte les
	deux partie de gestion en même temps séparer par un underscore
"""
from lib.davbuild import *
from General_surf import *
class New_article(stack):
	@Cache_error
	def initialisation(self):
		self.padding = dp(10)
		self.spacing = dp(10)
		self.image_link = 'media/logo.png'
		self.etape = 1
		self.infos_set()
		self.size_pos()

	def infos_set(self):
	# Gestion de la partie de désignation
		self.design = str()
		self.condit_name = str()
		self.condit_dict = dict()
		self.stockage_pr = str()
		self.famille = str()
		self.famille_list = self.sc.DB.Get_famille_dict().keys()
		self.taux = float()
		self.prix_vente = dict()
		self.alertqte = 1
		self.art_name = str()

		self.art_imag = str()

		self.file_link = "media/logo.png"

	def size_pos(self):
		self.clear_widgets()
		self.designation_surf = designation(self,
			bg_color = self.sc.aff_col1,size_hint = (.5,1))
		self.last_surf = stack(self,bg_color = self.sc.aff_col1,
			size_hint = (.5,1))

		self.add_surf(self.designation_surf)
		self.add_surf(self.last_surf)

	@Cache_error
	def Foreign_surf(self):
		self.designation_surf.add_all()
		self.add_last_surf()
		
	def add_last_surf(self):
		h = .06
		self.last_surf.clear_widgets()
		self.last_surf.add_text("L'image graphique de l'article",
			size_hint = (1,h),halign = 'center',
			text_color = self.sc.orange,font_size = '15sp',
			italic = True)
		f = float_l(self,size_hint = (1,.5))
		f.add_image(self.file_link)
		f.add_button("",on_press = self.get_file_from,
			bg_color = None)
		self.th_image_srf = f.th_image_srf
		self.last_surf.add_surf(f)
		self.last_surf.add_button_custom("Terminer",self.next_page,
			bg_color = self.sc.orange,text_color = self.sc.aff_col1,
			size_hint = (.3,h),padd = (.35,h))

	def get_type_l(self):
		liste = list()
		for dic in self.sc.DB.get_article_types().values():
			if self.type_name.lower() in dic.get('nom').lower():
				liste.append(dic.get('nom'))
		return liste

	def up_list(self,all_list = True):
		liste = self.get_type_l()
		if all_list:
			self.list_surf.info = str()
		self.list_surf.list_info = self.list_surf.normal_list(liste)
		self.list_surf.add_all()

# Gestion des actions des bouttons
	def set_type_name(self,wid,val):
		self.type_name = val
		self.up_list()

	def set_th_type(self,info):
		self.type_name = info
		self.up_list(False)

	def set_maga(self,info):
		self.maga_name = info

	def set_cate(self,info):
		self.cate_name = info

	def add_type_name(self,wid):
		if self.type_name not in self.type_dic.keys():
			self.add_all()
			typ_d = self.sc.DB.type_article_format()
			typ_d['nom'] = self.type_name
			self.sc.DB.update_type_article(typ_d)
		else:
			self.sc.add_refused_error("Ce type d'article existe déjà")

	def next_page(self,wid):
		art_dic = dict()
		art_dic['nom'] = self.art_name
		art_dic['Désignation'] = self.art_name
		art_dic['désignation'] = self.art_name
		art_dic["famille"] = self.famille
		art_dic['conditionnement'] = self.condit_dict
		art_dic['stockage'] = self.stockage_pr
		art_dic['prix de vente'] = self.prix_vente
		art_dic["seuil d'approvisionnement"] = self.alertqte
		
		self.__save_art__(dict(art_dic))
		self.infos_set()
		self.designation_surf.initialisation()
		self.add_all()

	def __save_art__(self,art_dic):
		self.sc.DB.Save_new_art(art_dic)

class designation(stack):
	def initialisation(self):
		self.padding = dp(10)
		self.spacing = dp(10)
		self.design = self.mother.design
		self.condit_name = self.mother.condit_name
		self.condit_dict = self.mother.condit_dict
		self.stockage_pr = self.mother.stockage_pr
		self.famille = self.mother.famille
		self.famille_list = self.mother.famille_list
		self.taux = self.mother.taux
		self.prix_vente = self.mother.prix_vente

		self.new_familly = str()
		self.srf_dict = dict()

		self.cond_list = list()
		self.alertqte = self.mother.alertqte

	def Foreign_surf(self):
		self.clear_widgets()
		h = .05
		self.add_text("Les informations générales de l'article",
			size_hint = (1,h),text_color = self.sc.text_col1,
			halign = 'center',bold = True,
			italic = True,underline = True,
			font_size = "16sp")
		self.add_padd((.15,h))
		self.add_text('Désignation',size_hint = (.2,h))

		Get_border_input_surf(self,"Désignation",
			size_hint = (.5,h),
			border_col = self.sc.green, bg_color = self.sc.aff_col3,
			on_text = self.set_name,default_text = self.mother.art_name)

		self.add_padd((.15,h))
		self.add_padd((.15,h))
		self.add_text("conditionnement",size_hint = (.2,h))
		Get_border_input_surf(self,'name',
			default_text = self.condit_name,
			bg_color = self.sc.aff_col3,
			on_text = self.set_condit_name,
			size_hint = (.3,h),
			border_col = self.sc.green)
		self.add_button("Ajouter",text_color = self.sc.orange,
			bg_color = None,halign = "left",size_hint = (.35,h),
			on_press = self.add_condit_name,bold = True)
		
		self.add_padd((.35,h))
		self.list_surf = liste_deroulante(self,str(),
			self.get_cont_list(),size_hint = (.6,.045),
			mult = 5,mother_fonc = self.set_th_condit)
		self.add_surf(self.list_surf)

		self.parametrage_surf = stack(self,size_hint = (1,.5),
			spacing = dp(10))
		self.add_surf(self.parametrage_surf)

	def add_parametrage(self):
		self.parametrage_surf.clear_widgets()
		h = .1
		self.parametrage_surf.add_text('Paramètrage',
			size_hint = (1,h),font_size = "16sp",
			italic = True,bold = True,
			)
		self.parametrage_surf.add_text('conditionnement de stockage',
			size_hint = (.3,h),
			text_color = self.sc.text_col1)
		self.parametrage_surf.add_surf(liste_set(self,
			self.stockage_pr,self.cond_list,
			mother_fonc = self.set_stockage_pr,size_hint =(.7,h)))
		if self.stockage_pr:
			self.condit_dict[self.stockage_pr] = (1,None)
			conds = list(self.cond_list)
			try:
				conds.remove(self.stockage_pr)
			except:
				return
			self.parametrage_surf.add_text("1",text_color = self.sc.orange,
				size_hint = (.05,h),bg_color = self.sc.aff_col3,radius = dp(5),
				padding_left = dp(5))
			self.parametrage_surf.add_text(self.stockage_pr,size_hint = (.1,h),
				text_color = self.sc.text_col1,padding_left = dp(5))
			self.parametrage_surf.add_text("==",size_hint = (.05,h),
				text_color = self.sc.green,halign = "center")
			ind = 0
			for cond_txt in conds:
				ind += 1
				if ind == 1:
					inf = self.stockage_pr
				else:
					inf = conds[ind-2]
				cnd = cond_txt
				tup = self.condit_dict.get(cnd,(12,inf))
				self.condit_dict[cnd] = tup
				self.parametrage_surf.add_input(tup[1],
					default_text = f"{tup[0]}",
					text_color = self.sc.orange,on_text = self.set_th_param,
					size_hint = (.1,h),bg_color = self.sc.aff_col3)
				self.srf_dict[tup[1]] = cnd
				self.parametrage_surf.add_text(cnd,text_color = self.sc.green,
					size_hint = (.1,h))
				self.parametrage_surf.add_text("==",size_hint = (.05,h),
					text_color = self.sc.green,)

			self.parametrage_surf.add_padd((1,.001))
			self.parametrage_surf.add_text_input("M'avertir si le stock est inférieur ou égale à",
				(.3,h),(.1,h),self.sc.text_col1,
				text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,on_text = self.set_alert,
				default_text = str(self.alertqte))
			self.parametrage_surf.add_text(self.stockage_pr+'(s)',
				size_hint = (.1,h))

			self.parametrage_surf.add_padd((1,.001))

			for cond_txt in self.cond_list:
				self.prix_vente.setdefault(cond_txt,int())
			self.parametrage_surf.add_text('Prix de vente',
				size_hint = (1,h),bold = True,italic = True)
			for cond_txt,prix in self.prix_vente.items():
				self.parametrage_surf.add_text(cond_txt,
					size_hint = (.1,h))
				Get_border_input_surf(self.parametrage_surf,
					cond_txt,size_hint = (.2,h),
					placeholder = f"Prix du {cond_txt}",
					border_col = self.sc.green,
					bg_color = self.sc.aff_col1,
					on_text = self.set_prix_vente,
					default_text = self.format_val(prix))
			self.parametrage_surf.add_padd((1,.001))	

			self.parametrage_surf.add_text("Famille d'article",
				size_hint = (.2,h),)
			self.list_srf = liste_set(self,self.famille,
				self.famille_list,mother_fonc = self.set_famille,
				size_hint = (.2,h))
			self.parametrage_surf.add_surf(self.list_srf)

			Get_border_input_surf(self.parametrage_surf,
				'nouvelle famille',default_text = self.new_familly,
				size_hint = (.35,h),bg_color = self.sc.aff_col1,
				border_col = self.sc.green,on_text = self.set_new_familly,
				placeholder = 'Nouvelle Famille')
			self.parametrage_surf.add_button('Ajouter et définir',
				bg_color = None,halign = 'left',
				size_hint = (.25,h),on_press = self.save_new_family,
				text_color = self.sc.orange,
				bold = True)


	def get_cont_list(self):
		liste = list()
		all_cond = self.sc.DB.get_conditionnement()
		for dic in all_cond.values():
			if self.condit_name.lower() in dic.get('nom').lower():
				liste.append(dic.get('nom'))
		return liste


	def up_list(self,all_list = True):
		liste = self.get_cont_list()
		if all_list:
			self.list_surf.info = str()
		self.list_surf.list_info = self.list_surf.normal_list(liste)
		self.list_surf.add_all()

# gestion des actions des bouttons
	def set_prix_vente(self,wid,val):
		wid.text = self.regul_input(wid.text)
		self.prix_vente[wid.info] = float(wid.text)

	def set_new_familly(self,wid,val):
		self.new_familly = val

	def save_new_family(self,wid):
		self.famille = self.new_familly
		#self.excecute(self._save_new_family_)
		self._save_new_family_()

	def _save_new_family_(self):
		dic = {self.new_familly:{"nom":self.new_familly}}
		self.sc.DB.save_famille(**dic)

	def set_name(self,wid,val):
		self.mother.art_name = val

	def set_param_info(self,info):
		ind,info = info.split(".")
		self.cond_list[int(ind)] = info

	def set_famille(self,info):
		self.famille = info

	def set_taux(self,wid,val):
		wid.text = self.regul_input(wid.text)
		self.taux = float(wid.text)
		self.mother.taux = self.taux

	def set_alert(self,wid,val):
		wid.text = self.regul_input(wid.text)
		self.alertqte = int(wid.text)
		self.mother.alertqte = self.alertqte

	def set_th_param(self,wid,val):
		wid.text = self.regul_input(wid.text)
		self.condit_dict[self.srf_dict[wid.info]] = ((float(wid.text),wid.info))
		self.mother.condit_dict = self.condit_dict

	def set_stockage_pr(self,info):
		self.stockage_pr = info
		self.mother.stockage_pr = self.stockage_pr
		self.add_parametrage()

	def set_th_condit(self,info):
		#self.condit_name = info
		if info not in self.cond_list:
			self.cond_list.append(info)
		else:
			self.cond_list.remove(info)
			if info in self.condit_dict:
				self.condit_dict.pop(info)
		self.mother.cond_list = self.cond_list
		self.up_list()
		self.add_parametrage()

	def set_condit_name(self,wid,val):
		self.condit_name = val
		self.up_list()

	def add_condit_name(self,wid):
		names = [dic.get('nom') for dic in self.sc.DB.get_conditionnement().values()]
		if self.condit_name not in names:
			dic = {
				self.condit_name:{"nom":self.condit_name}
			}
			self.sc.DB.save_conditionnement(**dic)
		else:
			self.sc.add_refused_error("Cet type de conditionnement existe déjà")
		self.up_list()

class Show_th_article(New_article):
	def initialisation(self):
		self.padding = dp(10)
		self.spacing = dp(10)
		self.th_article = self.mother.th_article
		self.image_link = self.th_article.get('img')
		self.etape = 1
		self.infos_set()
		self.size_pos()

	def infos_set(self):
	# Gestion de la partie de désignation
		self.design = str()
		self.condit_name = str()
		self.condit_dict = self.th_article.get('conditionnement')
		self.stockage_pr = self.th_article.get('stockage')
		self.famille = self.th_article.get('famille')
		self.famille_list = self.sc.DB.Get_famille_dict().keys()
		self.taux = float()
		self.prix_vente = self.th_article.get('prix de vente')
		self.alertqte = self.th_article.get("seuil d'approvisionnement")
		self.art_name = self.th_article.get('Désignation')

		self.art_imag = self.th_article.get('img')

		self.file_link = self.th_article.get('img')

# Gestion des actions des buttons
	def next_page(self,wid):
		art_dic = dict(self.th_article)
		art_dic['nom'] = self.art_name
		art_dic['Désignation'] = self.art_name
		art_dic['désignation'] = self.art_name
		art_dic["famille"] = self.famille
		art_dic['conditionnement'] = self.condit_dict
		art_dic['stockage'] = self.stockage_pr
		art_dic['prix de vente'] = self.prix_vente
		art_dic["seuil d'approvisionnement"] = self.alertqte

		self.sc.DB.Save_new_art(dict(art_dic))

		#self.mother.close_modal()

class art_list(box):
	def initialisation(self):
		self.padding = dp(10)
		self.spacing = dp(5)
		self.Search_text = str()
		self.size_pos()

		self.magasin = self.sc.magasin
		#self.fournisseur = #self.sc.DB.Get_fournisseur_list()[0]
		self.famille = str()
		self.s_famille = str()

	def size_pos(self):
		self.entete_surf = box(self,size_hint = (1,.045),
			spacing = dp(10),orientation = 'horizontal',
			bg_color = self.sc.aff_col1)
		self.corps_surf = Table(self,size_hint = (1,.95),
			bg_color = self.sc.aff_col3,radius = dp(10),
			exec_fonc  = self.on_show_art,
			exec_key = 'N°',padding = dp(10))
		self.add_surf(self.entete_surf)
		self.add_surf(self.corps_surf)

	def th_apply_col(self,data,ent):
		val = str(data.get(ent))
		if ent == "Stock actuel":
			val = val.replace('[b]','')
			val = val.replace('[/b]','')
			val = val.replace('[i]','')
			val = val.replace('[/i]','')
			if val:
				inf = val.split(' ')[1]
			else:
				inf = 0
			if int(inf) < 0:
				return self.sc.red
			else:
				return self.sc.green
	
	@Cache_error
	def Foreign_surf(self):
		self.add_entete()
		self.add_corp_surf()

	def Get_this_art_list(self):
		self.arts_dict = self.sc.DB.Get_article_list_dict()
		art_l = [dic for dic in map(self.trie,self.arts_dict.values())
		 if dic]
		return art_l

	def trie(self,art_d):
		th_d = dict(art_d)
		if self.Search_text.lower() not in th_d.get('désignation').lower():
			return None
		if self.famille:
			if not th_d.get('famille').lower() == self.famille.lower():
				return None
		th_d['N°'] = art_d.get('N°')
		th_d['Famille'] = art_d.get('famille')
		th_d['Stock actuel'] = self.get_art_stock(art_d)
		th_d['Prix de vente'] = self.get_art_prix(art_d)
		th_d['Vente total'] = self.get_art_sort_info(art_d,'vente')
		th_d['Achat total'] = self.get_art_sort_info(art_d,'arrivage')
		return th_d

	@Cache_error
	def add_entete(self):
		h = 1
		self.entete_surf.clear_widgets()
		self.entete_surf.add_text('Magasins :',size_hint = (.07,h),
			text_color = self.sc.text_col1)
		self.entete_surf.add_surf(liste_set(self,self.magasin,
			[self.sc.magasin],orientation = 'H',
			size_hint = (.12,h),mult = 2,
			mother_fonc = self.set_magasin))
		
		self.entete_surf.add_text('Famille:',size_hint = (.07,h),
			text_color = self.sc.text_col1)
		self.entete_surf.add_surf(liste_set(self,self.famille,
			self.sc.DB.get_famille().keys(),mult = 2,
			size_hint = (.12,h),mother_fonc = self.set_famille))
		b = box(self,radius = dp(10),
			bg_color = self.sc.aff_col3,
			orientation = 'horizontal',
			padding = dp(5),size_hint = (.3,1))
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
	def add_corp_surf(self):
		art_l = self.Get_this_art_list()
		entete = ["Désignation","Stock actuel",
			"Prix de vente","Vente total",
			'Achat total']
		wid_l = [.2,.2,.2,.2,.2]
		self.corps_surf.Creat_Table(wid_l,entete,art_l,
			ent_size = (1,.07),trie_entete = ("Désignation",),
			mult = .15,apply_col_fonc = self.th_apply_col)

	def get_art_stock(self,art_dic):
		mag_ident = self.sc.magasin #self.sc.DB.Get_this_magasin(self.magasin).get('N°')
		stks = art_dic.get('stocks').get(
			mag_ident,
			dict())
		cond = art_dic.get('conditionnement')
		stk_str = str()
		for key in cond:
			val = stks.get(key,0)
			stk_str += f" [b]{self.format_val(val)}[/b] [i]{key}[/i]"
		return stk_str

	def get_art_sort_info(self,art_dic,info_part):
		stks = art_dic.get(info_part,dict())
		cond = art_dic.get('conditionnement')
		stk_str = str()
		for key in cond:
			val = stks.get(key,0)
			stk_str += f" [b]{self.format_val(val)}[/b] [i]{key}[/i]"
		return stk_str

	def get_art_prix(self,art_dic):
		prix = art_dic.get('prix de vente')
		prix_str = str()
		for key,p_val in prix.items():
			prix_str += f" [i]{key}[/i] [b]{self.format_val(p_val)}[/b]"
		return prix_str

	def get_art_stock_(self,art_dic):
		mag_ident = self.sc.magasin#self.sc.DB.Get_this_magasin(self.magasin).get('N°')
		stks = art_dic.get('stocks').get(
			mag_ident,
			dict())
		cond = art_dic.get('conditionnement')
		stk_str = str()
		for key in cond:
			val = stks.get(key,0)
			stk_str += f" {self.format_val(val)} {key}"
		return stk_str

	def get_art_prix_(self,art_dic):
		prix = art_dic.get('prix de vente')
		prix_str = str()
		for key,p_val in prix.items():
			prix_str += f" {key} {self.format_val(p_val)}"
		return prix_str

	def Get_this_art_list_(self):
		self.arts_dict = self.sc.DB.Get_article_list_dict()
		art_l = [dic for dic in map(self.trie_,self.arts_dict.values()) if dic]
		return art_l

	def trie_(self,art_d):
		th_d = dict(art_d)
		th_d['N°'] = art_d.get('N°')
		th_d['Famille'] = art_d.get('famille')
		th_d['Stock actuel'] = self.get_art_stock_(art_d)
		th_d['Prix de vente'] = self.get_art_prix_(art_d)
		return th_d

# Défintion des méthodes d'actions des buttons et input*
	@Cache_error
	def Impression(self,wid):
		obj = self.sc.imp_part_dic('Résumé')(self)
		liste = self.Get_this_art_list_()
		entete = ["Désignation","Stock actuel","Prix de vente",
			"Vente total",'Achat total']
		wid_l = [.3,.25,.25,.1,.1]
		info = str()
		if self.magasin:
			info += f'Magasin : {self.magasin}<br/>'
		if self.famille:
			info += f'Famille : {self.famille}<br/>'
		if self.s_famille:
			info += f'Sous famille : {self.s_famille}<br/>'
		titre = f"Listes des articles"
		obj.Create_fact(wid_l,entete,liste,titre,info)

	def set_magasin(self,info):
		self.magasin = info
		self.add_corp_surf()

	def set_fourniseur(self,info):
		self.fournisseur = info
		self.add_corp_surf()

	def set_famille(self,info):
		self.famille = info
		self.add_all()

	def add_new_art(self,wid):
		self.new_art_set = True
		self.add_art_liste = False
		self.add_parti1_surf()

	def setting_search_txt(self,wid,val):
		self.Search_text = val
		self.add_corp_surf()

	@Cache_error
	def on_show_art(self,wid):
		self.th_article = self.sc.DB.Get_this_article(wid.info)
		srf = Show_th_article(self)
		srf.add_all()
		self.add_modal_surf(srf,size_hint = (.8,.85),
			titre = f"Modification de l'article {self.th_article.get('nom')}",)

class cmpt_art(stack):
	...

class Appro_surf(stack):
	def initialisation(self):
		self.spacing = dp(10)
		self.padding = dp(10)
		self.size_pos()
		self.init_infos()
		self.set_taxes = False
		self.valide_here = True

	def init_infos(self):
		self.magasin = self.sc.magasin
		self.fournisseur = self.sc.DB.Get_fournisseur_list()[0]
		self.article_dic = dict()
		self.article_name = str()
		self.curent_art_name = str()
		self.curent_art_ident = str()

		self.montant_total = float()
		self.taxes = float()

		self.curent_art_param = dict()

		self.magasin_list = [self.sc.magasin]
		self.fournisseur_list = self.sc.DB.Get_fournisseur_list()

	def size_pos(self):
		self.clear_widgets()
		self.entete_surf = stack(self,size_hint = (1,.05))
		self.article_srf = stack(self,size_hint = (.4,.3))
		self.paramet_srf = stack(self,size_hint = (.5,.3),
			padding = dp(10),spacing = dp(10),radius = dp(10),
			bg_color = self.sc.aff_col1)
		self.button_srf = stack(self,size_hint = (.1,.3))
		self.article_tab = Table(self,size_hint = (1,.63),
			bg_color = self.sc.aff_col3,exec_fonc = self.modify_art,
			exec_key = "Désignation")
		self.add_surf(self.entete_surf)
		self.add_surf(self.article_srf)
		Get_border_surf(self,self.paramet_srf,
			self.sc.green)
		self.add_surf(self.button_srf)
		self.add_surf(self.article_tab)

	def Foreign_surf(self):
		self.add_entete_surf()
		self.add_article_srf()
		self.add_paramet_srf()
		self.add_article_tab()

	def add_article_tab(self):
		entete = ["Désignation","Quantité","Prix d'achat",'Montant']
		wid_l = [.3,.3,.3,.1]
		liste = self.get_th_article_list()
		self.article_tab.Creat_Table(wid_l,entete,list(liste),
			mult = .1)
		if self.montant_srf:
			self.montant_srf.text = self.format_val(self.montant_total)

	def get_th_article_list(self):
		self.montant_total = float()
		for dic in self.article_dic.values():
			self.montant_total += dic.get("Montant")
		return self.article_dic.values()

	def add_button_srf(self):
		self.button_srf.clear_widgets()
		th_h = dp(20)
		f_s = "10sp"
		if self.article_dic or self.curent_art_param:
			if self.curent_art_param:
				but = self.button_srf.add_icon_but(
					icon = 'chevron-right',
					size_hint = (None,None),
					size = (dp(55),dp(55)),
					font_size = "40sp",
					text_color = self.sc.green,
					on_press = self.add_art_param)
				th_but = self.button_srf.add_button('Suivant',
					text_color = self.sc.green,size_hint = (1,None),
					height = th_h,font_size = f_s,
					on_press = self.add_art_param,
					halign = "left")

			else:
				...
			self.button_srf.add_icon_but(icon = 'close',
				text_color = self.sc.red,
				size_hint = (None,None),
				size = (dp(55),dp(55)),
				font_size = "40sp",
				on_press = self.clear_all,)
			self.button_srf.add_button('Effacer la liste',
				text_color = self.sc.red,size_hint = (1,None),
				bg_color = None,height = th_h,
				font_size = f_s,on_press = self.clear_all,
				halign = "left")
			if self.valide_here:
				self.button_srf.add_icon_but(
					icon = 'content-save',
					size_hint = (None,None),
					size = (dp(55),dp(55)),
					font_size = "40sp",
					text_color = self.sc.text_col1,
					on_press = self.save_art_param)
				self.button_srf.add_button('Sauvegarder',
					text_color = self.sc.text_col1,
					on_press = self.save_art_param,
					size_hint = (1,None),height = th_h,
					bg_color = None,font_size = f_s,
					halign = "left")

	def add_paramet_srf(self):
		four_id = self.sc.DB.Get_this_fourn_ident(self.fournisseur)
		self.paramet_srf.clear_widgets()
		self.curent_art_param = self.set_curent_art_param()
		self.add_button_srf()
		h = dp(40)
		if self.curent_art_name:
			acht_dic = self.curent_art_param.get('achats')
			prix_ven = self.curent_art_param.get("prix d'achat").get(four_id,dict())
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
					placeholder = "Prix d'achat")

	def set_curent_art_param(self):
		if self.curent_art_name:
			self.curent_art_name = self.curent_art_name.strip()
			self.fourn_id = self.sc.DB.Get_this_fourn_ident(self.fournisseur)
			curent_art = self.sc.DB.Get_this_article(self.curent_art_name)

			if not curent_art:
				return

			ident = curent_art.get('N°')
			curent_art_param = self.article_dic.get(ident,dict())
			if curent_art_param:
				return curent_art_param

			art_conds = curent_art.get('conditionnement')
			th_fourn_art = {}

			
			mag_id = 'Général' #self.sc.DB.Get_this_magasin(self.magasin).get("N°")
			
			th_fourn_art = {
				'N°' : curent_art.get('N°'),
				'Désignation' : curent_art.get('Désignation'),
				"prix d'achat" : curent_art.get(
					"prix d'achat").get(self.fourn_id,{cond:float() 
					for cond in art_conds.keys()}),
				'qté total acheter' : {cond:float() for cond in art_conds.keys()},
				"historique d'achat" : {self.sc.get_today():{cond:float() for cond in art_conds.keys()}}
			}
			curent_art_param = {
				"Désignation":curent_art.get('Désignation'),
				"N°":curent_art.get('N°'),
				"img":curent_art.get('img'),
				"achats":{cond:float() for cond in art_conds.keys()},
				"prix d'achat":{
					self.fourn_id:th_fourn_art.get("prix d'achat")
				}
			}
			return curent_art_param
		return None
			
	def add_entete_surf(self):
		self.entete_surf.clear_widgets()
		self.entete_surf.add_text('Magasin',size_hint = (.07,1))
		self.entete_surf.add_surf(liste_set(self,self.magasin,
			self.magasin_list,
			mother_fonc = self.set_magasin,
			size_hint = (.15,1)))
		self.entete_surf.add_text('Fournisseur',size_hint = (.07,1))
		self.entete_surf.add_surf(liste_set(self,self.fournisseur,
			self.fournisseur_list,
			mother_fonc = self.set_fourniseur,
			size_hint = (.15,1)))
		b = Get_border_surf(self.entete_surf,box(self,size_hint = (.3,1),
			radius = dp(10),bg_color = self.sc.aff_col1),self.sc.green)
		self.montant_srf = b.add_text("",text_color = self.sc.orange,
			halign = 'center',font_size = "17sp")

	def add_article_srf(self):
		h = .18
		self.article_srf.clear_widgets()
		self.article_srf.add_text('Articles',size_hint =(.15,h))
		Get_border_input_surf(self.article_srf,"Article",
			size_hint = (.6,h),border_col = self.sc.green,
			bg_color = self.sc.aff_col1,
			default_text = self.article_name,
			placeholder = "Nom de l'article",
			on_text = self.set_article_name)
		self.article_srf.add_padd((.25,h))
		self.article_srf.add_padd((.15,h))
		self.article_list_srf = liste_deroulante(self.article_srf,
			self.curent_art_name,self.sc.DB.Get_article_list(),
			size_hint = (.6,h),mult = 7,
			mother_fonc = self.set_curent_art)
		self.article_srf.add_surf(self.article_list_srf)

	def sort_article(self):
		liste = self.sc.DB.Get_article_list()
		return [i for i in liste if self.article_name.lower() 
			in i.lower()]

	def get_montant(self,qte,prix):
		mont = float()
		for k,val in qte.items():
			if val:
				mont += (prix.get(k,int()) * float(val))
		return mont

# Gestion des actions des fournisseurs
	def add_art_param(self,wid):
		th_b = dict(self.curent_art_param)
		qte = th_b.get('achats')
		vent = th_b.get("prix d'achat").get(self.fourn_id,dict())
		qte_str = self.sc.get_info_str(qte)
		if qte_str:
			th_b["Quantité"] = qte_str
			th_b["Prix d'achat"] = self.sc.get_info_str(vent)
			th_b['Montant'] = self.get_montant(qte,vent)
			self.article_dic[th_b.get('N°')] = th_b
		elif th_b.get("N°") in self.article_dic:
			self.article_dic.pop(th_b.get('N°'))
		self.article_list_srf.info = str()
		self.article_list_srf.add_all()
		self.curent_art_name = dict()
		self.add_paramet_srf()
		self.add_article_tab()

	def clear_all(self,wid):
		self.article_dic = dict()
		self.curent_art_name = str()
		self.curent_art_param = dict()
		self.add_paramet_srf()
		self.add_article_tab()

	def save_art_param(self,wid):
		self.sc.set_confirmation_srf(self._save_art_param)

	def _save_art_param(self):
		four_id = self.sc.DB.Get_this_fourn_ident(self.fournisseur)
		arriv_dic = dict()
		arriv_dic['fournisseur'] = four_id
		arriv_dic['magasin'] = self.sc.magasin
		arriv_dic['articles'] = dict(self.article_dic)
		arriv_dic['montant HT'] = float(self.montant_total)
		arriv_dic['taxes'] = float(self.taxes)
		arriv_dic["montant TTC"] = self.montant_total + self.taxes
		self.sc.DB.Save_arrivage(arriv_dic)
		self.init_infos()
		self.add_all()

	def set_qte_achat(self,wid,val):
		cond = wid.info
		wid.text = self.regul_input(wid.text)
		self.curent_art_param["achats"][cond] = float(wid.text)

	def set_prix_achat(self,wid,val):
		cond = wid.info
		wid.text = self.regul_input(wid.text)
		self.curent_art_param["prix d'achat"][self.fourn_id][cond] = float(wid.text)
		
	def set_magasin(self,info):
		self.magasin = info

	def set_fourniseur(self,info):
		self.fournisseur = info

	def set_article_name(self,wid,val):
		self.article_name = val
		liste = self.sort_article()
		self.article_list_srf.list_info = self.article_list_srf.normal_list(liste)
		self.article_list_srf.add_all()

	def set_curent_art(self,info):
		self.curent_art_name = info
		self.add_paramet_srf()
		#self.add_article_tab()

	def modify_art(self,wid):
		self.curent_art_name = wid.info
		self.add_paramet_srf()
		
class Perte_hand(Appro_surf):
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
		Get_border_input_surf(self.entete_surf,"Motif de la perte",
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

			mag_id =  self.sc.magasin #self.sc.DB.Get_this_magasin(self.magasin).get("N°")

			curent_art_param = {
				"Désignation":curent_art.get('Désignation'),
				"N°":ident,
				"img":curent_art.get('img'),
				"pertes":{cond:float() for cond in art_conds.keys()},
				"prix de vente":curent_art.get("prix de vente")
			}
			return curent_art_param
		return None

	def add_article_tab(self):
		entete = ["Désignation","Quantité","Prix de vente",'Montant']
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
		h = dp(40)
		if self.curent_art_name:
			acht_dic = self.curent_art_param.get('pertes')
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
					readonly = True,placeholder = "Prix d'achat")

# Gestion des actions des boutons
	def _save_art_param(self):
		perte_dic = dict()
		perte_dic['magasin'] = self.sc.magasin
		perte_dic['motif'] = self.motif
		perte_dic['articles'] = dict(self.article_dic)
		perte_dic['montant HT'] = float(self.montant_total)
		perte_dic['taxes'] = float(self.taxes)
		perte_dic["montant TTC"] = self.montant_total + self.taxes
		self.sc.DB.Save_perte(perte_dic)
		self.init_infos()
		self.add_all()

	def add_art_param(self,wid):
		th_b = dict(self.curent_art_param)
		qte = th_b.get('pertes')
		vent = th_b.get("prix de vente")
		qte_str = self.sc.get_info_str(qte)
		if qte_str:
			th_b["Quantité"] = qte_str
			th_b["Prix de vente"] = self.sc.get_info_str(vent)
			th_b['Montant'] = self.get_montant(qte,vent)
			self.article_dic[th_b.get('N°')] = th_b
		elif th_b.get("N°") in self.article_dic:
			self.article_dic.pop(th_b.get('N°'))
		self.article_list_srf.info = str()
		self.article_list_srf.add_all()
		self.curent_art_name = dict()
		self.add_article_tab()

	def set_motif(self,wid,val):
		self.motif = val

	def set_qte_achat(self,wid,val):
		cond = wid.info
		wid.text = self.regul_input(wid.text)
		self.curent_art_param["pertes"][cond] = float(wid.text)
