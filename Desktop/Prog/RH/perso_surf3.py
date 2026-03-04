#Coding:utf-8
"""
	Gestion des objets surface relatif à la gestion du 
	personnel même de l'entreprise
"""
from .perso_surf4 import *
from .perso_surf import Define_surf

class Personal_surf(box):
	def __init__(self,mother,perso_ident,**kwargs):
		kwargs['padding'] = dp(10)
		kwargs['spacing'] = dp(5)
		kwargs['radius'] = dp(10)
		box.__init__(self,mother,**kwargs)
		self.perso_ident = perso_ident

		self.size_pos()

	@Cache_error
	def Foreign_surf(self):
		self.this_perso = self.sc.DB.Get_this_perso(
			self.perso_ident)
		self.add_first_info()

	def size_pos(self):
		w,h = self.first_info_size = 1,.25

		self.second_size = 1,1-h

		self.first_info_surf = box(self,
			size_hint = self.first_info_size,
			orientation = "horizontal",
			bg_color = self.sc.aff_col1)

		self.add_surf(self.first_info_surf)

	@Cache_error
	def add_first_info(self):
		self.first_info_surf.clear_widgets()
		img = self.this_perso.get('img')
		if not img:
			img = "media/logo.png"
		self.img_surf = float_l(self,size_hint = (.33,.5),
			pos_hint = (0,.55))
		self.img_surf.add_image(img)
		
		self.first_info_surf.add_surf(self.img_surf)
		self.infos_surf = stack(self,size_hint = (.66,1),
			spacing = dp(5),padding = dp(5),radius = dp(10))

		self.first_info_surf.add_surf(self.infos_surf)
		self.add_info_surf()

	def add_img_surf(self):
		self.img_surf.clear_widgets()
		img = self.this_perso.get('img')
		if not img:
			img = "media/logo.png"
		self.img_surf.add_image(img)
		self.img_surf.add_button("",on_press = self.get_img_from,
			bg_color = None)

	@Cache_error
	def add_info_surf(self):
		h = .05
		self.infos_surf.clear_widgets()
		liste1 = ["nom","prénom","poste actuel",
		"pays de résidence",
		"ville de résidence","quartier","nationalité","NIP",
		"date de prise de fonction","téléphone","whatsapp","email",]
		dic = {i:self.this_perso.get(i) for i in liste1}
		for k,v in dic.items():
			read = True
			bg_col = self.sc.aff_col3
			if k == "date de prise de fonction":
				k = "Prise de fonction"
			self.infos_surf.add_text(k,size_hint = (.25,h),
				text_color = self.sc.text_col1)
			self.infos_surf.add_text(str(v),size_hint = (.25,h),
				text_color = self.sc.aff_col2,)

				
		buts = ["Voir le cv","Voir le contrat"]
		for k in buts:
			self.infos_surf.add_button(k,size_hint = (.2,h),
				text_color = self.sc.aff_col2,bg_color = None,
				on_press = self.gene_actions,halign = 'left',
				font_size = '17sp')

# Gestion des actions au niveau des buttons
	def gene_actions(self,wid):
		if wid.info == 'Voir le cv':
			lien = self.this_perso.get('cv',str())
		elif wid.info == "Voir le contrat":
			lien = self.this_perso.get("contrat de travail",str())
		if not lien:
			self.sc.add_refused_error("Lien non valide")
		else:
			self.open_link(lien)

class General(Define_surf):
	perso_ident = str()
	new_fic = False
	def __init__(self,mother,ident,**kwargs):
		kwargs['spacing'] = 0
		kwargs["padding"] = dp(5)
		Define_surf.__init__(self,mother,**kwargs)
		self.perso_ident = ident

	def Get_menu_infos(self):
		dic = {
			"Salaires":Salaires,
			"Définir missions":Missions,
			"Histo missions":H_missions,
			"Gestion général":Gestion,
			"Activitées":Activites,
		}
		self.menu_dict = dict()

		for i,srf in dic.items():
			if not self.curent_menu:
				self.curent_menu = i
			self.menu_dict[i] = srf(self,orientation = "horizontal")

