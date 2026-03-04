#Coding:utf-8
from lib.davbuild import *
from General_surf import *

class Info_client(stack):
	@Cache_error
	def initialisation(self):
		h = .05
		self.spacing = dp(10)
		self.padding = dp(10)
		self.this_client = self.mother.this_client
		self.type_client = "Personnes physiques"
		if self.this_client.get('type') == "entreprise":
			self.type_client = "Personnes morales"

		self.add_text("Fiche d'enrégistrement client des :",
			size_hint = (.18,h),text_color = self.sc.text_col1,
			font_size = '16sp',halign = 'right')
		self.add_surf(liste_set(self,self.type_client,['Personnes physiques',
			"Personnes morales"],size_hint = (.12,h),mult = 1,
			mother_fonc = self.set_type_client))
		self.add_text_input("Date d'enrégistrement:",(.11,h),(.09,h),
			self.sc.text_col1,text_halign = "right",
			text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,default_text = self.this_client.get("date d'enregistrement"),
			readonly = True)
		self.add_text_input("N° d'enrégistrement :",(.11,h),(.09,h),
			self.sc.text_col1,text_halign = "right",
			text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,
			default_text = self.this_client.get('N°'),
			readonly = True)
		if "écritures" in self.sc.DB.Get_access_of("Clients"):
			self.add_button_custom('Modifer',self.New_clt,size_hint = (.1,h),
				padd = (.05,h),text_color = self.sc.aff_col1)
			self.add_button_custom('Modifer et Imprimée',
				self.New_clt_imp,size_hint = (.1,h),
				padd = (.05,h),bg_color = self.sc.orange,
				text_color = self.sc.aff_col1)
		else:
			self.add_button_custom('Imprimée',self.clt_imp,size_hint = (.1,h),
				padd = (.05,h),bg_color = self.sc.orange)

		self.curent_part = str()
		self.size_pos()
		self.Init_info()

		self.infos_dict = {
			"Information Personnelles du client":self.add_info_client(),
			"Information sur son Avaliseur":self.add_info_avaliseur(),
			"Information financier du client":self.add_info_commercial(),
			#"Autres":self.add_info_affiliation()
		}

	@Cache_error
	def Init_info(self):
		self.client_info_dic = {
			"nom":str(),
			"prénom":str(),
			"date de naissance":str(),
			"lieu de naissance":str(),
			"Nationalité":"Béninoise",
			"profession":str(),
			"quartier":str(),
			"ville":str(),
			"maison":str(),
			"N° tel":str(),
			"N° Whatsapp":str(),
			"IFU":str(),
			"N° pièce d'identité":str(),
			"Type de pièce":str(),
			"Date de délivrance":str(),
			"Date d'expiration":str(),
			"Personne à contacter":str(),
			"Téléphone personne à contacter":str()
		}
		inf_clt = self.this_client.get('infos_document',dict())
		all_nam = self.this_client.get('nom').replace('_'," ")
		nom = all_nam.split(' ')[0]
		prenom = ' '.join(all_nam.split(' ')[1:])
		if not inf_clt:
			inf_clt['nom'] = nom
			inf_clt['prénom'] = prenom
			inf_clt['N° tel'] = self.this_client.get('tel')
			inf_clt['N° Whatsapp'] = self.this_client.get('whatsapp')
			inf_clt['ville'] = self.this_client.get('ville')
			inf_clt['quartier'] = self.this_client.get('quartier')
			inf_clt['maison'] = self.this_client.get('maison')
			inf_clt['profession'] = self.this_client.get('profession')
			inf_clt['IFU'] = self.this_client.get('IFU')

		for k,v in inf_clt.items():
			if k in self.client_info_dic:
				self.client_info_dic[k] = v

		self.avaliseur_info_dic = {
			"nom":str(),
			"prénom":str(),
			"date de naissance":str(),
			"lieu de naissance":str(),
			"Nationalité":"Béninoise",
			"profession":str(),
			"quartier":str(),
			"ville":str(),
			"maison":str(),
			"N° tel":str(),
			"N° Whatsapp":str(),
			"N° pièce d'identité":str(),
			"Type de pièce":str(),
			"Date de délivrance":str(),
			"Date d'expiration":str(),
		}
		inf_clt = self.this_client.get('infos_avaliseur',dict())
		for k,v in inf_clt.items():
			if k in self.avaliseur_info_dic:
				self.avaliseur_info_dic[k] = v

		
		self.info_finance = {
			"type d'activité":str(),
			"Addresse":str(),
			"Nature de votre bésoin":str(),
			"Montant d'achat estimé":str(),
			"Recette Journalière":str(),
			"Revenu mensuel":str(),
			"Autres informations":str(),
		}
		inf_clt = self.this_client.get('finance_infos',dict())
		for k,v in inf_clt.items():
			if k in self.info_finance:
				self.info_finance[k] = v
		
		self.aff_set = self.this_client.get("lien d'affiliation")
		self.liste_aff = []#self.sc.DB.Get_association_list()

		self.charger = self.this_client.get("chargé d'affaire")
		self.liste_charger = dict() #self.sc.get_all_charger()

	@Cache_error
	def Foreign_surf(self):
		self.set_but_part()

	def size_pos(self):

		self.info_client = stack(self,size_hint = (.55,.65),
			bg_color = self.sc.orange,padding = dp(10),
			spacing = dp(10),radius = dp(10))
		self.info_avaliseur = stack(self,size_hint = (.55,.65),
			bg_color = self.sc.green,padding = dp(10),
			spacing = dp(10),radius = dp(10))
		#self.add_surf(self.info_client)
		#self.add_surf(self.info_avaliseur)

		self.info_commercial = stack(self,size_hint = (.5,.6),
			spacing = dp(10),padding = dp(10),
			bg_color = (.3,.3,.35),radius = dp(10))

		self.info_affiliation = stack(self,size_hint = (.5,.6),
			spacing = dp(10),padding = dp(10))
		self.add_padd((1,.02))

		#self.add_surf(self.info_commercial)
		#self.add_surf(self.info_affiliation)

		self.but_part = box(self,size_hint =(.15,.9),padding = dp(20),
			spacing = dp(50))

		self.Aff_part = stack(self,size_hint =(.85,.9),
			padding_top = dp(50))

		self.add_surf(self.but_part)
		self.add_surf(self.Aff_part)

	@Cache_error
	def set_but_part(self):
		self._set_but_()
		self.up_aff_part()

	def _set_but_(self):
		self.but_part.clear_widgets()
		clt_pourc = self.get_pource_of(self.client_info_dic)
		aval_pourc = self.get_pource_of(self.avaliseur_info_dic)
		fina_pourc = self.get_pource_of(self.info_finance)
		dic = {
			"Information Personnelles du client":clt_pourc,
			"Information sur son Avaliseur":aval_pourc,
			"Information financier du client":fina_pourc,
			#"Autres":''
		}
		for k,v in dic.items():
			if not self.curent_part:
				self.curent_part = k
			bg_col = self.sc.aff_col3
			if self.curent_part == k:
				bg_col = self.sc.aff_col2
			b = box(self,bg_color = bg_col,
				radius = dp(20))
			b.add_button(k,size_hint = (1,.65),bg_color = None,
				info = k,on_press = self.change_but_part,
				font_size ="18sp",text_color = self.sc.text_col1)
			b.add_button(v,size_hint = (1,.35),bg_color = None,
				info = k,on_press = self.change_but_part,
				font_size = "15sp",text_color = self.sc.red)
			self.but_part.add_surf(b)

	def up_aff_part(self):
		self.Aff_part.clear_widgets()
		curent_surf = self.infos_dict.get(self.curent_part)
		self.Aff_part.add_padd((.25,1))
		self.Aff_part.add_surf(curent_surf)

	@Cache_error
	def change_but_part(self,wid):
		self.curent_part = wid.info
		self.add_all()

	def get_pource_of(self,dic):
		vals = dic.values()
		th_v = int()
		tot_ = int()
		for v in vals:
			if v:
				th_v += 1
			tot_ += 1
		return f"{round((th_v*100)/tot_,1)}% Terminées"

	def add_info_client(self):
		self.info_client.clear_widgets()
		self.info_client.add_text('Informations Personnelles du client',
			text_color = self.sc.aff_col3,font_size = "18sp",
			size_hint = (1,.08))
		for k,v in self.client_info_dic.items():
			self.info_client.add_surf(self.add_info(k,v,
				self.modif_clt,.13))
		return self.info_client

	def add_info_avaliseur(self):
		self.info_avaliseur.clear_widgets()
		self.info_avaliseur.add_text("Informations Personnelles sur l'avaliseur",
			text_color = self.sc.aff_col3,font_size = "18sp",
			size_hint = (1,.08))
		for k,v in self.avaliseur_info_dic.items():
			self.info_avaliseur.add_surf(self.add_info(k,v,
				self.modif_aval))
		return self.info_avaliseur

	def add_info(self,k,v,fonc,height = .16):
		b = box(self,size_hint = (.33,height),padding = [dp(10),dp(0),dp(10),dp(5)],
			radius = dp(10),bg_color = self.sc.aff_col1)
		b.add_text_input(k,(1,.45),(1,.55),self.sc.text_col1,
			text_color = self.sc.text_col1, bg_color = self.sc.aff_col3,
			default_text = self.format_val(v),on_text = fonc)
		return b

	def add_info_commercial(self):
		self.info_commercial.clear_widgets()
		self.info_commercial.add_text("Informations Commerciales et financières",
			size_hint = (1,.12),text_color = self.sc.aff_col1,
			underline = True,font_size = '18sp')
		for k,v in self.info_finance.items():
			if k != "Autres informations":
				self.info_commercial.add_surf(self.add_info(k,v,self.modif_finance,
					height = .2))
		self.info_commercial.add_text_input("Autres informations",
			(.15,.17),(.84,.37),self.sc.text_col3,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,default_text =
			self.info_finance.get("Autres informations"),
			on_text = self.modif_finance,multiline = True)
		return self.info_commercial

	def add_info_affiliation(self):
		self.info_affiliation.clear_widgets()
		self.info_affiliation.add_text("Lien d'affiliation :",
			size_hint = (.2,.2),text_color = self.sc.aff_col3,
			valign = 'top')
		self.info_affiliation.add_surf(liste_set(self,self.aff_set,
			self.liste_aff,"V",size_hint = (.3,.1),mult = 10,
			mother_fonc = self.set_aff_set))
		self.info_affiliation.add_text("Chargé d'affaire :",
			size_hint = (.2,.2),text_color = self.sc.text_col1,
			valign = 'top')
		self.info_affiliation.add_surf(liste_set(self,self.charger,
			self.liste_charger,"V",size_hint = (.3,.1),mult = 10,
			mother_fonc = self.set_char_set))
		return self.info_affiliation

