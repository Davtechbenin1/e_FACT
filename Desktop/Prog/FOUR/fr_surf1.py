#Coding:utf-8
"""
	Module de définition des surfaces de gestion des fournisseurs
"""
from lib.davbuild import *
from General_surf import *
from .fr_surf2 import *
from .fr_surf3 import *

class Gestion_cmds(menu_surf_V_maquette):
	def __init__(self,mother,this_fourn_info,**kwargs):
		box.__init__(self,mother,**kwargs)
		self.this_fourn_info = this_fourn_info
		self.size_pos()
		self.initialisation()
		
	def Get_menu_infos(self):
		dic = {
			'Informations général':Gestion_fourni,
			#"Commandes":Commandes,
			#"Paiements Fournisseur":paiement_Surf,
		}
		self.wid_dict = dict()
		for i,srf in dic.items():
			if self.sc.DB.Get_access_of(i):
				self.wid_dict[i] = srf
		self.icon_dict = {
			'Informations général':"card-account-details-outline",
			"Commandes":'file-document-edit-outline',
			"Paiements Fournisseur":'cash-multiple',
		}

class Gestion_fourni(box):
	def __init__(self,mother,**kwargs):
		kwargs['bg_color'] = mother.sc.aff_col2
		box.__init__(self,mother,**kwargs)
		#self.spacing = dp(2)
		self.this_fourn_info = mother.this_fourn_info
		self.ident_list = ["nom","IFU","RCCM","addresse","email",'téléphone',
			"whatsapp"]
		self.info_ident = {i:self.this_fourn_info[i] for i in self.ident_list}
		self.respo_cont = str()
		self.curent_sect = str()
		self.size_pos()
		self.add_all()

	@Cache_error
	def Foreign_surf(self):
		self.add_part_1_surf()

	def size_pos(self):
		w,h = self.part_1_size = 1,.4
		self.part_2_size = w,1-h

		self.part_1_surf = box(self,size_hint = (1,1),
			orientation = 'horizontal',spacing = dp(2),
			padding = [0,0,dp(0),dp(2)],)

		self.add_surf(self.part_1_surf)
		#self.add_surf(self.part_2_surf)
#
	@Cache_error
	def add_part_1_surf(self):
		self.part_1_surf.clear_widgets()
		self.ident_surf = stack(self,padding = dp(20),
			bg_color = self.sc.aff_col1,spacing = dp(5),
			radius = dp(10))
		self.second_part = box(self,bg_color = self.sc.aff_col1,
			spacing = dp(5),padding = dp(10),radius = dp(10))

		self.contact_surf = stack(self,bg_color = self.sc.aff_col1)
		self.secteur_acti = stack(self,bg_color = self.sc.aff_col1)

		self.second_part.add_surf(self.contact_surf)
		self.second_part.add_surf(self.secteur_acti)

		self.part_1_surf.add_surf(self.ident_surf)
		self.part_1_surf.add_surf(self.second_part)

		#self.part_1_surf.add_surf(self.secteur_acti)
		self.add_ident_surf()
		self.add_contact_surf()
		#self.add_secteur_acti()

	def add_ident_surf(self):
		h = .06
		self.ident_surf.clear_widgets()
		for part in self.ident_list:
			self.ident_surf.add_text(part,size_hint = (1,.03))
			Get_border_input_surf(self.ident_surf,part,
				bg_color = self.sc.aff_col3,size_hint = (1,h),
				text_color = self.sc.text_col1,border_col = self.sc.aff_col3,
				default_text = self.this_fourn_info.get(part,str()),
				placeholder = part,on_text = self.set_this_fourn_info)
		self.ident_surf.add_padd((1,.02))
		self.ident_surf.add_button_custom('Valider',self.modif_fourn_info,
			padd = (.3,h),size_hint = (.4,h),text_color = self.sc.aff_col1)

	def add_contact_surf(self):
		h = .09
		self.contact_surf.clear_widgets()
		self.contact_surf.add_text("Info du directeur",
			size_hint = (1,.07),text_color = self.sc.text_col1,
			halign = 'center',underline = True)
		resp = self.this_fourn_info.get('nom directeur')
		con_respo = self.this_fourn_info.get('tél directeur')
		nom = self.this_fourn_info.get('nom directeur')
		perso_cont = self.this_fourn_info.get('personnes à contacter')
		self.pers_cont_d = perso_cont
		self.respo_cont = con_respo
		self.respo_name = nom
		self.contact_surf.add_input(nom,size_hint = (.5,h),
			text_color = self.sc.text_col1,bg_color = self.sc.aff_col1,
			on_text = self.set_respo_name,placeholder = 'Nom du Directeur',
			default_text = nom)
		self.contact_surf.add_input(resp,size_hint = (.5,h),
			text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
			default_text = con_respo,placeholder = "Contact du Directeur",
			on_text = self.set_respo_conta)
		this_surf = dynamique_tab(self,size_hint = (1,.75))
		th_l = list()
		wid_l = [.7,.3]
		entete = 'Nom',"Contact"
		for k,v in perso_cont.items():
			d = {"Nom":k,'Contact':v}
			th_l.append(d)
		this_surf.infos_list = th_l
		this_surf.Creat_Table(wid_l,entete,mother_fonc = self.set_all_perso)
		self.contact_surf.add_text('Autres contacts',size_hint = (1,.07),
			text_color = self.sc.text_col1,halign = 'center',
			underline = True)
		self.contact_surf.add_surf(this_surf)

	"""
	def add_secteur_acti(self):
		h = .1
		self.secteur_acti.clear_widgets()
		self.secteur_acti.add_text('Types',size_hint = (.2,h),
			text_color = self.sc.text_col1)
		self.type_set = self.this_fourn_info.get('type de fournisseur')
		self.secteur_set = self.this_fourn_info.get("secteur d'activité")
		self.secteur_acti.add_surf(liste_set(self,self.type_set,
			self.sc.DB.Get_all_f_types(),mult = 1,mother_fonc = self.set_typ,
			size_hint = (.8,h)))
		B = box(self,size_hint = (1,h),spacing = dp(3),orientation = "horizontal")
		B.add_text_input("Secteurs d'activité",(.38,1),(.6,1),
			self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,default_text = self.curent_sect,
			on_text = self.set_secteur,placeholder = 'Trier',)
		B.add_icon_but(icon = "plus",size_hint = (None,1),
			text_color = self.sc.orange,on_press = self.New_sect,
			size = (dp(35),dp(35)))
		self.secteur_acti.add_surf(B)
		self.all_liste_surf = liste_choice(self,self.secteur_set,
			self.sc.DB.Get_Secteurs(),mother_fonc = self.modif_sect,
			size_hint = (1,.7))
		self.secteur_acti.add_surf(self.all_liste_surf)
		self.secteur_acti.add_button_custom("Modifer",self.modif_secteur,
			size_hint = (.5,h),padd = (.25,h),text_color = self.sc.aff_col1)
	"""

	def up_trie(self):
		self.all_liste_surf.info_l = self.secteur_set
		self.all_liste_surf.list_info = [i for i in self.sc.DB.Get_Secteurs()
			if self.curent_sect.lower() in i.lower()]

		self.all_liste_surf.add_all()

