#Coding:utf-8
"""
	Gestion des parties spécifiques de la gestion des fournisseurs
"""
from lib.davbuild import *
from General_surf import *

class Bien_et_services(box):
	@Cache_error
	def initialisation(self):
		self.orientation = "horizontal"
		self.this_fourn_id = self.mother.this_fourn_info.get('N°')
		self.this_famille = str()
		self.famille_list = self.sc.Get_famm_d()
		self.this_s_famille = str()
		self.this_art_list = self.sc.DB.Get_all_fourn_article_list(self.this_fourn_id)
		self.all_arti_list = self.sc.DB.Get_article_list()
		self.all_arti_dict = {i:self.sc.DB.Get_this_article(i) for i in self.all_arti_list}
		self.curent_art_set = str()
		self.name = str()
		self.size_pos()
		self.add_all()

	def size_pos(self):
		self.clear_widgets()
		w,h = self.show_article_size = .5,1
		self.develop_size = 1-w,h

		self.show_article_surf = stack(self,size_hint = self.show_article_size,
			spacing = dp(5))
		self.develop_surf = stack(self,size_hint = self.develop_size,
			spacing = dp(5),padding_left = dp(10))
		self.add_surf(self.show_article_surf)
		self.add_text("",size_hint = (None,1),width = dp(1),
			bg_color = self.sc.text_col1)
		self.add_surf(self.develop_surf)

	@Cache_error
	def Foreign_surf(self):
		self.add_show_article_surf()
		self.add_develop_surf()

	def add_show_article_surf(self):
		h = .045
		self.show_article_surf.clear_widgets()
		self.show_article_surf.add_text("Articles disponibles",
			text_color = self.sc.text_col1,underline = True,
			halign = "center",size_hint = (1,h))
		self.show_article_surf.add_text('Famille :',size_hint = (.13,h),
			text_color = self.sc.text_col1)
		self.show_article_surf.add_surf(liste_set(self,self.this_famille,
			self.famille_list,size_hint = (.3,h),mult = 1,mother_fonc = self.set_fam))
		if self.this_famille:
			self.show_article_surf.add_text('S. famille :',size_hint = (.13,h),
				text_color = self.sc.text_col1)
			liste = self.sc.DB.Get_s_famille_dict(self.this_famille)
			self.show_article_surf.add_surf(liste_set(self,self.this_s_famille,
				liste,size_hint = (.3,h),mult = 1,mother_fonc = self.set_s_fam))
		self.show_article_surf.add_padd((1,.00000000001))
		self.show_article_surf.add_padd((.1,h))
		self.show_article_surf.add_input('trie',size_hint = (.8,h),
			on_text = self.set_name,default_text = self.name,
			placeholder = 'Trier par nom',text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3)
		self.list_surf = scroll(self,size_hint = (1,.7),
			)
		self.show_article_surf.add_surf(self.list_surf)
		self.Up_tab()

	def Up_tab(self):
		self.list_surf.clear_widgets()
		h = dp(25)
		liste = self.Trie_art()
		if len(liste)>60:
			liste = liste[:60]
		H = len(liste)*(h+10)
		H += dp(10)
		stw = stack(self,size_hint = (1,None),height = H,
			spacing = dp(5))
		for txt in liste:
			txt_col = self.sc.text_col1
			bg_color = self.sc.aff_col3
			if txt in self.this_art_list:
				txt_col = self.sc.aff_col2
			if txt == self.curent_art_set:
				bg_color = self.sc.aff_col2
			b = box(self,size_hint = (1,None),height = h,
				orientation = 'horizontal',spacing = dp(5))
			b.add_button('',bg_color = bg_color,info = txt,
				size_hint = (None,None),on_press = self.select_art,
				width = dp(20),height = dp(20),pos_hint = (0,.2))
			b.add_button(txt,halign = 'left',text_color = txt_col,
				bg_color = None,on_press = self.select_art)
			stw.add_surf(b)
		self.list_surf.add_surf(stw)

	def Trie_art(self):
		lis = [i for i in self.all_arti_list if self.name.lower() in i.lower()]
		lis = [i for i in lis if self.this_famille.lower() in self.all_arti_dict.get(i).get('famille').lower()]
		lis = [i for i in lis if self.this_s_famille.lower() in self.all_arti_dict.get(i).get('sous famille').lower()]
		return lis

	def Trie(self,dic):
		pass

	def add_develop_surf(self):
		h = .045
		self.develop_surf.clear_widgets()
		if self.curent_art_set:
			self.this_art_dict = self.sc.DB.Get_this_four_art(
				self.this_fourn_id,self.curent_art_set)
			self.up_art_dict()
			self.develop_surf.add_text(self.curent_art_set.upper(),
				halign = 'center',underline = True,font_size = '18sp',
				size_hint = (1,h),text_color = self.sc.text_col1)
			if self.this_art_dict.get('nom') in self.this_art_list:
				buts = ['content-save-alert',"delete","close"]
				inset = True
			else:
				buts = ['content-save',"close"]
				inset = False

			dic = {
				"nom":self.this_art_dict.get('nom').replace('_',' '),
				"famille":self.this_art_dict.get('famille'),
				"sous famille":self.this_art_dict.get('sous famille'),
				"nbre par qté":self.this_art_dict.get('nbre_par_qté'),
			}
			for k,v in dic.items():
				self.develop_surf.add_text_input(k,(.2,h),(.3,h),
					self.sc.text_col1,text_color = self.sc.text_col1,
					bg_color = self.sc.aff_col3,default_text = v,
					readonly = True,)
			if inset:
				self.develop_surf.add_text("Quantité total demander",
					underline = True,text_color = self.sc.text_col1,
					halign = 'center',size_hint = (1,h))
				dic = self.this_art_dict.get("qté total demander")
				self.develop_surf.add_padd((.05,h))
				for k,v in dic.items():
					self.develop_surf.add_text_input(k,(.15,h),(.3,h),
						self.sc.text_col1,text_color = self.sc.text_col1,
						bg_color = self.sc.aff_col3,default_text = str(v),
						readonly = True)
			
				#self.develop_surf.add_icon_but(icon = "history",
				#	on_press = self.show_histo_dem,text_color = self.sc.orange,
				#	size_hint = (.1,h))

				self.develop_surf.add_text("Quantité total acheter",
					underline = True,text_color = self.sc.text_col1,
					halign = 'center',size_hint = (1,h))
				dic = self.this_art_dict.get("qté total acheter")
				self.develop_surf.add_padd((.05,h))
				for k,v in dic.items():
					self.develop_surf.add_text_input(k,(.15,h),(.3,h),
						self.sc.text_col1,text_color = self.sc.text_col1,
						bg_color = self.sc.aff_col3,default_text = str(v),
						readonly = True)
				#self.develop_surf.add_icon_but(icon = "history",
				#	on_press = self.show_histo_ach,text_color = self.sc.orange,
				#	size_hint = (.1,h))
			
			self.develop_surf.add_text("Prix d'achat",underline = True,
				text_color = self.sc.text_col1,halign = 'center',
				size_hint = (1,h))
			dic = self.this_art_dict.get("prix d'achat")
			self.develop_surf.add_padd((.05,h))
			for k,v in dic.items():
				self.develop_surf.add_text_input(k,(.15,h),(.3,h),
					self.sc.text_col1,text_color = self.sc.text_col1,
					bg_color = self.sc.aff_col3,default_text = str(v),
					on_text = self.set_prix_achat)
			self.develop_surf.add_padd((.1,h))
			
			
			col_list = self.sc.green,self.sc.red,self.sc.orange
			B = box(self,size_hint = (1,h),orientation = 'horizontal',
				padding_left = dp(20),padding_right = dp(20),
				spacing = dp(20))
			self.develop_surf.add_surf(B)
			for but,col in zip(buts,col_list):
				B.add_icon_but(icon = but,text_color = col,size_hint = (1,1),
					on_press = self.Exect_action,info = but.lower())

	@Cache_error
	def up_art_dict(self):
		origi_art = self.sc.DB.Get_this_article(self.curent_art_set)
		self.this_art_dict["nom"] = origi_art["nom"]
		self.this_art_dict["famille"] = origi_art["famille"]
		self.this_art_dict["sous famille"] = origi_art["sous famille"]
		self.this_art_dict["img"] = origi_art["img"]
		self.this_art_dict["nbre_par_qté"] = origi_art["nbre_par_qté"]

	@Cache_error
	def add_histo(self,part,imp_hist):
		h = .045
		histo_dict = self.this_art_dict.get(part)
		self.this_liste = list()
		for k,dic in histo_dict.items():
			d = dic
			d["date"] = k
			self.this_liste.append(d)
		
		self.develop_surf.clear_widgets()
		b = box(self,size_hint = (1,h),orientation = 'horizontal',
			spacing = dp(5))
		b.add_text(f'Historique des {part}',text_color = self.sc.text_col1,
			halign = 'center',underline = True)
		w = len('Impression') * dp(9)
		b.add_button('Impression',width = w,size_hint = (None,1),
			text_color = self.sc.text_col3, bg_color = self.sc.aff_col2,
			on_press = imp_hist)
		b.add_button('',size_hint = (None,None),height = dp(25),
			width = dp(25), bg_color = self.sc.red,on_press = self.back)
		self.develop_surf.add_surf(b)
		self.develop_surf.add_surf(Periode_set(self,size_hint = (.8,h),
			exc_fonc = self.Up_date))
		self.tab = Table(self,size_hint = (1,.9),
			bg_color = self.sc.aff_col3)
		self.develop_surf.add_surf(self.tab)
		self.Up_date()
		
	@Cache_error
	def Up_date(self):
		wid_l = .3,.35,.35
		entete = "date","qté","unité"
		liste = [j for j in self.this_liste if j.get('date') in 
			self.get_date_list(self.day1,self.day2)]
		self.tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.06))