class Salaires(box):
	@Cache_error
	def initialisation(self):
		self.status = str()
		self.status_list = ["Payée","Non payée"]
		self.perso_ident = str()#self.mother.perso_ident
		self.fiche_ident = str()
		self.size_pos()

	def size_pos(self):
		w,h = self.liste_size = .4,1
		self.details_size = 1-w,h

		self.liste_surf = stack(self,size_hint = self.liste_size,
			spacing = dp(5),padding = dp(10))
		self.details_surf = fiche_show(self,dict(),size_hint = self.details_size,
			spacing = dp(5),padding = dp(10))

		self.add_surf(self.liste_surf)
		self.add_text('',size_hint = (None,1),width = dp(1),
			bg_color = self.sc.sep)
		self.add_surf(self.details_surf)

	@Cache_error
	def Foreign_surf(self):
		self.add_liste_surf()
		self.add_details_surf()

	def add_liste_surf(self):
		h = .035
		self.liste_surf.clear_widgets()
		
		self.liste_surf.add_text('Choix du personnel',text_color = self.sc.text_col1,
			size_hint = (.3,.035))
		input_search_new(self.liste_surf,self.perso_ident,
			self.sc.get_devers_perso(),self.set_perso_ident,
			size_hint = (.7,.035))

		if self.perso_ident:
			self.liste_surf.add_text("Liste des fiches de paie",
				size_hint = (.8,h),underline = True,text_color = self.sc.text_col1,
				halign = 'center')
			if "écritures" in self.sc.DB.Get_access_of('Salaires'):
				self.liste_surf.add_icon_but(icon = 'plus',text_color = self.sc.green,
					on_press = self.New_fiche,size_hint = (.2,h))
			self.liste_surf.add_text('status',size_hint = (.2,h),text_color = self.sc.text_col1)
			self.liste_surf.add_surf(liste_set(self,self.status,self.status_list,
				mother_fonc = self.set_status,mult = 1,size_hint = (.8,h)))

			self.tab_surf = Table(self,bg_color = self.sc.aff_col3,
				padding = dp(10),radius = dp(10),exec_fonc = self.show_fiche,
				exec_key = 'N°',size_hint = (1,.83))
			self.liste_surf.add_surf(self.tab_surf)
			self.add_tab_surf()

	@Cache_error
	def add_tab_surf(self):
		entete = "date d'émissions","montant total","status"
		wid_l = .3,.35,.35
		liste = self.Trie_fich()
		self.tab_surf.Creat_Table(wid_l,entete,liste,ent_size = (1,.06))

	def Trie_fich(self):
		dic = self.sc.DB.Get_this_perso_fichs(self.perso_ident)
		liste = [j for i,j in dic.items()]
		if self.status:
			liste = [j for j in liste if self.status.lower() == j.get('status').lower()]
		return liste

	def add_details_surf(self):
		pass

# Gestion des actions des méthodes
	def set_perso_ident(self,info):
		self.perso_ident = info
		self.add_all()

	def set_status(self,info):
		self.status = info
		self.add_tab_surf()

	def show_fiche(self,wid):
		self.new_fic = False
		self.fiche_ident = wid.info
		fich_dic = self.sc.DB.Get_this_fiche_paie(self.perso_ident,wid.info)
		self.details_surf.fiche_info = fich_dic
		self.details_surf.New = False
		self.details_surf.add_all()

	def New_fiche(self,wid):
		self.details_surf.New = True
		self.details_surf.fiche_info = dict()
		self.details_surf.add_all()

