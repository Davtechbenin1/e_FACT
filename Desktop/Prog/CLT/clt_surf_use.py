#Coding:utf-8
from lib.davbuild import *
from General_surf import *
from .clt_surf1 import *
from .clt_infos import *

class TH_det_client(menu_surf_V_maquette):
	"""
	@Cache_error
	def initialisation(self):
		self.this_client = self.mother.this_client
		self.access_dic = self.mother.access_dic
		self.Get_menu_infos()
		self.curent_menu = str()
		self.size_pos()
	"""

	@Cache_error
	def Get_menu_infos(self):
		dic = {
			#"Identité":Identite,
			"Historique d'action":histo_act_client,
			"Information client":Info_client,
			#"Commandes":commandes,
			#"Paiements":paiements,
			
		}
		self.wid_dict = dict()
		for i,srf in dic.items():
			if self.sc.DB.Get_access_of(i):
				self.wid_dict[i] = srf
		self.icon_dict = {
			#"Identité": "account",              # Icône profil/utilisateur
			"Information client": "information", # Icône info
			"Commandes": "cart",                 # Icône panier/commande
			"Paiements": "credit-card",          # Icône paiement
			"Historique d'action": "history"     # Icône historique
		}


"""
	def size_pos(self):
		w,h = self.menu_size = 1,.04
		self.corps_size = w,1-h

		self.menu_surf = stack(self,size_hint = (self.menu_size),
			padding = [dp(5),dp(5),dp(5),0],spacing = dp(5),
			bg_color = self.sc.aff_col3)

		self.corps_surf = box(self,size_hint = self.corps_size)

		self.add_surf(self.menu_surf)
		self.add_text('',bg_color = self.sc.text_col1,
			size_hint = (1,None),height = dp(1))
		self.add_surf(self.corps_surf)

	@Cache_error
	def Foreign_surf(self):
		if self.this_client:
			self.add_menu_surf()
		else:
			self.clear_widgets()
			self.initialisation()

	def add_menu_surf(self):
		self.menu_surf.clear_widgets()
		self.corps_surf.clear_widgets()
		for k,surf in self.menu_dict.items():
			if not self.curent_menu:
				self.curent_menu = k
			bg_col = None
			txt_col = self.sc.text_col1
			if k == self.curent_menu:
				bg_col = self.sc.aff_col2
				txt_col = self.sc.aff_col2
				surf = surf(self,bg_color = self.sc.aff_col1)
				surf.add_all()
				self.corps_surf.add_surf(surf)

			self.menu_surf.add_button('',size_hint = (None,None),
				width = dp(25),height = dp(25),on_press = self.change_menu,
				info = k,bg_color = bg_col,radius = dp(15))
			self.menu_surf.add_button(k,size_hint = (None,None),
				width = dp(10)*len(k),info = k,height = dp(25),
				halign = 'left',on_press = self.change_menu,
				bg_color = None,text_color = txt_col)

# Gestion des actions
	def change_menu(self,wid):
		self.curent_menu = wid.info
		self.add_all()

	def ini_surf(self,wid):
		#self.mother.clear_widgets()
		#self.mother.add_surf(self.mother.liste_clt_surf)
		self.mother.close_modal()
"""

class details_client(box):
	@Cache_error
	def initialisation(self):
		self.this_client = self.mother.this_client
		self.access_dic = self.mother.access_dic
		self.Get_menu_infos()
		self.curent_menu = str()
		self.size_pos()

	def Get_menu_infos(self):
		dic = {
			"Identité":Identite,
			"Commandes":commandes,
			"Paiements":paiements,
			"statistique":box,
		}
		self.menu_dict = dict()
		if self.access_dic == "all":
			self.menu_dict = {
				"Identité":Identite,
				"Commandes":commandes,
				"Paiements":paiements,
				"statistique":box,
			}
		else:
			for i in dic:
				for i,srf in dic.items():
					if i in self.mother.access_dic:
						self.menu_dict[i] = srf

	def size_pos(self):
		w,h = self.menu_size = 1,.04
		self.corps_size = w,1-h

		self.menu_surf = stack(self,size_hint = (self.menu_size),
			padding = [dp(5),dp(5),dp(5),0],spacing = dp(5),
			bg_color = self.sc.aff_col3,radius = dp(10))

		self.corps_surf = box(self,size_hint = self.corps_size,
			padding = dp(10),radius = dp(10),
			bg_color = self.sc.aff_col1)

		self.add_surf(self.menu_surf)
		self.add_text('',bg_color = self.sc.text_col1,
			size_hint = (1,None),height = dp(1))
		self.add_surf(self.corps_surf)

	@Cache_error
	def Foreign_surf(self):
		if self.this_client:
			self.add_menu_surf()
		else:
			self.clear_widgets()
			self.initialisation()

	def add_menu_surf(self):
		self.menu_surf.clear_widgets()
		self.corps_surf.clear_widgets()
		for k,surf in self.menu_dict.items():
			if not self.curent_menu:
				self.curent_menu = k
			bg_col = None
			txt_col = self.sc.text_col1
			if k == self.curent_menu:
				bg_col = self.sc.aff_col2
				txt_col = self.sc.aff_col2
				surf = surf(self,bg_color = self.sc.aff_col1)
				surf.add_all()
				self.corps_surf.add_surf(surf)

			self.menu_surf.add_button('',size_hint = (None,None),
				width = dp(25),height = dp(25),on_press = self.change_menu,
				info = k,bg_color = bg_col,radius = dp(15))
			self.menu_surf.add_button(k,size_hint = (None,None),
				width = dp(10)*len(k),info = k,height = dp(25),
				halign = 'left',on_press = self.change_menu,
				bg_color = None,text_color = txt_col)