# Gestion des actions des bouttons
	@Cache_error
	def Exect_action(self,wid):
		if wid.info == 'close':
			self.initialisation()
			self.add_all()
		elif wid.info == "content-save":
			art_dic = self.this_art_dict
			art_dic["historique des prix"][self.sc.get_today()] = art_dic.get("prix d'achat")
			self.excecute(self.sc.DB.Save_fourn_article,
				self.this_fourn_id,art_dic)
			#self.sc.DB.Save_fourn_article(self.this_fourn_id,art_dic)
			self.initialisation()
			self.add_all()
		elif wid.info == 'content-save-alert':
			art_dic = self.this_art_dict
			art_dic["historique des prix"][self.sc.get_today()] = art_dic.get("prix d'achat")
			self.excecute(self.sc.DB.Modif_fourn_article,self.this_fourn_id,art_dic)
			#self.sc.DB.Modif_fourn_article(self.this_fourn_id,art_dic)
			self.initialisation()
			self.add_all()
		elif wid.info == "delete":
			art_dic = self.this_art_dict
			self.excecute(self.sc.DB.Archiv_fourn_article,
				self.this_fourn_id,art_dic)
			#self.sc.DB.Archiv_fourn_article(self.this_fourn_id,art_dic)
			self.initialisation()
			self.add_all()

	def back(self,wid):
		self.add_develop_surf()

	def show_histo_ach(self,wid):
		part = "historique d'achat"
		self.add_histo(part,self.Impression)

	def show_histo_dem(self,wid):
		part = "historique de demande"
		self.add_histo(part,self.Impression)

	def show_histo_pri(self,wid):
		part = "historique des prix"
		self.add_histo(part,self.Impression)

	def Impression(self,wid):
		...

	def set_prix_achat(self,wid,val):
		part = wid.info
		wid.text = self.regul_input(wid.text)
		if not wid.text:
			wid.text = str(0)
		dic = self.this_art_dict.get("prix d'achat")
		dic[part] = float(wid.text)
		self.this_art_dict["priw d'achat"] = dic

	def select_art(self,wid):
		if wid.info == self.curent_art_set:
			self.curent_art_set = str()
		else:
			self.curent_art_set = wid.info
		self.Up_tab()
		self.add_develop_surf()

	def set_name(self,wid,val):
		self.name = val
		self.Up_tab()

	def set_fam(self,info):
		self.this_famille = info
		self.add_show_article_surf()

	def set_s_fam(self,info):
		self.this_s_famille = info
		self.Up_tab()