class fiche_show(stack):
	def __init__(self,mother,fiche_info,**kwargs):
		stack.__init__(self,mother,**kwargs)
		self.fiche_info = fiche_info
		self.ident = str()#self.mother.perso_ident
		self.perso_info = dict()
		self.poste_info = dict()
		if self.ident:
			self.perso_info = self.sc.DB.Get_this_perso(self.ident)
			self.poste_info = self.sc.DB.Get_this_poste(self.perso_info.get('poste actuel'))
		if not self.fiche_info:
			self.New = True
		else:
			self.New = False

		self.deduction_liste = ["Manquant","Casse de produits","Retard",
			"Incompétence","Insubordination","Autres"]

	@Cache_error
	def Foreign_surf(self):
		h = .05
		self.ident = self.mother.perso_ident
		if self.ident:
			self.perso_info = self.sc.DB.Get_this_perso(self.ident)
			self.poste_info = self.sc.DB.Get_this_poste(self.perso_info.get('poste actuel'))
		
		self.clear_widgets()
		if self.New:
			txt = 'Nouvelle fiche de paie'
		else:
			txt = "Détails de la fiche de paie"
		self.add_text(txt,halign = "center",text_color = self.sc.text_col1,
			underline = True,size_hint = (1,.035))
		addresse = ','.join([self.perso_info.get('pays de résidence'),
			self.perso_info.get('ville de résidence'),self.perso_info.get('quartier'),
			self.perso_info.get('maison')])
		aug = self.perso_info.get('augmentation',float())
		self.info_dic1 = {
			"nom":self.perso_info.get('nom'),
			"prénom":self.perso_info.get('prénom'),
			"téléphone":self.perso_info.get('téléphone'),
			"addresse":addresse,
			"poste actuel":self.perso_info.get('poste actuel'),
			"type de personel":self.perso_info.get('type'),
			"salaire minimum":self.poste_info.get('salaire minimal'),
			"augmentation":aug
		}
		for k,v in self.info_dic1.items():
			try:
				float(v)
			except:
				pass
			else:
				v = self.format_val(v)
			self.add_text(k + " :",size_hint = (.18,h),text_color = self.sc.text_col1,
				)
			self.add_text(v,size_hint = (.32,h),text_color = self.sc.text_col1,
				)
			
		self.modif_dic = {
			"Prime":self.fiche_info.get('prime',float()),
			"Déduction":self.fiche_info.get('déduction',float()),
			"Objet de déduction":self.fiche_info.get('objet de déduction',str()),
			"détails":self.fiche_info.get('détails du déduction',str())
		}
		self.add_text('Définition des autres montants',
			size_hint = (1,h*1.5),text_color = self.sc.text_col1,
			underline = True, font_size = "20sp",halign = "center")
		for k,v in self.modif_dic.items():
			if k in ("Prime","Déduction"):
				try:
					float(v)
				except:
					pass
				else:
					v = self.format_val(v)
				self.add_padd((.2,h))
				self.add_text_input(k,(.3,h),(.3,h),self.sc.text_col1,
					text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
					on_text = self.modif_val,default_text = v)
				self.add_padd((.2,h))
		self.obj_deduction_surf = stack(self,size_hint = (1,h),
			spacing = dp(5),bg_color = self.sc.aff_col1,padding = dp(5),
			radius = dp(5))
		self.add_surf(self.obj_deduction_surf)
		self.Up_obj_surf()

		self.last_surf = stack(self,size_hint = (1,h*2),
			bg_color = self.sc.aff_col1,
			padding = dp(5),spacing = dp(5))
		self.add_surf(self.last_surf)
		self.Up_last_surf()

	@Cache_error
	def Up_last_surf(self):
		self.last_surf.clear_widgets()
		prime = self.modif_dic.get('Prime')
		Deduc = (self.modif_dic.get('Déduction'))
		aug = self.info_dic1.get('augmentation')
		salaire = self.info_dic1.get('salaire minimum')
		if not salaire:
			salaire = float()
		salaire = float(salaire)
		if not prime:
			prime = float()
		prime = float(prime)
		if not Deduc:
			Deduc = float()
		Deduc = float(Deduc)

		aug_mont = float()
		if aug > 100:
			aug_mont = salaire * aug/100
		else:
			aug_mont = float(aug)
		salaire += (aug_mont + prime - Deduc)
		self.THIS_SAL = salaire
		self.last_surf.add_padd((.2,.5))
		self.last_surf.add_text_input('Montant Total :',(.3,.5),(.3,.5),
			self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,default_text = self.format_val(salaire),
			readonly = True,font_size = "20sp",text_font_size = '20sp')
		self.last_surf.add_padd((.2,.5))
		if self.New:
			self.last_surf.add_padd((.066,.5))
			self.last_surf.add_button("Générer",size_hint = (.4,.5),
				text_color = self.sc.text_col3,bg_color = self.sc.aff_col2,
				on_press = self.Generer)

			self.last_surf.add_padd((.066,.5))
			self.last_surf.add_button("Générer et imprimer",size_hint = (.4,.5),
				text_color = self.sc.text_col3,bg_color = self.sc.orange,
				on_press = self.Generer_imp)
		else:
			self.last_surf.add_padd((.066,.5))
			self.last_surf.add_button("Modifier",size_hint = (.4,.5),
				text_color = self.sc.text_col3,bg_color = self.sc.aff_col2,
				on_press = self.modifier)

			self.last_surf.add_padd((.066,.5))
			self.last_surf.add_button("imprimer",size_hint = (.4,.5),
				text_color = self.sc.text_col3,bg_color = self.sc.orange,
				on_press = self.imprimer)

	@Cache_error
	def Up_obj_surf(self):
		self.obj_deduction_surf.clear_widgets()
		self.obj_deduction_surf.add_text('Objet de déduction',
			size_hint = (.2,1),text_color = self.sc.text_col1)
		self.obj_deduction_surf.add_surf(liste_set(self,
			self.modif_dic.get('Objet de déduction'),self.deduction_liste,
			size_hint = (.3,1),mult = 1,mother_fonc = self.modif_obj))
		if self.modif_dic.get('Objet de déduction'):
			self.obj_deduction_surf.add_input("détails",
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				default_text = self.modif_dic.get("détails"),
				size_hint = (.5,1),placeholder = "Détails",
				on_text = self.modif_det,readonly = False)

