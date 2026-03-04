#Coding:utf-8
"""
	Cet module permet la définition des surfaces à utiliser
	pour la gestion de vente au niveau du logiciel.
"""
from lib.davbuild import *
from General_surf import *
from .paie_surfs import *
from threading import Thread

class vente_rapide(box):
	def __init__(self,mother,art_dict,**kwargs):
		kwargs['spacing'] = dp(10)
		box.__init__(self,mother,**kwargs)
		"""
			art_dict représente le dictionnaire de l'article
			en cours de vente. Cela doit contenir les
			information de vente comme si on veut l'ajouter 
			au panier de vente
		"""
		self.art_dic = art_dict
		self.montant = self.art_dic.get('montant_TTC')
		self.size_pos()
		self.add_all()

	def Foreign_surf(self):
		self.add_client_surf()

	def set_cmd_ident(self):
		return self.sc.DB.Get_cmd_id()

	def size_pos(self):
		w,h = self.client_surf_size = 1,.5
		self.paie_surf_size = w,1-h

		self.client_surf = choose_client(self,(.1),
			spacing = dp(10),
			size_hint = self.client_surf_size)
		self.paie_surf = paiement_surf(self,.08,
			"Vente au comptant",self.montant,spacing = dp(10),
			size_hint = self.paie_surf_size)

		self.add_surf(self.client_surf)
		self.add_surf(self.paie_surf)

	def add_client_surf(self):
		pass
		#self.client_surf.add_all()

# Sauvegarde d'une vente
	def Save_vente(self,paie_id,mont):
		format_cmd = self.sc.DB.Get_cmd_format()
		selected_client = self.client_surf.clt_choose
		if not selected_client:
			self.sc.add_refused_error('Un client est nécessaire pour une vente')
		else:
			format_cmd['client'] = self.sc.DB.Get_this_clt_num(selected_client)
			format_cmd['montant TTC'] = self.art_dic['montant_TTC']
			format_cmd['paiements'] = [paie_id]
			format_cmd['montant payé'] = self.montant
			format_cmd['paiement actuel'] = paie_id
			format_cmd['articles'] = [self.art_dic]
			format_cmd['status de la commande'] = 'Livrée'
			format_cmd['status du paiement'] = 'Soldée'
			format_cmd['date de traitement'] = self.sc.get_now()
			format_cmd['date de livraison'] = self.sc.get_now()
			format_cmd['provenance'] = "Bureau"
			format_cmd['auteur'] = self.sc.get_curent_perso()
			format_cmd["provenance d'origine"] = "Bureau"
			format_cmd["auteur d'origine"] = self.sc.get_curent_perso()
			self.excecute(self.sc.DB.Save_cmd,format_cmd)
			#self.sc.DB.Save_cmd(format_cmd)

class choose_client(stack):
	def __init__(self,mother,info_h_hint,
		**kwargs):
		stack.__init__(self,mother,**kwargs)
		"""
			Cet objet permet l'enrégistrement, l'affichage,
			et la selection des clients
		"""
		self.clt_list_surf = all_clt_list(self,.1)
		self.add_surf(self.clt_list_surf)

		self.clt_choose = self.sc.DB.Get_clt_vente_rapide()
		if self.clt_choose:
			self.Show_clt(self.clt_choose)
		
	def Foreign_surf(self):
		self.clt_list_surf.add_all()

	def Show_clt(self,name):
		self.PRIORITY_LAY = show_clt_info(self,
			name,.08)
		self.add_all()

# Méthode des gestion des actions
	def choose_clt(self,wid):
		self.clt_choose = wid.info
		self.sc.DB.Save_clt_vente_rapide(self.clt_choose)
		self.PRIORITY_LAY = show_clt_info(self,
			self.clt_choose,.08)
		self.add_all()

	def BACK(self,wid):
		self.clt_choose = str()
		self.PRIORITY_LAY = None
		self.clear_widgets()
		self.add_surf(self.clt_list_surf)
		self.clt_list_surf.add_all()

	def Add_new_clt(self,wid):
		self.PRIORITY_LAY = Set_new_clt(self,(.09))
		self.add_all()