class Commandes(box):
	@Cache_error
	def initialisation(self):
		self.day1 = self.sc.get_today()
		self.day2 = self.sc.get_today()
		self.orientation = "horizontal"
		self.this_fourn_id = self.mother.this_fourn_info.get('N°')
		self.liste_status = ['Livrés',"Non livrés"]
		self.this_status = str()
		self.this_paie = str()
		self.liste_paie = ['Soldée','Non soldée',"Avancée"]
		self.this_cmd = str()

		self.this_famille = str()
		self.famille_list = self.sc.Get_famm_d()
		self.this_s_famille = str()
		self.this_art_list = list()

		#self.all_arti_list = #self.sc.DB.Get_all_fourn_article_list(self.this_fourn_id)
		self.all_arti_dict = {i.get("nom"):i for i in self.sc.DB.Get_article_list_dict().values()}
		#{i:self.sc.DB.Get_this_article(i) for i in self.all_arti_list}
		self.all_arti_list = [i for i in self.all_arti_dict.keys()]
		self.curent_art_set = str()
		self.name = str()
		self.taxes_enable = list()
		self.taxes_dict = dict()
		self.Fact = dict()
		self.size_pos()
		self.add_all()
		self.init_fact()

	def init_fact(self):
		self.new_art_set = self.sc.DB.Get_cmd_f_art()
		
	def size_pos(self):
		self.clear_widgets()
		w,h = self.show_article_size = .4,1
		self.develop_size = 1-w,h

		self.show_cmd_surf = stack(self,size_hint = self.show_article_size,
			spacing = dp(5))
		self.develop_surf = Details_cmd(self,size_hint = self.develop_size,
			spacing = dp(5),padding_left = dp(10))
		self.add_surf(self.show_cmd_surf)
		self.add_text("",size_hint = (None,1),width = dp(1),
			bg_color = self.sc.text_col1)
		self.add_surf(self.develop_surf)

	@Cache_error
	def Foreign_surf(self):
		self.aff_cmds_surf()
		self.add_develop_surf()

	def aff_cmds_surf(self):
		h = .045
		self.show_cmd_surf.clear_widgets()
		self.show_cmd_surf.add_text('Liste des Commandes',text_color = self.sc.text_col1,
			underline = True,halign = 'center',size_hint = (.9,h))
		if "écritures" in self.sc.DB.Get_access_of("Commandes"):
			self.show_cmd_surf.add_icon_but(icon = "plus",size_hint = (.1,h),
				text_color = self.sc.green,on_press = self.New_cmd)
		self.show_cmd_surf.add_surf(Periode_set(self,size_hint = (1,h),
			exc_fonc = self.Up_tab))
		self.show_cmd_surf.add_text('Satus commandes :',size_hint = (.35,h),
			text_color = self.sc.text_col1)
		self.show_cmd_surf.add_surf(liste_set(self,self.this_status,
			self.liste_status,size_hint = (.65,h),mult = 1,
			mother_fonc = self.Set_this_status))
		self.show_cmd_surf.add_text('Satus paiements :',size_hint = (.35,h),
			text_color = self.sc.text_col1)
		self.show_cmd_surf.add_surf(liste_set(self,self.this_paie,
			self.liste_paie,size_hint = (.65,h),mult = 1,
			mother_fonc = self.Set_this_paie))
		self.tab = Table(self,size_hint = (1,.78),
			bg_color = self.sc.aff_col3,exec_fonc = self.show_cmd,
			exec_key = 'N°')
		self.show_cmd_surf.add_surf(self.tab)
		self.Up_tab()

	@Cache_error
	def Up_tab(self):
		wid_l = .3,.35,.35
		entete = ["N°","montant restant","status"]
		liste = self.Trie_liste()
		self.tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.06),
			ligne_h = .09)

	def Trie_liste(self):
		date_liste = self.get_date_list(self.day1,self.day2)
		liste = self.sc.DB.Get_this_fourn_cmds(self.this_fourn_id,
			date_liste)
		return [i for i in map(self.Trie,liste) if i]

	def Trie(self,dic):
		mont_t = dic.get("montant TTC")
		mont_p = dic.get('montant payé')
		dic['montant restant'] = mont_t - mont_p
		if self.this_status:
			if dic.get('status').lower() != self.this_status.lower():
				return None
		if self.this_paie:
			if dic.get('status du paiement').lower() != self.this_paie.lower():
				return None
		return dic

	@Cache_error
	def add_new_cmd_set(self):
		h = .045
		self.show_cmd_surf.clear_widgets()
		self.show_cmd_surf.add_text('Nouvelle commande',
			text_color = self.sc.text_col1,halign = 'center',
			size_hint = (.9,h))
		self.show_cmd_surf.add_icon_but(icon = 'close',
			text_color = self.sc.red,size_hint = (.1,h),
			on_press = self.back)
		self.show_cmd_surf.add_text('Famille :',size_hint = (.15,h),
			text_color = self.sc.text_col1)
		self.show_cmd_surf.add_surf(liste_set(self,self.this_famille,
			self.famille_list,size_hint = (.3,h),mult = 1,mother_fonc = self.set_fam))
		if self.this_famille:
			self.show_cmd_surf.add_text('S. famille :',size_hint = (.18,h),
				text_color = self.sc.text_col1)
			liste = self.sc.DB.Get_s_famille_dict(self.this_famille)
			self.show_cmd_surf.add_surf(liste_set(self,self.this_s_famille,
				liste,size_hint = (.3,h),mult = 1,mother_fonc = self.set_s_fam))
		self.show_cmd_surf.add_padd((1,.00000000001))
		self.show_cmd_surf.add_padd((.1,h))
		self.show_cmd_surf.add_input('trie',size_hint = (.8,h),
			on_text = self.set_name,default_text = self.name,
			placeholder = 'Trier par nom',text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3)
		self.list_surf = scroll(self,size_hint = (1,.6),
			)
		self.show_cmd_surf.add_surf(self.list_surf)

		self.set_infos_surf = box(self,size_hint = (1,.1),
			orientation = 'horizontal',padding_right = dp(10),
			spacing  =dp(10))
		self.show_cmd_surf.add_surf(self.set_infos_surf)
		self.Up_this_tab()

	@Cache_error
	def add_infos_surf(self):
		self.set_infos_surf.clear_widgets()
		if self.curent_art_set:
			self.curent_art_dict = self.sc.DB.Get_this_four_art(
				self.this_fourn_id ,self.curent_art_set)
			d1 = {
				"qté":float(),
				"unité":float()
			}
			prix = self.curent_art_dict.get("prix d'achat")
			d2 = {
				"prix qté":prix.get('qté'),
				"prix unité":prix.get('unité')
			}
			self.new_art_set.update(d2)
			b1 = stack(self,size_hint = (.3,1),spacing = dp(5))
			for k,v in d1.items():
				v = self.new_art_set.get(k)
				b1.add_text_input(k,(.4,.5),(.6,.5),self.sc.text_col1,
					text_color = self.sc.text_col1,bg_color  =self.sc.aff_col3,
					on_text = self.set_art_qte,default_text = str(v))
			self.set_infos_surf.add_surf(b1)

			b2 = stack(self,size_hint = (.4,1),spacing = dp(5))
			for k,v in d2.items():
				b2.add_text_input(k,(.4,.5),(.6,.5),self.sc.text_col1,
					text_color = self.sc.text_col1,bg_color  =self.sc.aff_col3,
					on_text = self.set_art_qte,default_text = str(v))
			self.set_infos_surf.add_surf(b2)

			self.taxes_surf = stack(self,size_hint = (.4,1)
				,spacing = dp(5))
			self.set_infos_surf.add_surf(self.taxes_surf)
			self.Up_taxe()
			self.set_infos_surf.add_icon_but(icon = 'plus',size_hint = (None,None),
				size = (dp(35),dp(35)),on_press = self.Add_art,
				text_color = self.sc.green)

	def Up_taxe(self):
		self.taxes_surf.clear_widgets()
		taxes = {
			"TVA":18,
			"AIB":5
		}
		self.taxes_dict.update(taxes)
		for k,v in taxes.items():
			txt_col = self.sc.text_col1
			bg_color = self.sc.aff_col3
			read = True
			inp_col = self.sc.aff_col1
			if k in self.taxes_enable:
				txt_col = self.sc.aff_col2
				bg_color = self.sc.aff_col2
				read = False
				inp_col = self.sc.aff_col3

			b = box(self,orientation = "horizontal",size_hint = (1,.5))
			b.add_button('',size_hint = (None,None),width = dp(20),
				height = dp(20),on_press = self.enable_t, info = k,
				bg_color = bg_color,pos_hint = (0,.2))
			b.add_button(k,on_press = self.enable_t, info = k,
				bg_color = None,halign = 'left',text_color = self.sc.text_col1)
			b.add_input(k,on_text = self.set_taxes,readonly = read,
				text_color = txt_col,bg_color = inp_col,default_text = str(v),
				placeholder = k,)
			b.add_text('%',text_color = self.sc.text_col1)
			self.taxes_surf.add_surf(b)

	@Cache_error
	def Up_this_tab(self):
		self.list_surf.clear_widgets()
		h = dp(25)
		liste = self.Trie_art()
		if len(liste)>60:
			liste = liste[:60]
		H = len(liste)*(h+10)
		H += dp(10)
		stw = stack(self,size_hint = (1,None),height = H,
			spacing = dp(5))
		self.this_art_list = [j.get('nom') for j in self.Fact.get('articles')]
		for txt in liste:
			txt_col = self.sc.text_col1
			bg_color = self.sc.aff_col3
			if txt in self.this_art_list:
				txt_col = self.sc.aff_col2
			if txt == self.curent_art_set:
				bg_color = self.sc.aff_col2
			b = box(self,size_hint = (1,None),height = h,
				orientation = 'horizontal',spacing = dp(5))
			b.add_button('',bg_color = bg_color,info = txt,
				size_hint = (None,None),on_press = self.select_art,
				width = dp(20),height = dp(20),pos_hint = (0,.2))
			b.add_button(txt,halign = 'left',text_color = txt_col,
				bg_color = None,on_press = self.select_art)
			stw.add_surf(b)
		self.list_surf.add_surf(stw)

	def Trie_art(self):
		lis = [i for i in self.all_arti_list if self.name.lower() in i.lower()]
		lis = [i for i in lis if self.this_famille.lower() in self.all_arti_dict.get(i).get('famille').lower()]
		lis = [i for i in lis if self.this_s_famille.lower() in self.all_arti_dict.get(i).get('sous famille').lower()]
		return lis

	@Cache_error
	def add_develop_surf(self):
		self.develop_surf.fact_dic = self.Fact
		self.develop_surf.add_all()