# Gestion des actions des méthodes
	@Cache_error
	def Generer(self,wid):
		self.fiche_info = self.sc.DB.Get_fiche_format()
		self.fiche_info.update(self.info_dic1)
		self.fiche_info['prime'] = self.modif_dic.get('Prime')
		self.fiche_info['déduction'] = self.modif_dic.get('Déduction')
		self.fiche_info['objet de déduction'] = self.modif_dic.get("Objet de déduction")
		self.fiche_info['détails du déduction'] = self.modif_dic.get('détails')
		self.fiche_info["montant total"] = self.THIS_SAL

		ident = self.mother.perso_ident
		self.excecute(self.sc.DB.Save_fiche_paie,ident,self.fiche_info)
		#self.sc.DB.Save_fiche_paie(ident,self.fiche_info)
		self.sc.add_refused_error(f"Fiche de paie enrégistrée pour {self.info_dic1.get('nom')}")
		self.clear_widgets()
		self.mother.add_liste_surf()

	def Generer_imp(self,wid):
		self.Generer(wid)
		self.imprimer(wid)

	@Cache_error
	def modifier(self,wid):
		self.fiche_info['prime'] = self.modif_dic.get('Prime')
		self.fiche_info['déduction'] = self.modif_dic.get('Déduction')
		self.fiche_info['objet de déduction'] = self.modif_dic.get("Objet de déduction")
		self.fiche_info['détails du déduction'] = self.modif_dic.get('détails')
		self.fiche_info["montant total"] = self.THIS_SAL

		ident = self.mother.perso_ident
		self.excecute(self.sc.DB.Save_fiche_paie,ident,self.fiche_info)
		#self.sc.DB.Save_fiche_paie(ident,self.fiche_info)
		self.sc.add_refused_error(f"Fiche de paie modifiée pour {self.info_dic1.get('nom')}")
		self.clear_widgets()
		self.mother.add_liste_surf()

	@Cache_error
	def imprimer(self,wid):
		self.sc.impress_fich_paie(self.fiche_info)

	def modif_val(self,wid,val):
		wid.text = self.regul_input(wid.text)
		if wid.text:
			self.modif_dic[wid.info] = float(wid.text)
		else:
			self.modif_dic[wid.info] = float()
		self.Up_last_surf()

	def modif_det(self,wid,val):
		self.modif_dic['détails'] = val
		
	def modif_obj(self,info):
		self.modif_dic["Objet de déduction"] = info
		self.Up_obj_surf()