class all_clt_list(box):
	def __init__(self,mother,info_h_hint,**kwargs):
		kwargs['spacing'] = dp(10)
		box.__init__(self,mother,**kwargs)
		self.ifh = info_h_hint
		self.size_pos()

		self.curent_type = str()
		self.curent_cate = str()
		self.credit = str()
		self.clt_name = self.sc.DB.Get_clt_vente_rapide()

		self.type_liste = self.sc.get_type_list()
		self.cate_liste = self.sc.get_cat_list()
		self.add_all()
		
	def size_pos(self):
		w,h = self.entete_size = 1,self.ifh*3
		self.table_surf_size = w,1-h

		self.entete_surf = stack(self,
			size_hint = self.entete_size,
			spacing = dp(10),
			padding_bottom = dp(10))
		self.table_surf = Table(self,
			size_hint = self.table_surf_size,
			exec_fonc = self.mother.choose_clt,
			exec_key = "Nom",padding = dp(10),
			bg_color = self.sc.aff_col3,
			radius = dp(10))

		self.add_surf(self.entete_surf)
		self.add_surf(self.table_surf)

	def Foreign_surf(self):
		self.all_clt_liste = self.sc.DB.Get_clt_to_show()
		self.add_entete_surf()
		self.add_table_surf()

	def add_entete_surf(self):
		self.entete_surf.clear_widgets()
		self.entete_surf.add_text('Liste des clients',
			underline = True, halign = 'center', 
			text_color = self.sc.text_col1,
			size_hint = (1,.31))
		self.entete_surf.add_text('Type :',
			size_hint = (.1,.31),
			text_color = self.sc.text_col1)
		self.entete_surf.add_surf(liste_set(self.entete_surf,
			self.curent_type,self.type_liste,size_hint = (.2,.33),
			mult = 1.5,mother_fonc = self.set_type))
		self.entete_surf.add_text('Catégorie :',
			size_hint = (.18,.31),
			text_color = self.sc.text_col1)
		self.entete_surf.add_surf(liste_set(self.entete_surf,
			self.curent_cate,self.cate_liste,size_hint = (.25,.31),
			mult = 1,mother_fonc = self.set_cate))

		self.entete_surf.add_input('nom',size_hint = (.4,.31),
			text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
			on_text = self.set_clt_name,
			placeholder = 'Trier les informations par nom')

		self.entete_surf.add_text('vente à crédit ?',text_color = self.sc.text_col1,
			size_hint = (.18,.31))
		self.entete_surf.add_surf(liste_set(self.entete_surf,
			self.credit,['Oui','Non'],size_hint = (.1,.31),
			mult = 2,mother_fonc = self.set_credit))

		self.entete_surf.add_button("Ajouter",size_hint = (.2,.29),
			bg_color = self.sc.aff_col2,text_color = self.sc.text_col3,
			on_press = self.mother.Add_new_clt)

	def add_table_surf(self):
		entete = ['Nom',"Type","Catégorie","Solde"]
		wid_l = [.4,.2,.2,.2]
		ent_size = (1,self.ifh*1.2)
		donner_l = self.Trie_clt()
		self.table_surf.Creat_Table(wid_l,entete,
			donner_l,ent_size = ent_size)

	def Trie_clt(self):
		this_l = list()
		for clt_d in self.all_clt_liste:
			if self.clt_name.lower() in clt_d.get('Nom').lower():
				this_l.append(clt_d)
		this_l = self.Trie_sur_credit(this_l)
		this_l = self.trie_sur_cate(this_l)
		this_l = self.tris_sur_typ(this_l)
		this_l.sort(key = itemgetter("Nom"))
		return this_l

	def Trie_sur_credit(self,liste):
		this_l = list()
		if self.credit:
			if self.credit.lower() == "oui":
				self.credit = True
			else:
				self.credit = False
			for clt_d in liste:
				if clt_d.get('credit') == self.credit:
					this_l.append(clt_d)
			return this_l

		else:
			return liste

	def trie_sur_cate(self,liste):
		if self.curent_cate:
			this_l = list()
			for clt_d in liste:
				if clt_d.get('Catégorie') == self.curent_cate:
					this_l.append(clt_d)
			return this_l
		else:
			return liste

	def tris_sur_typ(self,liste):
		if self.curent_type:
			this_l = list()
			for clt_d in liste:
				if clt_d.get('Type') == self.curent_type:
					this_l.append(clt_d)
			return this_l
		else:
			return liste