# Gestion des actions des buttons
	def set_art_qte(self,wid,val):
		wid.text = self.regul_input(wid.text)
		self.new_art_set[wid.info] = wid.text

	def set_taxes(self,wid,val):
		wid.text = self.regul_input(wid.text)
		self.taxes_dict[wid.info] = wid.text

	def enable_t(self,wid):
		if wid.info in self.taxes_enable:
			self.taxes_enable.remove(wid.info)
		else:
			self.taxes_enable.append(wid.info)
		self.Up_taxe()

	@Cache_error
	def Add_art(self,wid):
		if self.new_art_set.get('qté') or self.new_art_set.get('unité'):
			qte = self.new_art_set.get('qté')
			unit = self.new_art_set.get('unité')
			p_qte = self.new_art_set.get('prix qté')
			p_uni = self.new_art_set.get('prix unité')
			self.new_art_set['Désignation'] = self.curent_art_set.replace("_",' ')
			self.new_art_set["nom"] = self.curent_art_set
			art_d = self.sc.DB.Get_this_article(self.curent_art_set)
			self.new_art_set['img'] = art_d.get('img')
			self.new_art_set['qté_uni'] = art_d.get('qté')
			self.new_art_set['uni_uni'] = art_d.get('unité')
			taxe_en = {i:self.taxes_dict.get(i) for i in self.taxes_enable}
			mont,taxe,mont_ttc = self.Get_mont()
			self.new_art_set['taxes'] = taxe
			self.new_art_set['montant_HT'] = mont
			self.new_art_set['montant_TTC'] = mont_ttc
			self.new_art_set['taxes_enable'] = taxe_en
			self.new_art_set['info'] = self.curent_art_set
			self.Fact["articles"].append(self.new_art_set)
		self.Up_fact()
		self.add_develop_surf()
		self.init_fact()
		self.curent_art_set = str()
		self.add_infos_surf()
		self.Up_this_tab()

	def Up_fact(self):
		mont = float()
		taxe = float()
		mont_ttc = float()
		for art_d in self.Fact.get('articles'):
			mont += art_d.get('montant_HT')
			taxe += art_d.get('taxes')
			mont_ttc += art_d.get('montant_TTC')
		self.Fact['montant HT'] = mont
		self.Fact['taxes'] = taxe
		self.Fact['montant TTC'] = mont_ttc

	def Get_mont(self):
		qte = self.new_art_set.get('qté')
		unit = self.new_art_set.get('unité')
		p_qte = self.new_art_set.get('prix qté')
		p_uni = self.new_art_set.get('prix unité')
		mont = float()
		if qte:
			mont += float(qte)*float(p_qte)
		if unit:
			mont += float(unit)*float(p_uni)
		taxes = 0
		for i in self.taxes_enable:
			val = float(self.taxes_dict.get(i,float()))
			taxes += round(mont*val/100,2)
		mont_ttc = mont + taxes
		return mont,taxes,mont_ttc

	def select_art(self,wid):
		if wid.info == self.curent_art_set:
			self.curent_art_set = str()
		else:
			self.curent_art_set = wid.info
			self.Get_art_from_l()
		self.Up_this_tab()
		self.add_infos_surf()

	def Get_art_from_l(self):
		for art_d in self.Fact.get("articles"):
			if art_d.get('nom') == self.curent_art_set:
				self.new_art_set = art_d
				self.Fact['articles'].remove(art_d)
				self.add_develop_surf()
				return
		self.init_fact()

	def set_name(self,wid,val):
		self.name = val
		self.Up_this_tab()

	def set_fam(self,info):
		self.this_famille = info
		self.add_new_cmd_set()

	def set_s_fam(self,info):
		self.this_s_famille = info
		self.Up_this_tab()

	@Cache_error
	def New_cmd(self,wid):
		self.Fact = {
			"articles":list(),
			"montant TTC":float(),
			'montant HT':float(),
			'taxes':float(),
		}
		self.develop_surf.new_cmd = True
		self.add_new_cmd_set()
		self.add_develop_surf()

	def back(self,wid):
		if self.Fact.get("articles"):
			self.sc.add_refused_error('Commande en coours')
		else:
			self.Fact = dict()
			self.add_all()

	def Set_this_status(self,info):
		self.this_status = info
		self.Up_tab()

	def Set_this_paie(self,info):
		self.this_paie = info
		self.Up_tab()

	@Cache_error
	def show_cmd(self,wid):
		self.this_cmd = wid.info
		self.Fact = self.sc.DB.Get_this_fourn_cmd(
			self.this_cmd)
		self.develop_surf.new_cmd = False
		self.develop_surf.fact_dic = self.Fact
		self.add_develop_surf()

