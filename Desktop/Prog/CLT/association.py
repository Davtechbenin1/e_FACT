#Coding:utf-8
"""
	Gestion des associations
"""
from lib.davbuild import *
from General_surf import *
from .clt_surf_use import *

class association(box):
	@Cache_error
	def initialisation(self):
		self.orientation = 'horizontal'
		self.padding = [dp(2),dp(2),dp(2),0]
		self.th_cate = str()
		self.form_t = 'Trier par nom'
		self.t_liste = 'Trier par nom', 'Trier par numéro'
		self.cat_list = self.sc.DB.Get_all_type_asso()
		self.autre_cont = dict()
		self.documents = list()
		self.curent_doc = str()
		self.ass_ident = str()
		self.new_infos = {
			"nom":str(),
			"dirigeant":str(),
			"contact dirigeant":str(),
			"siège":str(),
			"identification":str(),
		}
		self.size_pos()
		self.add_all()

	def size_pos(self):
		w,h = self.liste_ass_size = .33,1
		self.aff_ass_size = 1-w,h

		self.liste_ass_surf = stack(self,size_hint = self.liste_ass_size,
			padding = dp(10),radius = dp(10),spacing = dp(5),
			bg_color = self.sc.aff_col1)

		self.aff_ass_surf = show_ass_info(self,size_hint = self.aff_ass_size,
			radius = dp(10),bg_color = self.sc.aff_col1)

		self.add_surf(self.liste_ass_surf)
		self.add_text('',size_hint = (None,1),width = dp(1),
			bg_color = self.sc.text_col1)
		self.add_surf(self.aff_ass_surf)

	@Cache_error
	def Foreign_surf(self):
		self.add_liste_surf()
		self.add_develop()

	@Cache_error
	def add_liste_surf(self):
		self.liste_ass_surf.clear_widgets()
		h = .045
		self.liste_ass_surf.add_text('liste des affiliations',text_color = self.sc.text_col1,
			halign = 'center',underline = True,size_hint = (.8,h))
		if "écritures" in self.sc.DB.Get_access_of("Affiliation"):
			self.liste_ass_surf.add_icon_but(icon = 'plus',
				text_color = self.sc.green,on_press = self.new_ass,
				size_hint = (.1,h))
		self.liste_ass_surf.add_icon_but(icon = 'printer',
			text_color = self.sc.black,on_press = self.Impression,
			size_hint = (.1,h))
		self.liste_ass_surf.add_text('Trie par catégorie',text_color = self.sc.text_col1,
			size_hint =(.3,h))
		self.liste_ass_surf.add_surf(liste_set(self,"Général",self.cat_list,
			size_hint = (.7,h),mult = 3,mother_fonc = self.set_cate))
		self.info_b = box(self,size_hint = (1,h),orientation = 'horizontal')
		self.up_info_b()
		self.liste_ass_surf.add_surf(self.info_b)

		self.tab = Table(self,size_hint = (1,.845),bg_color = self.sc.aff_col3,
			exec_key = "nom",exec_fonc = self.show_ass)
		self.liste_ass_surf.add_surf(self.tab)
		self.up_tab()

	@Cache_error
	def up_tab(self):
		entete = 'nom',"montant dû","nbres clients"
		wid_l = [.4,.3,.3]
		liste = self.Trie_asso()
		self.tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.07))

	def Trie_asso(self):
		dic = self.sc.DB.Get_associations()
		liste = list()
		for ident,nom in dic.items():
			asso_dic = self.sc.DB.Get_this_association(ident)
			if type(asso_dic) == dict:
				clts = asso_dic.get('clients membres')
				asso_dic['nbres clients'] = len(clts)
				liste.append(asso_dic)
		liste = [i for i in map(self.Trie,liste) if i]
		return liste

	def Trie(self,dic):
		if dic:
			if self.th_cate:
				if dic.get("catégorie").lower() != self.th_cate.lower():
					return None
			if self.form_t:
				if self.form_t == 'Trier par nom':
					if self.ass_ident.lower() not in dic.get('nom').lower():
						return None
				elif self.form_t == 'Trier par numéro':
					if self.ass_ident.lower() not in dic.get('N°').lower():
						return None
			return dic

	def up_info_b(self):
		self.info_b.clear_widgets()
		self.info_b.add_input('nom',text_color = self.sc.text_col1,
			on_text = self.set_ass_info,bg_color = self.sc.aff_col3,
			size_hint = (.7,1),placeholder = self.form_t)
		self.info_b.add_surf(liste_set(self,self.form_t,self.t_liste,size_hint = (.3,1),
			mult = 1,mother_fonc = self.set_form_t))

	@Cache_error
	def add_new_ass(self):
		self.liste_ass_surf.clear_widgets()
		h = .045
		b = box(self,size_hint = (1,h),orientation = 'horizontal')
		b.add_text("Nouvelle affiliation",text_color = self.sc.text_col1,
			halign = "center",underline = True)
		b.add_button('',size_hint = (None,None),width = dp(20),
			height = dp(20),bg_color = self.sc.red,on_press = self.close_new)
		self.liste_ass_surf.add_surf(b)
		self.liste_ass_surf.add_text('Catégorie',size_hint = (.3,h),
			text_color = self.sc.text_col1,)
		self.liste_ass_surf.add_surf(liste_set(self,self.th_cate,self.cat_list,
			"V",size_hint = (.7,h),mult = 3,mother_fonc = self.set_cate))

		for k,v in self.new_infos.items():
			self.liste_ass_surf.add_text_input(k,(.3,h),(.6,h),
				self.sc.text_col1, text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,default_text = str(v),
				on_text = self.set_new_infos)

		d_tab = dynamique_tab(self,size_hint = (1,h*5),
			bg_color = self.sc.aff_col3)
		entete = 'Nom','Téléphone ou email'
		wid_l = .5,.5
		d_tab.Creat_Table(wid_l,entete,self.set_autre_cont)
		self.liste_ass_surf.add_text('Autres contactes',size_hint = (1,h),
			text_color = self.sc.text_col1,halign = 'center')
		self.liste_ass_surf.add_surf(d_tab)

		self.liste_ass_surf.add_text_input('Ajouter un documents',
			(.3,h),(.4,h),self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,default_text = "Les documents ici",
			readonly = True)
		self.liste_ass_surf.add_button('Parcourir',bg_color = self.sc.orange,
			text_color = self.sc.text_col3,on_press = self.get_img_from,
			size_hint = (.3,h))

		self.liste_of_doc = box(self,size_hint = (1,h*1.3),
			orientation = "horizontal",spacing = dp(5))
		self.liste_ass_surf.add_surf(self.liste_of_doc)
		self.up_liste_of_doc()

		self.liste_ass_surf.add_button_custom("Sauvegarder",size_hint = (.4,h),
			bg_color = self.sc.aff_col2,text_color = self.sc.text_col3,
			fonc = self.save_assos,padd = (.3,h))

	@Cache_error
	def up_liste_of_doc(self):
		self.liste_of_doc.clear_widgets()
		[self.liste_of_doc.add_button(i,text_color = self.sc.text_col1,
			bg_color = self.sc.orange,radius = 0,on_press = self.remove_from) 
			for i in self.documents]

	@Cache_error
	def add_develop(self):
		self.aff_ass_surf.ass_ident = self.ass_ident
		self.aff_ass_surf.add_all()