# méthodes de gestion des actions
	def set_cate(self,info):
		if self.curent_cate:
			self.curent_cate = str()
		else:
			self.curent_cate = info
		self.add_table_surf()

	def set_type(self,info):
		if self.curent_type:
			self.curent_type = str()
		else:
			self.curent_type = info
		self.add_table_surf()

	def set_credit(self,info):
		if self.credit:
			self.credit = str()
		else:
			self.credit = info
		self.add_table_surf()

	def set_clt_name(self,wid,val):
		self.clt_name = val
		self.mother.clt_choose = val
		self.add_table_surf()

class show_clt_info(box):
	def __init__(self,mother,clt_name,info_h_hint,**kwargs):
		kwargs['orientation'] = "horizontal"
		box.__init__(self,mother,**kwargs)
		"""
			Affiche uniquement les informations du
			client
		"""
		self.clt_name = clt_name
		self.ifh = info_h_hint
		self.clt_dict = self.sc.DB.Get_this_clt(self.clt_name)
		self.size_pos()
		self.add_all()

	def size_pos(self):
		w,h = self.img_surf_size = .35,1
		self.det_surf_size = 1-w,h
		self.img_surf = float_l(self,
			size_hint = self.img_surf_size)
		self.details_surf = stack(self,
			size_hint = self.det_surf_size,
			spacing = dp(10))

		self.add_surf(self.img_surf)
		self.add_surf(self.details_surf)

	def Foreign_surf(self):
		self.add_image_part()
		self.add_infos_part()

	def add_image_part(self):
		self.img_surf.clear_widgets()
		self.img_surf.add_image(self.clt_dict.get('img'))

	def add_infos_part(self):
		self.details_surf.clear_widgets()
		b_ = stack(self,size_hint = (1,self.ifh*2),
			bg_color = self.sc.aff_col3,radius = dp(10))
		B = box(self,size_hint = (1,.5),
			orientation = 'horizontal')
		B.add_text(self.clt_dict.get('nom'),
			halign ='center',font_size = "20sp",
			text_color = self.sc.text_col1,
			radius = dp(10))
		B.add_button('',info = "clt_show_surf",
			on_press = self.mother.BACK,
			bg_color = self.sc.red,size_hint = (None,None),
			height = dp(20),width = dp(20),pos_hint = (0,.25))
		b_.add_surf(B)

		solde = self.clt_dict.get('solde')
		if not solde:
			solde = 0
		b_.add_text_input('Solde :    ',
			(.2,.5),(.7,.5),self.sc.text_col1,
			text_color = self.sc.text_col1,font_size = '20sp',
			bg_color = self.sc.aff_col3,readonly = True,
			default_text = self.format_val(solde),
			text_halign = 'right')
		self.details_surf.add_surf(b_)
		b = box(self,size_hint = (1,self.ifh*2),
			orientation = 'horizontal',spacing = dp(5))
		p_dic = {
			"Type":self.clt_dict.get('type'),
			"Catégorie":self.clt_dict.get('catégorie')
		}
		for k,v in p_dic.items():
			b_ = box(self,bg_color = self.sc.aff_col3,
				radius = dp(10),padding = [dp(5),0,
				dp(5),dp(5)])
			b_.add_text(k,halign = 'center',
				text_color = self.sc.text_col1)
			b_.add_text(v,halign = 'center',
				text_color = self.sc.text_col3,
				bg_color = self.sc.aff_col2,radius = dp(5))
			b.add_surf(b_)
		self.details_surf.add_surf(b)
		self.details_surf.add_text_input('Téléphone :',
			(.3,self.ifh),(.6,self.ifh),self.sc.text_col1,
			text_color = self.sc.text_col1,font_size = "17sp",
			bg_color = self.sc.aff_col3,readonly = True,
			default_text = self.clt_dict.get("tel"))

		self.details_surf.add_text_input('N° Whatsapp :',
			(.3,self.ifh),(.6,self.ifh),self.sc.text_col1,
			text_color = self.sc.text_col1,font_size = "17sp",
			bg_color = self.sc.aff_col3,readonly = True,
			default_text = self.clt_dict.get("whatsapp"))
		adress = (self.clt_dict.get('pays')+', '+self.clt_dict.get('ville')+', '+
			self.clt_dict.get('quartier')+', '+self.clt_dict.get("maison"))
		self.details_surf.add_text('Adresse complète',
			text_color = self.sc.text_col1,size_hint = (1,self.ifh))
		self.details_surf.add_text(adress,size_hint = (1,self.ifh*1.5),
			bg_color = self.sc.aff_col3,text_color = self.sc.text_col1,
			radius = dp(10))