# Gestion des actions des fournisseurs
	@Cache_error
	def modif_secteur(self,wid):
		if "écritures" in self.sc.DB.Get_access_of('Informations général'): 
			self.this_fourn_info["secteur d'activité"] = self.secteur_set
			self.this_fourn_info['type de fournisseur'] = self.type_set
			self.this_fourn_info["tél directeur"] = self.respo_cont
			self.this_fourn_info['nom directeur'] = self.respo_name
			self.this_fourn_info['personnes à contacter'] = self.pers_cont_d
			self.excecute(self.sc.DB.Modif_fournisseur,self.this_fourn_info)
			#self.sc.DB.Modif_fournisseur(self.this_fourn_info)
			self.mother.mother.add_all()
			self.sc.add_refused_error("Informations modifier")
		else:
			self.sc.add_refused_error("Impossible de continuer à cause d'une restriction système !! Parlez-en à votre supérieur hiérachique")

	def modif_sect(self,liste):
		self.secteur_set = liste

	def set_secteur(self,wid,val):
		self.curent_sect = val
		self.up_trie()

	@Cache_error
	def New_sect(self,wid):
		if "écritures" in self.sc.DB.Get_access_of('Informations général'):
			if self.curent_sect:
				self.excecute(self.sc.DB.Save_secteurs,self.curent_sect)
				self.secteur_set.append(self.curent_sect)
				self.curent_sect = str()
				self.up_trie()
		else:
			self.sc.add_refused_error("Impossible de continuer à cause d'une restriction système !! Parlez-en à votre supérieur hiérachique")

	def set_this_fourn_info(self,wid,val):
		self.info_ident[wid.info] = val

	@Cache_error
	def modif_fourn_info(self,wid):
		if "écritures" in self.sc.DB.Get_access_of('Informations général'):
			self.this_fourn_info.update(self.info_ident)
			self.excecute(self.sc.DB.Modif_fournisseur,self.this_fourn_info)
			self.sc.add_refused_error('Identité du fournisseur modifier avec succès !')
		else:
			self.sc.add_refused_error("Impossible de continuer à cause d'une restriction système !! Parlez-en à votre supérieur hiérachique")

	def set_respo_conta(self,wid,val):
		self.respo_cont = val

	def set_respo_name(self,wid,val):
		self.respo_name = val

	def set_all_perso(self,liste):
		self.pers_cont_d = dict()
		for d in liste:
			self.pers_cont_d[d.get('Nom')] = d.get('Contact')

	def set_typ(self,info):
		self.type_set = info