# Gestion des actions
	@Cache_error
	def change_menu(self,wid):
		self.curent_menu = wid.info
		self.add_all()

class Identite(stack):
	@Cache_error
	def initialisation(self):
		if self.mother.access_dic == "all":
			self.access_liste = "all"
		else:
			self.access_liste = self.mother.access_dic.get('Identité')
		
		self.this_client = self.mother.this_client
		self.size_pos()
		self.th_typ = self.this_client.get('type')
		self.th_cat = self.this_client.get('catégorie')
		self.th_asso = self.this_client.get('association appartenue')
		self.th_cred = self.this_client.get('vente à crédit')
		self.th_cont = self.this_client.get('type de contrat')
		self.th_remb = self.this_client.get('type de remboursement')
		self.th_char = self.this_client.get("chargé d'affaire")
		self.typ_list = ['particulier',"entreprise","association"]
		self.cat_list = ['standart',"grossiste"]
		self.cred_list = 'Oui',"Non"
		self.asso_all_dic = self.sc.DB.Get_associations()
		self.asso_list = [i for i in self.asso_all_dic.values()]
		self.ass_all_idents = {j:i for i,j in self.asso_all_dic.items()}

		self.ident_dict = dict()
		self.contact_dict = dict()
		self.this_note = str()

	def size_pos(self):
		self.part_size = 1,.5
		self.nom_part_surf = box(self,size_hint = (1,.45),
			bg_color = self.sc.aff_col1,padding = dp(10),
			spacing = dp(5),orientation = "horizontal")
		self.second_part_surf = box(self,size_hint = (1,.55),
			bg_color = self.sc.aff_col1,padding = dp(10),
			radius = [0,0,dp(10),dp(10)],spacing = dp(5),
			orientation = 'horizontal')
		self.add_surf(self.nom_part_surf)
		self.add_surf(self.second_part_surf)

	@Cache_error
	def Foreign_surf(self):
		self.add_nom_part_surf()
		self.add_second_part_surf()
		self.add_nom_surf()
		self.add_contact_surf()

		self.add_article_prefe()
		self.add_visite_surf()

	def add_nom_part_surf(self):
		h = .07
		self.nom_part_surf.clear_widgets()
		self.img_surf = float_l(self,size_hint = (.16,1))
		self.img_surf.add_image(self.this_client.get('img'))
		self.img_surf.add_button("",bg_color = None,on_press = self.get_img_from)
		self.nom_part_surf.add_surf(self.img_surf)

		self.nom_surf = stack(self,spacing = dp(5),padding = dp(5),
			size_hint = (.64,1))
		self.contact_surf = stack(self,spacing = dp(5),padding = dp(5),
			size_hint = (.2,1))
		self.nom_part_surf.add_surf(self.nom_surf)
		self.nom_part_surf.add_surf(self.contact_surf)

	def add_second_part_surf(self):
		self.second_part_surf.clear_widgets()

		self.article_prefe = stack(self,size_hint = (.4,1))
		self.visite_surf = stack(self,spacing = dp(5),
			size_hint = (.6,1))
		
		self.second_part_surf.add_surf(self.article_prefe)
		self.second_part_surf.add_surf(self.visite_surf)

	def add_nom_surf(self):
		h = .093
		self.nom_surf.clear_widgets()
		self.nom_surf.add_text(self.this_client.get('nom'),
			size_hint = (.65,h),text_color = self.sc.text_col1,
			font_size = "17sp",halign = 'center')
		self.nom_surf.add_text(f'Solde: {self.format_val(self.this_client.get("solde"))}',
			text_color = self.sc.aff_col2,font_size = '17sp',
			size_hint = (.35,h))
		dic1 = {
			"nom":self.this_client.get("nom"),
			"ville":self.this_client.get('ville'),
			"quartier":self.this_client.get('quartier'),
			"maison":self.this_client.get('maison'),
			"profession":self.this_client.get('profession'),
			"IFU":self.this_client.get('IFU'),
			"tel":self.this_client.get('tel'),
			"whatsapp":self.this_client.get('whatsapp'),
			"email":self.this_client.get('email'),
			"localité":self.this_client.get('localité',str()),
			"nom du client":self.this_client.get('nom du client',str()),
			"prénom du client":self.this_client.get('prénom du client',str()),
			"date de naissance":self.this_client.get('date de naissance',str()),
			"lieu de naissance":self.this_client.get('lieu de naissance',str()),
			"Personne à contacter":self.this_client.get('Personne à contacter',str()),
			"Téléphone personne à contacter":self.this_client.get('Téléphone personne à contacter',str()),
		}
		if self.th_typ == "entreprise":
			dic1['RCCM'] = self.this_client.get('RCCM',str())

		if self.this_client.get("solde"):
			dic1.pop("nom")

		for k,v in dic1.items():
			self.nom_surf.add_text_input(k,(.25,h),(.25,h),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				on_text = self.new_info,default_text = str(v),
				placeholder = k)
		
	def add_contact_surf(self):
		h = .122
		self.contact_surf.clear_widgets()
		self.contact_surf.add_text_input("date d'enregistrement :",
			(.45,h),(.5,h),self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,readonly = True,
			default_text = self.this_client.get("date d'enregistrement"))

		bg_col = self.sc.orange
		categorie = self.this_client.get('status')
		if "ordinaire" in categorie.lower():
			bg_col = self.sc.green
		else:
			bg_col = self.sc.red

		self.contact_surf.add_text_input('Catégorie actuelle',(.45,h),(.5,h),
			bg_col,text_color = self.sc.text_col3,bg_color = bg_col,
			default_text = categorie,readonly = True,)

		self.contact_surf.add_text_input("Numéro de dossier",(.45,h),(.5,h),
			bg_col,text_color = self.sc.text_col3,bg_color = bg_col,
			default_text = self.this_client.get('N°'),readonly = True,)

		dic = {
			"Type":(self.th_typ,self.typ_list,self.set_type),
			"Catégorie":(self.th_cat,self.cat_list,self.set_cat),
			"Association":(self.th_asso,self.asso_list,self.set_asso),
			"Chargé d'affaire":(self.th_char,self.sc.get_all_charger(),
				self.set_char)
		}
		for k,liste in dic.items():
			txt,liste,fonc = liste
			self.contact_surf.add_text(k,size_hint = (.45,h),
				text_color = self.sc.text_col1)
			self.contact_surf.add_surf(liste_set(self,txt,liste,
				mother_fonc = fonc, mult = 1, size_hint = (.55,h)))

		self.contact_surf.add_padd((.066,h))
		
	def add_article_prefe(self):
		self.article_prefe.clear_widgets()
		self.article_prefe.add_text('Articles préférés',size_hint = (1,.05),
			halign = 'center',text_color = self.sc.text_col1, 
			underline = True)

		self.articles_p = self.this_client.get('articles préférés')
		if not self.articles_p:
			self.articles_p = dict()
		liste = [{"nom":i,"qté":j,"famille":self.sc.DB.Get_famille_of(i)} 
			for i,j in self.articles_p.items()]
		if liste:
			liste.sort(key = itemgetter("qté"))
		if len(liste) > 10:
			liste = liste[:10]
		art_l = Table(self,size_hint = (1,.955),bg_color = self.sc.aff_col3,
			padding = dp(10),radius = dp(10))
		entete = "famille",'nom',"qté"
		wid_l = .4,.35,.25
		art_l.Creat_Table(wid_l,entete,liste)
		self.article_prefe.add_surf(art_l)

	def add_visite_surf(self):
		h = .06
		self.visite_surf.clear_widgets()
		self.visite_surf.add_text("Historique d'actions du client",
			text_color = self.sc.text_col1,halign = 'center',
			underline = True,size_hint = (1,h))
		self.visite_surf.add_surf(Periode_set(self,size_hint = (1,.07),
			exc_fonc = self.Trie_visite,info_w = .2))
		self.ths_v_tab = Table(self,size_hint = (1,.85),
			bg_color = self.sc.aff_col3,padding = dp(10),
			radius = dp(10))
		self.visite_surf.add_surf(self.ths_v_tab)
		self.Trie_visite()

	def Trie_visite(self):
		wid_l = .2,.2,.2,.2,.2
		entete = "date","solde de départ","achats","paiements",'solde final'
		liste = self.get_histo_list()
		self.ths_v_tab.Creat_Table(wid_l,entete,liste)

	def get_histo_list(self):
		date_liste = self.get_date_list(self.day1,self.day2)
		all_histo = self.this_client.get('historique du solde',dict())
		liste = list()
		if all_histo:
			for date in date_liste:
				dic = all_histo.get(date)
				if dic:
					dic['date'] = date
					liste.append(dic)
		return liste
				