class Set_new_clt(box):
	def __init__(self,mother,info_h_hint,**kwargs):
		kwargs['orientation'] = 'horizontal'
		kwargs['spacing'] = dp(10)
		box.__init__(self,mother,**kwargs)
		self.ifh = info_h_hint
		self.size_pos()
		self.model_clt_new = self.sc.DB.Get_client_format('particulier')
		#print(self.model_clt_new)
		self.nom,self.prenom = str(),str()
		self.curent_cate = self.model_clt_new.get('catégorie')
		self.curent_type = self.model_clt_new.get('type')
		self.model_clt_new["date d'enregistrement"] = self.day1
		self.this_img = self.model_clt_new.get('img')
		self.genre_dict = self.sc.DB.Get_clt_types()
		self.association_membre = str()
		self.liste_association = self.sc.DB.Get_Association_list()

		self.solde_act = float()
		self.tel = str()
		self.email = str()

		self.add_all()

	def size_pos(self):
		w,h = self.part1_size = .4,1
		self.part2_size = 1-w,h

		self.part1_surf = box(self,
			size_hint = self.part1_size,
			spacing = dp(10))
		self.part2_surf = stack(self,
			size_hint = self.part2_size,
			spacing = dp(10))

		self.add_surf(self.part1_surf)
		self.add_surf(self.part2_surf)

	def Foreign_surf(self):
		self.add_part1_surf()
		self.add_part2_surf()

	def add_part1_surf(self):
		self.part1_surf.clear_widgets()
		F = float_l(self,size_hint = (1,self.ifh*8))
		F.add_image(self.model_clt_new.get('img'))
		F.add_button('',bg_color = None,bg_opact=0,
			on_press = self.get_img_from)
		self.part1_surf.add_surf(F)
		dic = {
			'Nom :':self.nom,
			"Prénom :":self.prenom
		}
		for k,v in dic.items():
			B = box(self,size_hint = (1,self.ifh),
				orientation = 'horizontal')
			B.add_text_input(k,(.4,1),
				(.6,1),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = 
				self.sc.aff_col3,on_text = self.set_name,
				default_text = v,placeholder = k)
			self.part1_surf.add_surf(B)

	def add_part2_surf(self):
		self.part2_surf.clear_widgets()
		self.part2_surf.add_text('Types :',size_hint = 
			(.4,self.ifh),text_color = self.sc.text_col1)
		self.part2_surf.add_surf(liste_set(self.part2_surf,
			self.curent_type,self.sc.get_type_list(),
			size_hint = (.5,self.ifh),mult = 1,
			mother_fonc = self.set_type))
		self.part2_surf.add_button('',size_hint = (None,None),
			bg_color = self.sc.red,height = dp(20),
			width = dp(20),on_press = self.mother.BACK)

		self.genre_list = self.genre_dict.get(self.curent_type)
		self.curent_genre = self.genre_list[0]
		self.part2_surf.add_text('Genre :',size_hint = 
			(.4,self.ifh),text_color = self.sc.text_col1)
		self.part2_surf.add_surf(liste_set(self.part2_surf,
			self.curent_genre,self.genre_list,
			size_hint = (.6,self.ifh),mult = 1,
			mother_fonc = self.set_genre))

		self.part2_surf.add_text('Catégorie :',size_hint = 
			(.4,self.ifh),text_color = self.sc.text_col1)
		self.part2_surf.add_surf(liste_set(self.part2_surf,
			self.curent_cate,self.sc.get_cat_list(),
			size_hint = (.6,self.ifh),mult = 1,
			mother_fonc = self.set_cate))

		

		self.part2_surf.add_surf(Periode_set(self.part2_surf,
			input_color = self.sc.aff_col3,info = "Date d'ajout :",
			one_part = True,exc_fonc = self.set_date_add,
			info_w = .19,size_hint = (1,self.ifh)))
		dic = {
			"Téléphone :":self.tel,
			"Solde :":self.solde_act,
			"Email :":self.email,
		}
		for k,v in dic.items():
			self.part2_surf.add_text_input(k,(.4,self.ifh),
				(.6,self.ifh),self.sc.text_col1, 
				on_text = self.set_last_info,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,)

		self.last_part = box(self,size_hint = (1,self.ifh*2))
		self.part2_surf.add_surf(self.last_part)
		self.add_last()

	def add_last(self):
		self.last_part.clear_widgets()
		self.last_part.add_button('Ajouter',
			size_hint = (.6,1),pos_hint = (.2,0),
			text_color = self.sc.text_col3, 
			bg_color = self.sc.aff_col2,
			on_press = self.Add_client)
		txt = self.error_text
		txt_col = self.sc.red
		if self.succes_text:
			txt = self.succes_text
			txt_col = self.sc.green
		self.last_part.add_text(txt,text_color = txt_col,
			halign = 'center')