# Gestion des actions des méthodes
	@Cache_error
	def Impression(self,wid):
		obj = self.sc.imp_part_dic('Résumé')(self)
		liste = self.Trie_asso()
		entete = ["date d'ajout","nom",'catégorie',"montant dû",
			"nbres clients","contact dirigeant"]
		wid_l = .2,.19,.14,.14,.14,.19
		titre = 'Liste des affiliations'
		info = 'Agence TOKPOTA1'
		obj.Create_fact(wid_l,entete,liste,titre,info)

	@Cache_error
	def save_assos(self,wid):
		if self.check(self.new_infos):
			if self.documents:
				self.documents = [self.sc.DB.Save_image(i) for i in self.documents]
			self.ass_dic = self.sc.DB.Get_association_format()
			self.ass_dic.update(self.new_infos)
			self.ass_dic['catégorie'] = self.th_cate
			self.ass_dic["documents juridiques"] = self.documents
			self.ass_dic["autres contact"] = self.autre_cont
			self.excecute(self.sc.DB.Save_association,self.ass_dic)
			self.sc.add_refused_error('Affiliations prise en compte !')
			self.new_infos = {
				"nom":str(),
				"dirigeant":str(),
				"contact dirigeant":str(),
				"siège":str(),
				"identification":str(),
			}
			self.th_cate = str()
			self.add_liste_surf()
		else:
			self.sc.add_refused_error('Les informations ne sont pas au complète !')


	def remove_from(self,wid):
		if wid.info in self.documents:
			self.documents.remove(wid.info)
		self.up_liste_of_doc()

	def upload_fic(self,selection):
		if not selection in self.documents:
			self.documents.append(selection)
		self.up_liste_of_doc()

	def set_autre_cont(self,liste):
		for dic in liste:
			nom = dic.get('Nom')
			cont = dic.get('Téléphone ou email')
			self.autre_cont[nom] = cont

	def set_new_infos(self,wid,val):
		self.new_infos[wid.info] = val

	def close_new(self,wid):
		self.add_liste_surf()

	def new_ass(self,wid):
		self.add_new_ass()

	def set_form_t(self,info):
		self.form_t = info
		self.up_info_b()

	def set_ass_info(self,wid,val):
		self.ass_ident = val.lower()
		self.up_tab()

	def set_cate(self,info):
		self.th_cate = info
		self.up_tab()

	def show_ass(self,wid):
		if wid.info == self.ass_ident:
			self.ass_ident = str()
		else:
			self.ass_ident = wid.info
		self.add_develop()