# Gestion des actions des bouttons
	def set_note(self,wid,val):
		self.this_note = val

	def Supprimer(self,wid):
		self.sc.DB.Sup_clt_info(self.this_client)
		self.sc.add_refused_error("Client supprimer avec succès")
		self.mother.this_client = dict()
		self.mother.add_all()

	def set_remb(self,info):
		self.th_remb = info
		self.ident_dict['type de remboursement'] = self.th_remb

	def set_char(self,info):
		self.th_char = info
		self.ident_dict["chargé d'affaire"] = self.th_char

	def set_contrat(self,info):
		self.th_cont = info
		self.ident_dict['type de contrat'] = self.th_cont

	@Cache_error
	def upload_fic(self,selection):
		self.this_client['img'] = selection
		self.img_surf.clear_widgets()
		self.img_surf.add_image(self.this_client.get('img'))
		self.img_surf.add_button("",bg_color = None,on_press = self.get_img_from)

	def set_contact(self,wid,val):
		self.this_client[wid.info] = val

	def set_cred(self,info):
		self.th_cred = info
		self.ident_dict['vente à crédit'] = info

	def set_type(self,info):
		self.th_typ = info
		self.ident_dict['type'] = info

	def set_cat(self,info):
		self.th_cat = info
		self.ident_dict['catégorie'] = info

	@Cache_error
	def set_asso(self,info):
		if info:
			info = self.sc.DB.Get_asso_num(info)
		clt_name = self.this_client.get('N°')
		solde = float(self.this_client.get("solde"))	
		if self.th_asso:
			self._set_asso(info,clt_name,solde)
		else:
			self._set_asso_(info,clt_name,solde)
		self.th_asso = info
		self.ident_dict['association appartenue'] = info

	def _set_asso(self,info,clt_name,solde):
		try:
			asso_ident = self.ass_all_idents[self.th_asso]
		except KeyError:
			asso_ident = self.th_asso
		self.sc.DB.Sup_client_asso(asso_ident,clt_name,solde)
		self.this_client["association appartenue"] = info
		self.sc.DB.Update_client(self.this_client)

	def _set_asso_(self,info,clt_name,solde):
		self.sc.DB.Add_client_asso(info,clt_name,solde)
		self.this_client["association appartenue"] = info
		self.sc.DB.Update_client(self.this_client)

	def new_info(self,wid,val):
		self.ident_dict[wid.info] = val

	@Cache_error
	def valid_info(self,wid):
		self.this_client.update(self.ident_dict)
		ident = self.sc.DB.Update_client(self.this_client)
		if ident:
			self.sc.add_refused_error("Identité modifier !")
			self.ident_dict = dict()
		else:
			self.this_client = self.sc.DB.Get_this_clt(self.this_client.get('N°'))