class CMD_stock(Commandes):
	def size_pos(self):
		self.clear_widgets()
		w,h = self.show_article_size = .4,1
		self.develop_size = 1-w,h

		self.show_cmd_surf = stack(self,size_hint = self.show_article_size,
			spacing = dp(5))
		self.develop_surf = Details_cmd_stk(self.mother,size_hint = self.develop_size,
			spacing = dp(5),padding_left = dp(10))
		self.add_surf(self.show_cmd_surf)
		self.add_text("",size_hint = (None,1),width = dp(1),
			bg_color = self.sc.text_col1)
		self.add_surf(self.develop_surf)

	@Cache_error
	def initialisation(self):
		self.clear_widgets()
		self.day1 = self.sc.get_today()
		self.day2 = self.sc.get_today()
		self.orientation = "horizontal"

		self.this_fourn_id = self.mother.this_fourn_info.get('N°')
		if self.this_fourn_id:
			self.liste_status = ['Livrés',"Non livrés"]
			self.this_status = str()
			self.this_paie = str()
			self.liste_paie = ['Soldée','Non soldée',"Avancée"]
			self.this_cmd = str()

			self.this_famille = str()
			self.famille_list = self.sc.Get_famm_d()
			self.this_s_famille = str()
			self.this_art_list = list()
			self.all_arti_list = self.sc.DB.Get_all_fourn_article_list(self.this_fourn_id)
			self.all_arti_dict = {i:self.sc.DB.Get_this_article(i) for i in self.all_arti_list}
			self.curent_art_set = str()
			self.name = str()
			self.taxes_enable = list()
			self.taxes_dict = dict()
			self.Fact = dict()
			self.size_pos()
			self.add_all()
			self.init_fact()

	@Cache_error
	def aff_cmds_surf(self):
		h = .045
		self.show_cmd_surf.clear_widgets()
		b = box(self,size_hint = (1,h),orientation = "horizontal",
			spacing = dp(5),padding_right = dp(10))
		b.add_text('Liste des Commandes',text_color = self.sc.text_col1,
			underline = True,halign = 'center')
		self.show_cmd_surf.add_surf(b)
		self.show_cmd_surf.add_surf(Periode_set(self,size_hint = (1,h),
			exc_fonc = self.Up_tab,info_w = .2,))
		self.tab = Table(self,size_hint = (1,.85),
			bg_color = self.sc.aff_col3,exec_fonc = self.show_cmd,
			exec_key = 'N°')
		self.show_cmd_surf.add_surf(self.tab)
		self.Up_tab()

	@Cache_error
	def Up_tab(self):
		wid_l = .55,.45
		entete = ["N°","montant TTC"]
		liste = self.Trie_liste()
		self.tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.1))

	def Trie_liste(self):
		date_liste = self.get_date_list(self.day1,self.day2)
		liste = self.sc.DB.Get_this_fourn_cmds(self.this_fourn_id,
			date_liste)
		self.this_status = 'Non livrée'
		liste = [j for j in liste if 
		j.get('status').lower() == self.this_status.lower()]
		return liste