class show_ass_info(box):
	@Cache_error
	def initialisation(self):
		self.orientation = 'horizontal'
		self.this_client = dict()
		self.th_typ = str()
		self.th_cate_client = str()
		self.this_clt_name = str()
		self.this_date_dict = {"day1":self.sc.get_today(),
			"day2":self.sc.get_today()}
		self.trie_sur_p = False
		self.size_pos()

	def size_pos(self):
		self.status_clt = str()
		self.status_l = "Ordinaire",'Douteu','Litigieu'
		self.solde_clt = str()
		self.solde_l = "Normal","Négatif","Positif"
		
		w,h = self.info_part_size = .5,1
		self.clt_part_size = 1-w, h

		self.info_part_surf = stack(self,size_hint = self.info_part_size,
			padding = dp(10),spacing = dp(5))
		self.clt_part_surf = stack(self,size_hint = self.clt_part_size, 
			padding = dp(10),spacing = dp(5))

		self.clt_surf = show_th_clt_info(self)

		self.add_surf(self.info_part_surf)
		self.add_text('',size_hint = (None,1),width = dp(1),
			bg_color = self.sc.text_col1)
		self.add_surf(self.clt_part_surf)

	@Cache_error
	def Reinit(self):
		self.clear_widgets()
		if self.this_client:
			self.clt_surf.this_client = self.this_client
			self.clt_surf.add_all()
			self.add_surf(self.clt_surf)
		else:
			self.add_surf(self.info_part_surf)
			self.add_text('',size_hint = (None,1),width = dp(1),
				bg_color = self.sc.text_col1)
			self.add_surf(self.clt_part_surf)

	@Cache_error
	def Foreign_surf(self):
		if self.ass_ident:
			self.ass_dic = self.sc.DB.Get_this_association(self.ass_ident)
			if self.ass_dic:
				self.th_cate = self.ass_dic["catégorie"]
				self.cat_list = self.sc.DB.Get_all_type_asso()
				self.autre_cont = self.ass_dic.get('autres contact')
				self.documents = self.ass_dic.get('documents juridiques')
				self.curent_doc = str()
				liste = ["nom","dirigeant","contact dirigeant","siège",
					"identification"]
				self.new_infos = {i:self.ass_dic[i] for i in liste}

				self.add_info_part_surf()
				self.add_client_part()
			else:
				self.sc.add_refused_error("Données corrompues")
				print(self.ass_ident)

	@Cache_error
	def add_info_part_surf(self):
		self.info_part_surf.clear_widgets()
		h = .045
		self.info_part_surf.add_text("Détails de l'association",
			text_color = self.sc.text_col1,halign = "center",
			underline = True,size_hint = (.9,h))
		self.info_part_surf.add_icon_but(icon = 'close',
			size_hint = (.05,h),text_color = self.sc.red,
			on_press = self.close_new)
		self.info_part_surf.add_text_input("Numéro",
			(.3,h),(.6,h),self.sc.text_col1,text_color = self.sc.orange,
			bg_color = self.sc.aff_col1,default_text = self.ass_dic.get('N°'),
			readonly = True,font_size = '20sp')
		self.info_part_surf.add_text('Catégorie',size_hint = (.3,h),
			text_color = self.sc.text_col1)
		self.info_part_surf.add_surf(liste_set(self,self.th_cate,self.cat_list,
			"V",size_hint = (.7,h),mult = 3,mother_fonc = self.set_cate))

		for k,v in self.new_infos.items():
			self.info_part_surf.add_text_input(k,(.3,h),(.6,h),
				self.sc.text_col1, text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,default_text = str(v),
				on_text = self.set_new_infos)

		d_tab = dynamique_tab(self,size_hint = (1,h*7),
			bg_color = self.sc.aff_col3)
		entete = 'Nom','Téléphone ou email'
		wid_l = .5,.5
		liste = [{"Nom":k,'Téléphone ou email':v} for k,v in self.autre_cont.items()]
		d_tab.infos_list = liste
		d_tab.Creat_Table(wid_l,entete,self.set_autre_cont)
		self.info_part_surf.add_text('Autres contactes',size_hint = (1,h),
			text_color = self.sc.text_col1,halign = 'center')
		self.info_part_surf.add_surf(d_tab)

		if self.documents:
			self.info_part_surf.add_text('Liste des documents juridiques',
				text_color = self.sc.text_col1,halign = 'center',
				size_hint = (1,h))

		self.liste_of_doc = box(self,size_hint = (1,h*1.3),
			orientation = "horizontal",spacing = dp(5))
		self.info_part_surf.add_surf(self.liste_of_doc)
		self.up_liste_of_doc()

		if "écritures" in self.sc.DB.Get_access_of('Affiliation'):
			if not self.ass_dic.get('déjà client'):
				self.info_part_surf.add_button_custom("Modifier",size_hint = (.3,h),
					bg_color = self.sc.orange,text_color = self.sc.text_col3,
					fonc = self.save_assos,padd = (.066,h))
				self.info_part_surf.add_button_custom("Sauvegarder comme un client",
					size_hint = (.5,h),padd = (.066,h),fonc = self.save_as_client)
			else:
				self.info_part_surf.add_button_custom("Modifier",size_hint = (.3,h),
					bg_color = self.sc.orange,text_color = self.sc.text_col3,
					fonc = self.save_assos,padd = (.066,h))
				self.info_part_surf.add_button_custom("Supprimer des clients",
					bg_color = self.sc.red,size_hint = (.5,h),padd = (.066,h),
					fonc = self.save_as_client)
		self.info_part_surf.add_button_custom("Accord de partenariat",
			self.set_contrat,text_color = self.sc.white,
			bg_color = self.sc.black, size_hint = (.5,h),padd = (.25,h))

	@Cache_error
	def set_contrat_surf(self):
		h = .045
		self.info_part_surf.clear_widgets()
		self.info_part_surf.add_text('Veillez vérifier les informations ci dessus',
			text_color = self.sc.text_col1,halign = "center",
			size_hint = (.9,h))
		self.info_part_surf.add_icon_but(icon = 'close',
			text_color = self.sc.red,size_hint = (.1,h),
			on_press = self.CLOS)
		for k,v in self.th_ass_d.items():
			self.info_part_surf.add_text_input(k,(.45,h),(.5,h),
				self.sc.text_col1,text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,on_text = self.set_ass_infos,
				default_text = str(v))
		self.info_part_surf.add_padd((1,.01))
		self.info_part_surf.add_button_custom('Générer',self.Set_CONT,
			text_color = self.sc.text_col3,bg_color = self.sc.orange,
			size_hint = (.4,h),padd = (.3,h))

	@Cache_error
	def up_liste_of_doc(self):
		self.liste_of_doc.clear_widgets()
		ind = 1
		for i in self.documents:
			self.liste_of_doc.add_button(f"Doc {ind}",info = i,
				text_color = self.sc.aff_col2,
				bg_color = None,halign = "left",
				radius = 0,on_press = self.remove_from) 
			ind += 1
	
	@Cache_error		
	def add_client_part(self):
		self.clt_part_surf.clear_widgets()
		h = .045
		self.clt_part_surf.add_text("Les clients membres de l'association",text_color = self.sc.text_col1,
			halign = 'center',underline = True,size_hint = (.9,.035))
		self.clt_part_surf.add_icon_but(icon ='printer',
			text_color = self.sc.black,size_hint = (.1,.035),	
			on_press = self.Impression,)
		txt_col = self.sc.orange
		if self.trie_sur_p:
			txt_col = self.sc.green
		self.clt_part_surf.add_button("Trier sur période d'ajouts",
			size_hint = (1,h),text_color = txt_col,
			halign = "left",bg_color = None,
			on_press = self.set_periode_surf)
		if self.trie_sur_p:
			self.periode_surf = Periode_set(self,size_hint = (1,h),
				info = "Période d'ajouts :",info_w = .3,
				exc_fonc = self.set_periode,date_dict = self.this_date_dict)
			self.clt_part_surf.add_surf(self.periode_surf)

		self.clt_part_surf.add_text_input('Trier par nom',(.25,h),(.65,h),
			self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,on_text = self.set_name,
			placeholder ='Trier par nom du client',
			default_text = self.this_clt_name)

		self.tab_surf = Table(self,size_hint = (1,.855),
			bg_color = self.sc.aff_col3,exec_fonc = self.show_clt,
			exec_key = "nom",padding = dp(5),radius = dp(10))

		self.clt_part_surf.add_surf(self.tab_surf)
		self.update_tab()

	@Cache_error
	def update_tab(self):
		wid_l = .4,.2,.2,.2,
		entete = "nom","chargé d'affaire","solde","tel"
		liste = self.Trie_clt()
		self.tab_surf.Creat_Table(wid_l,entete,liste,ent_size = (1,.07))

	def Trie_clt(self):
		self.ass_ident
		dic = self.sc.DB.Get_this_association(self.ass_ident)
		liste = list()
		for clt in dic.get('clients membres'):
			clt_d = self.sc.DB.Get_this_clt(clt)
			if not clt_d:
				dic["clients membres"].remove(clt)
				lll = dic.get('clients membres')
				dic['montant dû'] = float()
				for ident in lll:
					dic['montant dû']+=clt_d.get("solde",float())
				self.sc.DB.Modif_association(dic)
			else:
				liste.append(clt_d)
		
		liste = [i for i in map(self.Trie_real,liste) if i]
		return liste

	def Trie_real(self,dic):
		if dic:
			if self.th_typ:
				if self.th_typ.lower() not in dic.get('type',str()).lower():
					return False
			if self.trie_sur_p:
				date_liste = self.get_date_list(self.this_date_dict.get('day1',
					self.sc.get_today()),self.this_date_dict.get('day2',
					self.sc.get_today()))
				if dic.get("date d'enregistrement") not in date_liste:
					return False
			if self.this_clt_name.lower() not in dic.get('nom').lower():
				return None
		return dic