# Gestion des actions des bouttons
	def modif_clt(self,wid,val):
		self.client_info_dic[wid.info] = val
		self._set_but_()

	def modif_aval(self,wid,val):
		self.avaliseur_info_dic[wid.info] = val
		self._set_but_()

	def modif_finance(self,wid,val):
		self.info_finance[wid.info] = val
		self._set_but_()

	@Cache_error
	def _New_clt(self,*wid,save= True):
		th_nom = self.client_info_dic.get('nom')
		if not th_nom:
			self.sc.add_refused_error("Les informations du clients sont obligatoires")
			return str()
		th_nom += ' '+self.client_info_dic.get("prénom")
		th_nom = th_nom.strip()
		if len(th_nom) < 5:
			self.sc.add_refused_error('Le nom du client doit dépasser 5 carractères')
			return str()
		clt_typ = "particulier"
		if "morales" in self.type_client:
			clt_typ = "entreprise"
		clt_dic = self.this_client
		self.client_info_dic['n'] = clt_dic['N°']
		self.client_info_dic["date d'enregistrement"] = clt_dic["date d'enregistrement"]
		clt_localite = f"Bénin, {self.client_info_dic['ville']}, {self.client_info_dic['quartier']}, maison:{self.client_info_dic['maison']}"
		clt_dic['nom'] = th_nom
		clt_dic["association appartenue"] = self.aff_set
		clt_dic["lien d'affiliation"] = self.aff_set
		clt_dic["chargé d'affaire"] = self.charger
		clt_dic['pays'] = "Bénin"
		clt_dic['tel'] = self.client_info_dic['N° tel']
		clt_dic['whatsapp'] = self.client_info_dic['N° Whatsapp']
		clt_dic['ville'] = self.client_info_dic['ville']
		clt_dic['quartier'] = self.client_info_dic['quartier']
		clt_dic['maison'] = self.client_info_dic['maison']
		clt_dic['localité'] = clt_localite
		clt_dic['profession'] = self.client_info_dic['profession']
		clt_dic['infos_document'] = self.client_info_dic
		clt_dic['infos_avaliseur'] = self.avaliseur_info_dic
		clt_dic["finance_infos"] = self.info_finance
		clt_dic['nom du client'] = self.client_info_dic['nom']
		clt_dic['prénom du client'] = self.client_info_dic['prénom']

		clt_dic['date de naissance'] = self.client_info_dic['date de naissance']
		clt_dic['lieu de naissance'] = self.client_info_dic['lieu de naissance']
		clt_dic['Personne à contacter'] = self.client_info_dic['Personne à contacter']
		clt_dic["Téléphone personne à contacter"] = self.client_info_dic["Téléphone personne à contacter"]
		if save:
			self.sc.DB.Update_client(clt_dic)
		return True

	@Cache_error
	def New_clt(self,*args):
		if self._New_clt():
			self.sc.add_refused_error(f"Client modifier")
			self.Init_info()
			self.add_all()

	@Cache_error
	def clt_imp(self,wid):
		self.New_clt_imp(save = False)

	@Cache_error
	def New_clt_imp(self,*wid,save = True):
		all_dict = dict()
		if self._New_clt(save):
			client_info = self.redo_dic(self.client_info_dic,"clt")
			avalis_info = self.redo_dic(self.avaliseur_info_dic,"aval")
			financ_info = self.redo_dic(self.info_finance,'fin')
			all_dict.update(client_info)
			all_dict.update(avalis_info)
			all_dict.update(financ_info)
			all_dict["lien_affiliation"] = self.aff_set
			#print(all_dict)

			fic = os.path.abspath(f"./media/{all_dict.get('cltnom')}.docx")
			#try:
			self.sc.Generer_doxs(os.path.abspath("./media/DEMANDE.docx"),
				fic,all_dict)
			self.open_link(fic)
			#self.sc.add_refused_error('Document généré')
			#except:
			#	self.sc.add_refused_error('Vous avez un document word du même nom ouvert')
			self.Init_info()
			self.add_all()

	def set_aff_set(self,info):
		self.aff_set = info

	def set_char_set(self,info):
		self.charger = info

	def set_type_client(self,info):
		self.type_client = info

	def redo_dic(self,dic,key):
		th_dic = dict()
		for k,v in dic.items():
			th_k = self.redo_key(k)
			th_dic[key+th_k] = v
		return th_dic

	def redo_key(self,key):
		HHH = 'abcdefghijklmnopqrstuvwxyz '+"1234567890"
		K = str()
		for i in key:
			i = i.lower()
			if i in HHH:
				K += i
		return K.replace(' ',"_")