class Details_cmd(box):
	@Cache_error
	def initialisation(self):
		self.size_pos()
		self.fact_dic = dict()
		self.padding = [dp(10),dp(10),dp(10),0]
		self.new_cmd = True

	def size_pos(self):
		w,h = self.entete_size = 1,.045
		self.corps_size = w,1-h*2
		self.pied_size = w,h
		self.entete_surf = box(self,size_hint = self.entete_size,
			orientation = 'horizontal',spacing = dp(5),
			padding_top = dp(3))
		self.corps_surf = Table(self,size_hint = self.corps_size,
			bg_color = self.sc.aff_col3,padding = dp(5),
			radius = dp(5),exec_fonc = self.modif_art,
			exec_key = "nom")
		self.pied_surf = box(self,size_hint = self.pied_size,
			orientation = 'horizontal',spacing=dp(5),
			padding = dp(5))
		self.add_surf(self.entete_surf)
		self.add_surf(self.corps_surf)
		self.add_surf(self.pied_surf)

	@Cache_error
	def Foreign_surf(self):
		if self.fact_dic:
			self.add_entete_surf()
			self.add_corps_surf()
			self.add_pied_surf()
		else:
			self.clear_widgets()
			self.size_pos()

	@Cache_error
	def add_entete_surf(self):
		h = 1
		self.entete_surf.clear_widgets()
		dic = {
			"montant HT":self.fact_dic.get('montant HT'),
			"taxes":self.fact_dic.get('taxes'),
			"montant TTC":self.fact_dic.get('montant TTC'),
		}
		for k,v in dic.items():
			self.entete_surf.add_text_input(k,(.15,h),(.15,h),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				readonly = True,default_text = self.format_val(v))

	@Cache_error
	def add_corps_surf(self):
		entete = ["Désignation","Quantité","Prix d'achat",
			'Montant']
		wid_l = [.2,.2,.3,.2]
		liste = self.Get_l()
		self.corps_surf.Creat_Table(wid_l,entete,liste,ent_size = (1,.06),
			ligne_h = .08)

	@Cache_error
	def add_pied_surf(self):
		self.pied_surf.clear_widgets()
		liste = self.Get_l()
		qtr = self.Get_qts_str(liste)
		self.pied_surf.add_text(qtr,text_color = self.sc.text_col1,
			halign = 'center',size_hint = (.8,1))
		if self.new_cmd:
			self.pied_surf.add_icon_but(icon = "content-save",size_hint = (.1,1),
				text_color = self.sc.green,on_press = self.valider_cmd)
		else:
			self.pied_surf.add_icon_but(icon = "printer",size_hint = (.1,1),
				text_color = self.sc.black,on_press = self.Imprimer_cmd)
			if self.fact_dic.get('status') != "Livrée":
				if "écritures" in self.sc.DB.Get_access_of("Commandes"):
					self.pied_surf.add_icon_but(icon = "pencil",size_hint = (.1,1),
						text_color = self.sc.orange,on_press = self.modifier_cmd)

					self.pied_surf.add_icon_but(icon = "delete",size_hint = (.1,1),
						text_color = self.sc.red,on_press = self.supprimer_cmd)

	def Get_l(self):
		return list(self.fact_dic.get('articles',dict()).values())