class show_th_clt_info(details_client):
	def add_menu_surf(self):
		self.menu_surf.clear_widgets()
		self.corps_surf.clear_widgets()
		for k,surf in self.menu_dict.items():
			if not self.curent_menu:
				self.curent_menu = k
			bg_col = None
			txt_col = self.sc.text_col1
			if k == self.curent_menu:
				bg_col = self.sc.aff_col2
				txt_col = self.sc.aff_col2
				surf = surf(self,bg_color = self.sc.aff_col1)
				surf.add_all()
				self.corps_surf.add_surf(surf)

			self.menu_surf.add_button('',size_hint = (None,None),
				width = dp(25),height = dp(25),on_press = self.change_menu,
				info = k,bg_color = bg_col,radius = dp(15))
			self.menu_surf.add_button(k,size_hint = (None,None),
				width = dp(10)*len(k),info = k,height = dp(25),
				halign = 'left',on_press = self.change_menu,
				bg_color = None,text_color = txt_col)

		self.menu_surf.add_padd((.3,1))
		self.menu_surf.add_button('',size_hint = (None,None),
			width = dp(20),height = dp(20),bg_color = self.sc.red,
			on_press = self.Back)
		

	def Back(self,wid):
		self.mother.this_client = dict()
		self.mother.Reinit()