class Missions(Salaires):
	@Cache_error
	def size_pos(self):
		w,h = self.liste_size = .4,1
		self.details_size = 1-w,h

		self.liste_surf = stack(self,size_hint = self.liste_size,
			spacing = dp(5),padding = dp(10))
		self.details_surf = mission_show(self,dict(),size_hint = self.details_size,
			spacing = dp(5),padding = dp(10))

		self.add_surf(self.liste_surf)
		self.add_text('',bg_color = self.sc.sep,size_hint = (None,1),
			width = dp(1))
		self.add_surf(self.details_surf)

	@Cache_error
	def Foreign_surf(self):
		self.status = str()
		self.niveau = str()
		self.type_mi = str()
		self.type_liste = ['Ordinaire',"Extraordinaire","Hebdomadaire",
			"Mensuel","Exceptionnel"]
		self.status_list = ["En cours","Terminée"]
		self.niveau_liste = ['Urgent',"Moins urgent","Obligatoire",
			"Optionel"]
		self.add_liste_surf()
		self.add_details_surf()

	@Cache_error
	def add_liste_surf(self):
		h = .045
		self.tab_surf = Table(self,bg_color = self.sc.aff_col3,
			padding = dp(10),radius = dp(10),exec_fonc = self.show_fiche,
			exec_key = 'N°',size_hint = (1,.67))
		self.liste_surf.clear_widgets()
		self.liste_surf.add_text('Choix du personnel',text_color = self.sc.text_col1,
			size_hint = (.3,.035))
		input_search_new(self.liste_surf,self.perso_ident,
			self.sc.get_devers_perso(),self.set_perso_ident,
			size_hint = (.7,.035))

		if self.perso_ident:
			self.liste_surf.add_text("Liste des missions",
				size_hint = (.9,h),underline = True,
				text_color = self.sc.text_col1,
				halign = 'center')
			self.liste_surf.add_icon_but(icon = 'plus',size_hint = (.1,h),
				on_press = self.New_fiche,text_color = self.sc.green)

			self.liste_surf.add_surf(Periode_set(self,size_hint = (1,h),
				exc_fonc = self.add_tab_surf))
			b = box(self,size_hint = (1,h),orientation = 'horizontal',
				spacing = dp(10))
			b.add_text('Status :',size_hint = (.15,1),text_color = self.sc.text_col1)
			b.add_surf(liste_set(self,self.status,self.status_list,
				mother_fonc = self.set_status,mult = 1,size_hint = (.85,1)))
			
			self.liste_surf.add_surf(b)

			b = box(self,size_hint = (1,h),orientation = 'horizontal',
				spacing = dp(10))
			b.add_text('Niveau :',size_hint = (.15,1),text_color = self.sc.text_col1)
			b.add_surf(liste_set(self,self.niveau,self.niveau_liste,
				mother_fonc = self.set_niveau,mult = 1,size_hint = (.85,1)))
			
			self.liste_surf.add_surf(b)

			b = box(self,size_hint = (1,h),orientation = 'horizontal',
				spacing = dp(10))
			b.add_text('Type :',size_hint = (.15,1),text_color = self.sc.text_col1)
			b.add_surf(liste_set(self,self.type_mi,self.type_liste,
				mother_fonc = self.set_type,mult = 1,size_hint = (.85,1)))
			
			self.liste_surf.add_surf(b)

			self.liste_surf.add_surf(self.tab_surf)
			self.add_tab_surf()

	@Cache_error
	def add_tab_surf(self):
		entete = "date d'émission","type de mission","status"
		wid_l = .3,.35,.35
		liste = self.Trie_fich()
		self.tab_surf.Creat_Table(wid_l,entete,liste,ent_size = (1,.07))

	def Trie_fich(self):
		dic = self.sc.DB.Get_missions_of(self.perso_ident)
		date_liste = self.get_date_list(self.day1,self.day2)
		liste = [j for i,j in dic.items() if j.get("date d'émission") in date_liste]
		if self.status:
			liste = [j for j in liste if self.status.lower() ==  j.get('status').lower()]
		if self.niveau:
			liste = [j for j in liste if self.niveau.lower() ==  j.get('niveau').lower()]
		if self.type_mi:
			liste = [j for j in liste if self.type_mi.lower() ==  j.get('type de mission').lower()]
		return liste

# Gestion des actions
	def set_niveau(self,info):
		self.niveau = info
		self.add_tab_surf()

	def set_type(self,info):
		self.type_mi = info
		self.add_tab_surf()

	def show_fiche(self,wid):
		self.new_fic = False
		self.fiche_ident = wid.info
		fich_dic = self.sc.DB.Get_this_missions_info(self.perso_ident,wid.info)
		self.details_surf.fiche_info = fich_dic
		self.details_surf.New = False
		self.details_surf.add_all()