# Gestion des actions des buttons
	def modif_art(self,wid):
		if self.new_cmd:
			self.mother.select_art(wid)

	def Imprimer_cmd(self,wid):
		...

	@Cache_error
	def valider_cmd(self,wid):
		if self.fact_dic.get('articles'):
			cmd_dic = self.sc.DB.Get_cmd_fournisseur()
			cmd_dic.update(self.fact_dic)
			cmd_dic['fournisseur'] = self.mother.this_fourn_id
			self.excecute(self.sc.DB.Save_fourn_cmd,cmd_dic)
			#self.sc.DB.Save_fourn_cmd(cmd_dic)
			self.sc.add_refused_error('Commande enrégistrer')
			self.mother.Fact = dict()
			self.mother.add_all()
		else:
			self.mother.Fact = dict()
			self.mother.add_all()

	@Cache_error
	def modifier_cmd(self,wid):
		ident = self.fact_dic["N°"]
		self.excecute(self.sc.DB.Del_fourn_cmd,self.fact_dic)
		#self.sc.DB.Del_fourn_cmd(self.fact_dic)
		self.new_cmd = True
		self.mother.Fact = self.fact_dic
		self.mother.add_new_cmd_set()
		self.mother.add_develop_surf()
		
	@Cache_error
	def supprimer_cmd(self,wid):
		dep = {i:j for i,j in self.fact_dic.items()}
		self.excecute(self.sc.DB.Del_fourn_cmd,dep)
		self.fact_dic = dict()
		self.mother.Fact = dict()
		self.mother.aff_cmds_surf()
		self.mother.add_develop_surf()

class Details_cmd_stk(Details_cmd):
	@Cache_error
	def add_pied_surf(self):
		self.pied_surf.clear_widgets()
		liste = self.Get_l()
		qtr = self.Get_qts_str(liste)
		self.pied_surf.add_text(qtr,text_color = self.sc.text_col1,
			halign = 'center')
	
		self.pied_surf.add_icon_but(icon = 'check-bold',size_hint = (.2,1),
			text_color = self.sc.green,on_press = self.valider_cmd)

# Gestion des actions des méthodes
	@Cache_error
	def valider_cmd(self,wid):
		self.mother.bon_commande = self.fact_dic
		self.mother.remove_widget(self.mother.art_set_set)
		self.mother.add_surf(self.mother.det_surf)
		self.mother.add_det_surf()