class New_clt_surf(Info_client):
	@Cache_error
	def initialisation(self):
		h = .05
		self.padding = dp(10)
		self.spacing = dp(10)
		self.type_client = "Personnes physiques"
		self.add_text("Fiche d'enrégistrement client des :",
			size_hint = (.18,h),text_color = self.sc.text_col1,
			font_size = '16sp',halign = 'right')
		self.add_surf(liste_set(self,self.type_client,['Personnes physiques',
			"Personnes morales"],size_hint = (.12,h),mult = 1,
			mother_fonc = self.set_type_client))
		self.add_text_input("Date d'enrégistrement:",(.11,h),(.17,h),
			self.sc.text_col1,text_halign = "right",
			text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,
			default_text = self.sc.get_today(),
			readonly = True)
		

		self.add_button_custom('Valider',self.New_clt,size_hint = (.1,h),
			padd = (.025,h),text_color = self.sc.aff_col3)
		self.add_button_custom('Valider et Imprimée',self.New_clt_imp,size_hint = (.1,h),
			padd = (.025,h),bg_color = self.sc.orange,text_color = self.sc.aff_col3)
		self.curent_part = str()
		self.size_pos()
		self.Init_info()
		self.infos_dict = {
			"Information Personnelles du client":self.add_info_client(),
			"Information sur son Avaliseur":self.add_info_avaliseur(),
			"Information financier du client":self.add_info_commercial(),
			#"Autres":self.add_info_affiliation()
		}

	@Cache_error
	def Init_info(self):
		self.client_info_dic = {
			"nom":str(),
			"prénom":str(),
			"date de naissance":str(),
			"lieu de naissance":str(),
			"Nationalité":"Béninoise",
			"profession":str(),
			"quartier":str(),
			"ville":str(),
			"maison":str(),
			"N° tel":str(),
			"N° Whatsapp":str(),
			"IFU":str(),
			"N° pièce d'identité":str(),
			"Type de pièce":str(),
			"Date de délivrance":str(),
			"Date d'expiration":str(),
			"Personne à contacter":str(),
			"Téléphone personne à contacter":str()
		}

		self.avaliseur_info_dic = {
			"nom":str(),
			"prénom":str(),
			"date de naissance":str(),
			"lieu de naissance":str(),
			"Nationalité":"Béninoise",
			"profession":str(),
			"quartier":str(),
			"ville":str(),
			"maison":str(),
			"N° tel":str(),
			"N° Whatsapp":str(),
			"N° pièce d'identité":str(),
			"Type de pièce":str(),
			"Date de délivrance":str(),
			"Date d'expiration":str(),
		}
		
		self.info_finance = {
			"type d'activité":str(),
			"Addresse":str(),
			"Nature de votre bésoin":str(),
			"Montant d'achat estimé":str(),
			"Recette Journalière":str(),
			"Revenu mensuel":str(),
			"Autres informations":str(),
		}
		
		self.aff_set = str()
		#self.liste_aff = self.sc.DB.Get_association_list()

		self.charger = str()
		self.liste_charger = dict() #self.sc.get_all_charger()