class mission_show(fiche_show):
	def init(self):
		self.spacing = dp(15)
		self.type_liste = self.mother.type_liste
		self.niveau_liste = self.mother.niveau_liste
		#self.mother.status_list
		if self.New:
			self.status_list = ['En attente']
			self.modif_dic = {
				"type de mission":str(),
				"niveau":str(),
				"status":"En attente"
			}
		elif not self.New:
			self.status_list = [self.fiche_info.get("status")]
			self.modif_dic = {
				"type de mission":self.fiche_info.get('type de mission'),
				"niveau":self.fiche_info.get('niveau'),
				"status":self.fiche_info.get('status')
			}
		if type(self.fiche_info.get('ordre de missions')) == dict:
			self.th_ordre = {i:j for i,j in self.fiche_info.get('ordre de missions',dict()).items()}
			if self.th_ordre:
				st = str()
				for k,v in self.th_ordre.items():
					if v != "En cours":
						pass
					else:
						st += f"{k}\n"
				self.th_ordre = st
			else:
				self.th_ordre = str()
		else:
			self.th_ordre = str()

		self.th_marg = self.fiche_info.get('marge de retard',float())

	@Cache_error
	def Foreign_surf(self):
		h = .047
		self.clear_widgets()
		self.init()
		if self.New:
			txt = 'Nouvelle ordre de mission'
		else:
			txt = "Détails de l'ordre de mission"
		self.add_text(txt,halign = "center",text_color = self.sc.text_col1,
			underline = True,size_hint = (1,.035))

		date = self.fiche_info.get("date d'émission",self.sc.get_today())
		self.add_text_input("date d'émission :",(.18,h),(.2,h),self.sc.text_col1,
			text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
			readonly = True,default_text = date)

		dic = {
			"type de mission :":[self.modif_dic.get('type de mission'),
				self.type_liste,self.set_type],
			"niveau d'exécution :":[self.modif_dic.get('niveau'),
				self.niveau_liste,self.set_niveau],
			"status :":[self.modif_dic.get('status'),
				self.status_list,self.set_status]
		}
		for k,tup in dic.items():
			txt,lis,fonc = tup
			self.add_text(k,size_hint = (.15,.05),
				text_color = self.sc.text_col1)
			self.add_surf(liste_set(self,txt,lis,mother_fonc = fonc,
				size_hint = (.35,h),mult = 1))
		
		
		this_dic = self.fiche_info.get("temps d'accomplissement",dict())
		self.add_surf(Periode_set(self,size_hint = (.6,h),
			info = "Durée d'exécution :",info_w = .2,date_dict = this_dic
			))
		self.add_text_input('Marge de Retard',(.2,h),(.1,h),self.sc.text_col1,
			text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
			on_text = self.Set_marge,default_text = str(self.th_marg))
		self.add_text('Jours',size_hint = (.1,h),text_color = self.sc.text_col1)

		self.add_text('Le contenue',size_hint = (.85,h),
			text_color = self.sc.text_col1,halign = "center",
			font_size = "20sp",underline = True,)
		
		self.Up_last_surf()

		

		self.add_input("ordres",size_hint = (1,.68),text_color = self.sc.text_col1,
			placeholder = 'Les ordres ici séparer par la touche entrer',
			bg_color = self.sc.aff_col3,multiline = True,on_text = self.set_ordre,
			default_text = self.th_ordre)
		

	def Up_last_surf(self):
		h = .045
		if self.New:
			self.add_icon_but(icon = 'printer',text_color = self.sc.black,
				on_press = self.imprimer,size_hint = (.05,h))
			self.add_icon_but(icon = 'content-save',text_color = self.sc.orange,
				on_press = self.Generer,size_hint = (.05,h))
		else:
			status = self.fiche_info.get('status')
			if status != 'Terminée':
				self.add_icon_but(icon = 'pencil',text_color = self.sc.green,
					on_press = self.modifier,size_hint = (.05,h))
				self.add_icon_but(icon = 'printer',text_color = self.sc.black,
					on_press = self.imprimer,size_hint = (.05,h))
				self.add_icon_but(icon = 'delete',text_color = self.sc.red,
					on_press = self.supprimer,size_hint = (.05,h))

			else:
				self.add_icon_but(icon = 'printer',text_color = self.sc.black,
					on_press = self.imprimer,size_hint = (.05,h))
				self.add_icon_but(icon = 'delete',text_color = self.sc.red,
					on_press = self.supprimer,size_hint = (.05,h))