# Gestion des actions des méthodes
	@Cache_error
	def set_contrat(self,wid):
		#"""
		infos = ("Numéro_enregistrement","nom","tel","commune","arrondissement","addresse",
			"responsable",'fonction_responsable',"tel_responsable",
			'point_focal',"fonction_point_focal",'tel_point_focal',
			"lieu_contrat","date_contrat")
		ass_infos = self.ass_dic.get('Contrat info',dict())
		if not ass_infos:
			ass_infos['nom'] = self.ass_dic.get('nom')
			ass_infos['tel'] = self.ass_dic.get('contact dirigeant')
			ass_infos['responsable'] = self.ass_dic.get('dirigeant')
			ass_infos["tel_responsable"] = self.ass_dic.get('contact dirigeant')

		Num = ass_infos.get("Numéro_enregistrement")
		if not Num:
			ass_infos["Numéro_enregistrement"] = self.ass_dic.get('N°').split("ASSO")[-1]
		self.th_ass_d = {i:ass_infos.get(i,str()) for i in infos}
		#"""
		self.set_contrat_surf()

	def Set_CONT(self,wid):
		if self.check(self.th_ass_d):
			self.ass_dic["Contrat info"] = self.th_ass_d
			self.sc.DB.Modif_association(self.ass_dic)
			fic = os.path.abspath(f"./media/{self.th_ass_d.get('nom')}.docx")
			try:
				self.sc.Generer_doxs(os.path.abspath("./media/ASSOS.docx"),fic,
					self.th_ass_d)
				self.open_link(fic)
				self.sc.add_refused_error('Document généré')
				self.add_all()
			except:
				self.sc.add_refused_error('Vous avez un document word du même nom ouvert')
		else:
			self.sc.add_refused_error("Toutes les informations sont obligatoire")

	def set_ass_infos(self,wid,val):
		self.th_ass_d[wid.info] = val

	def CLOS(self,wid):
		self.add_all()

	def set_name(self,wid,val):
		self.this_clt_name = val
		self.update_tab()

	def set_solde_clt(self,info):
		self.solde_clt = info
		self.update_tab()

	def set_status_clt(self,info):
		self.status_clt = info
		self.update_tab()

	def save_as_client(self,wid):
		self.sc.DB.Save_as_client(self.ass_ident)

	def set_type(self,info):
		self.th_typ = info
		self.update_tab()

	def set_cate_client(self,info):
		self.th_cate = info
		self.update_tab()

	def set_periode(self):
		self.this_date_dict = self.periode_surf.date_dict
		self.update_tab()

	def set_periode_surf(self,wid):
		if self.trie_sur_p:
			self.trie_sur_p = False
		else:
			self.trie_sur_p = True

		self.add_client_part()

	def show_clt(self,wid):
		self.this_client = self.sc.DB.Get_this_clt(wid.info)
		self.Reinit()

	@Cache_error
	def Impression(self,wid):
		obj = self.sc.imp_part_dic('Résumé')(self)
		liste = self.Trie_clt()
		entete = ["date d'enregistrement","nom",'type',
		'catégorie',"solde","tel"]
		wid_l = .2,.19,.14,.14,.14,.19
		info = str()
		if self.th_typ:
			info+=f"Type de clients: {self.th_typ}<br/>"
		if self.th_cate:
			info+=f"Catégorie de clients: {self.th_cate}<br/>"
		if self.solde_clt:
			info+=f"Status de solde: {self.solde_clt}<br/>"
		if self.status_clt:
			info+=f"status du clients: {self.status_clt}<br/>"
		if self.trie_sur_p:
			info+=f"Période d'ajout: du {self.day1} au {self.day2}<br/>"
		titre = f"Clients appartenant à l'association <br/>< {self.ass_ident} >"
		info += 'Agence TOKPOTA1'
		obj.Create_fact(wid_l,entete,liste,titre,info)

	@Cache_error
	def save_assos(self,wid):
		if self.check(self.new_infos):
			if self.documents:
				self.documents = [self.sc.DB.Save_image(i) for i in self.documents]
			self.ass_dic = self.sc.DB.Get_this_association(self.ass_ident)
			self.ass_dic.update(self.new_infos)
			self.ass_dic['catégorie'] = self.th_cate
			self.ass_dic["documents juridiques"] = self.documents
			self.ass_dic["autres contact"] = self.autre_cont
			self.sc.DB.Modif_association(self.ass_dic)
			self.sc.add_refused_error('Informations Modifier')
		else:
			self.sc.add_refused_error('Les informations ne sont pas au complète !')


	def remove_from(self,wid):
		self.open_link(wid.info)

	def upload_fic(self,selection):
		if not selection in self.documents:
			self.documents.append(selection)
		self.up_liste_of_doc()

	def set_autre_cont(self,liste):
		for dic in liste:
			nom = dic.get('Nom')
			cont = dic.get('Téléphone ou email')
			self.autre_cont[nom] = cont

	def set_new_infos(self,wid,val):
		self.new_infos[wid.info] = val

	def close_new(self,wid):
		self.mother.ass_ident = str()
		self.mother.clear_widgets()
		self.mother.size_pos()
		self.mother.add_all()

	def new_ass(self,wid):
		self.add_new_ass()

	def set_form_t(self,info):
		self.form_t = info
		self.up_info_b()

	def set_ass_info(self,wid,val):
		self.ass_ident = val.lower()
		self.up_tab()

	def set_cate(self,info):
		self.th_cate = info