# méthode de gestion des actions
	def set_genre(self,info):
		if self.curent_genre:
			self.curent_genre = str()
		else:
			self.curent_genre = info

	def set_asso(self,info):
		if self.association_membre:
			self.association_membre = str()
		else:
			self.association_membre = info

	def Add_client(self,wid):
		nom = f"{self.nom} {self.prenom}"
		nom = nom.strip()
		if nom:
			self.model_clt_new["nom"] = nom.replace('.','')
			if self.curent_cate:
				self.model_clt_new["catégorie"] = self.curent_cate
			if self.curent_type:
				self.model_clt_new['type'] = self.curent_type
			if self.solde_act:
				self.model_clt_new['solde à la création'] = float(self.solde_act)
				self.model_clt_new['solde'] = float(self.solde_act)
			self.model_clt_new['tel'] = self.tel
			self.model_clt_new['email'] = self.email
			self.model_clt_new['img'] = self.this_img
			ret = self.sc.DB.Save_client(self.model_clt_new)
			if ret:
				self.mother.clt_choose = nom
				self.sc.DB.Save_clt_vente_rapide(nom)
				self.mother.Show_clt(nom)
				
				self.sc.add_refused_error("Nouveau client ajouter")
			else:
				self.sc.add_refused_error("Cet client existe déjà dans la base")
			
		else:
			self.error_text = 'Nom de client indispenable'
			self.sc.add_refused_error("Le nom du client est indispenable")
			self.add_last()

	def set_last_info(self,wid,val):
		if wid.info == "Téléphone :":
			self.tel = val
		elif "solde" in wid.info.lower():
			try:
				val = float(val)
			except:
				self.error_text = "format du solde non valide"
				self.add_last()
			else:
				self.solde_act = val
				self.add_last()
		elif "email" == wid.info.lower():
			self.email = val

	def set_type(self,info):
		if self.curent_type:
			self.curent_type = str()
		else:
			self.curent_type = info
			self.model_clt_new = self.sc.DB.Get_client_format(self.curent_type)
			self.add_part2_surf()

	def set_cate(self,info):
		if self.curent_cate:
			self.curent_cate = str()
		else:
			self.curent_cate = info

	def set_date_add(self):
		self.model_clt_new["date d'enregistrement"] = self.day1

	def get_img_from(self,wid):
		self.sc.file_chooser(self.modif_img)

	def modif_img(self,select):
		self.this_img = select
		self.model_clt_new['img'] = select
		self.add_part1_surf()

	def set_name(self,wid,val):
		if wid.info == "Nom :":
			self.nom = val
		elif wid.info == "Prénom :":
			self.prenom = val
		nom = f"{self.nom} {self.prenom}"
		nom = nom.strip()