# Gestion des actions des méthodes
	def set_ordre(self,wid,val):
		self.th_ordre = val

	def set_type(self,info):
		self.modif_dic['type de mission'] = info

	def set_status(self,info):
		pass

	def set_niveau(self,info):
		self.modif_dic['niveau'] = info

	def Set_marge(self,wid,val):
		wid.text = self.regul_input(wid.text)
		self.th_marg = wid.text

	@Cache_error
	def Generer(self,wid):
		if self.th_ordre and self.check(self.modif_dic):
			ident = self.mother.perso_ident
			self.fiche_info = self.sc.DB.Get_missions_format()
			self.fiche_info.update(self.modif_dic)
			self.fiche_info['personnel'] = ident
			self.fiche_info['marge de retard'] = self.th_marg
			self.fiche_info["temps d'accomplissement"] = {"day1":self.day1,"day2":self.day2}
			ordre = {i:"En cours" for i in self.th_ordre.split("\n")}
			self.fiche_info['ordre de missions'] = ordre

			self.sc.DB.Save_missions(self.fiche_info)
			self.sc.add_refused_error(f"Ordre de mission enrégistrée pour {ident}")
			self.clear_widgets()
			self.mother.add_liste_surf()
		else:
			self.sc.add_refused_error('Information incomplète')

	@Cache_error
	def supprimer(self,wid):
		ident = self.mother.perso_ident
		self.sc.DB.Del_missions(self.fiche_info)
		self.sc.add_refused_error(f"Ordre de mission supprimée pour {ident}")
		self.clear_widgets()
		self.mother.add_liste_surf()

	@Cache_error
	def modifier(self,wid):
		ident = self.mother.perso_ident
		self.fiche_info.update(self.modif_dic)
		self.fiche_info['personnel'] = ident
		self.fiche_info['marge de retard'] = self.th_marg
		self.fiche_info["temps d'accomplissement"] = {"day1":self.day1,"day2":self.day2}
		ordre = self.fiche_info.get("ordre de missions",dict())
		ordre = {i:j for i,j in ordre.items() if j != "En cours"}
		ordre.update({i:"En cours" for i in self.th_ordre.split("\n")})
		self.fiche_info['ordre de missions'] = ordre

		self.sc.DB.Save_missions(self.fiche_info)
		self.sc.add_refused_error(f"Ordre de mission modifiée pour {ident}")
		self.clear_widgets()
		self.mother.add_liste_surf()

	def imprimer(self,wid):
		pass
		
class H_missions(Missions):
	@Cache_error
	def add_liste_surf(self):
		h = .035
		self.tab_surf = Table(self,bg_color = self.sc.aff_col3,
			padding = dp(10),radius = dp(10),exec_fonc = self.show_fiche,
			exec_key = 'N°',size_hint =(1,.72))
		self.liste_surf.clear_widgets()
		self.liste_surf.add_text('Choix du personnel',text_color = self.sc.text_col1,
			size_hint = (.3,.035))
		input_search_new(self.liste_surf,self.perso_ident,
			self.sc.get_devers_perso(),self.set_perso_ident,
			size_hint = (.7,.035))
		if self.perso_ident:
			self.liste_surf.add_text("Liste des missions",
				size_hint = (1,h),underline = True,
				text_color = self.sc.text_col1,
				halign = 'center')
			self.liste_surf.add_surf(Periode_set(self,size_hint = (1,h),
				exc_fonc = self.add_tab_surf))
			b = box(self,size_hint = (1,h),orientation = 'horizontal',
				spacing = dp(10))
			b.add_text('Status :',size_hint = (.15,1),text_color = self.sc.text_col1)
			b.add_surf(liste_set(self,self.status,self.status_list,
				mother_fonc = self.set_status,mult = 1,size_hint = (.85,1)))
			
			self.liste_surf.add_surf(b)

			b = box(self,size_hint = (1,h),orientation = 'horizontal',
				spacing = dp(10))
			b.add_text('Niveau :',size_hint = (.15,1),text_color = self.sc.text_col1)
			b.add_surf(liste_set(self,self.niveau,self.niveau_liste,
				mother_fonc = self.set_niveau,mult = 1,size_hint = (.85,1)))
			
			self.liste_surf.add_surf(b)

			b = box(self,size_hint = (1,h),orientation = 'horizontal',
				spacing = dp(10))
			b.add_text('Type :',size_hint = (.15,1),text_color = self.sc.text_col1)
			b.add_surf(liste_set(self,self.type_mi,self.type_liste,
				mother_fonc = self.set_type,mult = 1,size_hint = (.85,1)))
			
			self.liste_surf.add_surf(b)

			self.liste_surf.add_surf(self.tab_surf)
			self.add_tab_surf()

	@Cache_error
	def size_pos(self):
		w,h = self.liste_size = .4,1
		self.details_size = 1-w,h

		self.liste_surf = stack(self,size_hint = self.liste_size,
			spacing = dp(5),padding = dp(10))
		self.details_surf = this_mission_show(self,dict(),size_hint = self.details_size,
			spacing = dp(5),padding = dp(10))

		self.add_surf(self.liste_surf)
		self.add_text("",size_hint = (None,1),bg_color = self.sc.sep,
			width = dp(1))
		self.add_surf(self.details_surf)

	def add_tab_surf(self):
		entete = "date d'émission","type de mission","status"
		wid_l = .3,.35,.35
		liste = self.Trie_fich()
		self.tab_surf.Creat_Table(wid_l,entete,liste,ent_size = (1,.07))