# Gestion des actions des bouttons
	@Cache_error
	def _New_clt(self,*wid):
		th_nom = self.client_info_dic.get('nom')
		if not th_nom:
			self.sc.add_refused_error("Les informations du clients sont obligatoires")
			return str()
		th_nom += ' '+self.client_info_dic.get("prénom")
		th_nom = th_nom.strip()
		if len(th_nom) < 5:
			self.sc.add_refused_error('Le nom du client doit dépasser 5 carractères')
			return str()
		clt_dic = dict()
		clt_localite = f"Bénin, {self.client_info_dic['ville']}, {self.client_info_dic['quartier']}, maison:{self.client_info_dic['maison']}"
		clt_dic['nom'] = th_nom
		clt_dic["association appartenue"] = self.aff_set
		clt_dic["lien d'affiliation"] = self.aff_set
		clt_dic["chargé d'affaire"] = self.charger
		clt_dic['pays'] = "Bénin"
		clt_dic['tel'] = self.client_info_dic['N° tel']
		clt_dic['whatsapp'] = self.client_info_dic['N° Whatsapp']
		clt_dic['ville'] = self.client_info_dic['ville']
		clt_dic['quartier'] = self.client_info_dic['quartier']
		clt_dic['maison'] = self.client_info_dic['maison']
		clt_dic['localité'] = clt_localite
		clt_dic['profession'] = self.client_info_dic['profession']
		clt_dic['infos_document'] = self.client_info_dic
		clt_dic['infos_avaliseur'] = self.avaliseur_info_dic
		clt_dic["finance_infos"] = self.info_finance
		clt_dic['nom du client'] = self.client_info_dic['nom']
		clt_dic['prénom du client'] = self.client_info_dic['prénom']

		clt_dic['date de naissance'] = self.client_info_dic['date de naissance']
		clt_dic['lieu de naissance'] = self.client_info_dic['lieu de naissance']
		clt_dic['Personne à contacter'] = self.client_info_dic['Personne à contacter']
		clt_dic["Téléphone personne à contacter"] = self.client_info_dic["Téléphone personne à contacter"]
		self.sc.DB.Save_client(clt_dic)
		return True

	def New_clt(self,*args):
		if self._New_clt():
			self.sc.add_refused_error(f"Client {self.client_info_dic.get('nom')} ajouter avec succès")
			self.Init_info()
			self.mother.close_modal()

	@Cache_error
	def New_clt_imp(self,*wid):
		all_dict = dict()
		if self._New_clt():
			client_info = self.redo_dic(self.client_info_dic,"clt")
			avalis_info = self.redo_dic(self.avaliseur_info_dic,"aval")
			financ_info = self.redo_dic(self.info_finance,'fin')
			all_dict.update(client_info)
			all_dict.update(avalis_info)
			all_dict.update(financ_info)
			all_dict["lien_affiliation"] = self.aff_set

			fic = os.path.abspath(f"./media/{all_dict.get('nom')}.docx")
			try:
				self.sc.Generer_doxs(os.path.abspath("./media/DEMANDE.docx"),
					fic,all_dict)
				self.open_link(fic)
				self.sc.add_refused_error('Document généré')
				self.mother.close_modal()
			except:
				self.sc.add_refused_error('Vous avez un document word du même nom ouvert')
			self.Init_info()
			self.mother.close_modal()

	def set_aff_set(self,info):
		self.aff_set = info

	def set_char_set(self,info):
		self.charger = info

	def set_type_client(self,info):
		self.type_client = info

	def redo_dic(self,dic,key):
		th_dic = dict()
		for k,v in dic.items():
			th_k = self.redo_key(k)
			th_dic[key+th_k] = v
		return th_dic

	def redo_key(self,key):
		HHH = 'abcdefghijklmnopqrstuvwxyz_'+"1234567890"
		K = str()
		for i in key:
			l = i.lower()
			if i in HHH:
				K += i
		return K.replace(' ',"_")