class this_mission_show(mission_show):
	@Cache_error
	def init(self):
		self.type_liste = self.mother.type_liste
		self.niveau_liste = self.mother.niveau_liste
		
		self.status_list = [self.fiche_info.get("status")]
		self.modif_dic = {
			"type de mission":self.fiche_info.get('type de mission'),
			"niveau":self.fiche_info.get('niveau'),
			"status":self.fiche_info.get('status')
		}
		self.th_ordre = self.fiche_info.get('ordre de missions')

		self.th_marg = self.fiche_info.get('marge de retard',float())

	@Cache_error
	def Foreign_surf(self):
		h = .05
		self.clear_widgets()
		self.init()
		txt = "Détails de l'ordre de mission"
		self.add_text(txt,halign = "center",text_color = self.sc.text_col1,
			underline = True,size_hint = (1,h))

		date = self.fiche_info.get("date d'émission",self.sc.get_today())
		self.add_text_input("date d'émission :",(.18,h),(.2,h),self.sc.text_col1,
			text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
			readonly = True,default_text = date)

		dic = {
			"type de mission :":[self.modif_dic.get('type de mission'),
				self.type_liste,self.set_type],
			"niveau d'exécution :":[self.modif_dic.get('niveau'),
				self.niveau_liste,self.set_niveau],
			"status :":[self.modif_dic.get('status'),
				self.status_list,self.set_status]
		}
		for k,tup in dic.items():
			txt,lis,fonc = tup
			self.add_text(k,size_hint = (.14,.05),
				text_color = self.sc.text_col1)
			self.add_surf(liste_set(self,txt,lis,mother_fonc = fonc,
				size_hint = (.35,h),mult = 1,readonly = True))
		
		this_dic = self.fiche_info.get("temps d'accomplissement",dict())
		self.add_surf(Periode_set(self,size_hint = (.6,h),
			info = "Durée d'exécution :",info_w = .2,date_dict = this_dic
			,readonly = True))
		self.add_text_input('Marge de Retard',(.2,h),(.1,h),self.sc.text_col1,
			text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
			on_text = self.Set_marge,default_text = str(self.th_marg),
			readonly = True)
		self.add_text('Jours',size_hint = (.1,h),text_color = self.sc.text_col1)

		self.add_text('Le contenue',size_hint = (.5,h),
			text_color = self.sc.text_col1,halign = "center",
			font_size = "20sp",underline = True,)
		self.Up_last_surf()
		
		self.ordre_surf = Table(self,size_hint = (1,.724),
			padding = dp(5),radius = dp(10),bg_color = self.sc.aff_col3,
			exec_key = 'ordre',exec_fonc = self.change_status)
		self.add_ordre_surf()
		self.add_surf(self.ordre_surf)

	@Cache_error
	def add_ordre_surf(self):
		wid_l = .7,.3
		entete = ['ordre','status']
		liste = [{'ordre':k,"status":v} for k,v in self.th_ordre.items() if k]
		self.ordre_surf.Creat_Table(wid_l,entete,liste,ent_size = (1,.07))

	@Cache_error
	def Up_last_surf(self):
		h = .05
		date = self.fiche_info.get("date d'accomplissement")
		if date:
			self.add_text(f"Date d'accomplissement: {date}",
				text_color = self.sc.green,
				halign = "right",size_hint = (.35,h))
			
		else:
			self.add_text(f"En cours d'exécution",
				text_color = self.sc.green,
				halign = "right",size_hint = (.35,h))

		self.add_icon_but(icon = 'printer',size_hint = (.05,h),
			text_color = self.sc.black,	on_press = self.imprimer,)


# Gestion des actions de méthode
	def change_status(self,wid):
		...