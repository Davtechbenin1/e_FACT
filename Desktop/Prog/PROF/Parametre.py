#Coding:utf-8
"""
	Gestion de la surface des paramètres
"""
from lib.davbuild import *
from General_surf import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from ..TRES.Trs_surf import Tresorerie
from ..IMPR.Impression import Factures_normal
from .doc_sys import doc_sys
from kivy.core.window import Window

class Par_General(box):
	@Cache_error
	def initialisation(self):
		#self.orientation = "horizontal"
		self.spacing = dp(10)
		self.modifier = False
		self.try_modif = False
		self.set_new_client = False
		self.ent_info = self.sc.DB.get_entreprise()
		
		self.size_pos()

	def size_pos(self):
		w,h = self.infos_size = .4,1
		self.aff_size = 1-w,h

		self.infos_surf = stack(self,size_hint = (1,1),
			bg_color = self.sc.aff_col1,padding = dp(10),
			radius = dp(10),
			spacing = dp(5))

		self.add_surf(self.infos_surf)

	def Foreign_surf(self):
		self.add_infos_surf()

	@Cache_error
	def add_infos_surf(self):
		h = .035
		H = .4
		self.infos_surf.clear_widgets()
		self.img_surf = float_l(self,size_hint = (.3,.4))
		self.img_surf.add_image(self.ent_info.get('logo',"media/logo.png"))
		self.th_image_srf = self.img_surf.th_image_srf
		self.infos_surf.th_image_srf = self.img_surf.th_image_srf
		self.img_surf.add_button('',bg_color = None,
			on_press = self.get_img_from,)
		self.infos_surf.add_surf(self.img_surf)

		self.infos_set_surf = stack(self,size_hint = (.3,H),
			padding = [dp(5),dp(20),dp(5),dp(5)],spacing = dp(10))

		dic = {
			"sigle":self.ent_info.get('sigle',str()),
			"dénomination":self.ent_info.get('dénomination',str()),
			"forme juridique":self.ent_info.get('forme juridique',str()),
			"IFU":self.ent_info.get('IFU',str()),
			"RCCM":self.ent_info.get('RCCM',str()),
			"F. principal":self.ent_info.get('F. principal',str())
		}
		for k,v in dic.items():
			hh = .1
			self.infos_set_surf.add_text_input(k+' :',(.3,hh*1.3),(.6,hh*1.3),
				self.sc.text_col1,bg_color = self.sc.aff_col3,
				text_color = self.sc.text_col1,on_text = self.set_infos,
				default_text = str(v),inp_info = k,)
		self.infos_surf.add_surf(self.infos_set_surf)
		inf = stack(self,size_hint = (.4,H))
		self.infos_surf.add_surf(inf)
		inf.add_text('Activitées secondaires :',size_hint =(.3,.1),
			)

		Get_border_input_surf(inf,"activitées secondaires",
			(.6,1),text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,on_text = self.set_infos,
			multiline = True,
			default_text = self.ent_info.get('activitées secondaires',str()),
			placeholder = "Les autres activitées secondaires séparer par des virgules")
		

		th_b = box(self,size_hint = (1,.45),
			orientation = "horizontal",spacing = dp(20),
			padding = dp(10))
		self.infos_surf.add_surf(th_b)
		
		dic = {
			"téléphone":self.ent_info.get("téléphone",str()),
			"whatsapp":self.ent_info.get("whatsapp",str()),
			"email":self.ent_info.get("email",str()),
		}
		self.set_part_infos(th_b,dic,self.set_infos,"Contacts")

		dic = {
			"pays":self.ent_info.get("pays",str()),
			"ville":self.ent_info.get("ville",str()),
			"quartier":self.ent_info.get("quartier",str()),
			"maison":self.ent_info.get("maison",str()),
		}
		self.set_part_infos(th_b,dic,self.set_infos,"Addresse")
		
		dic = {
			"responsable":self.ent_info.get("responsable",str()),
			"numéro perso":self.ent_info.get("numéro perso",str()),
			"addresse":self.ent_info.get("addresse",str()),
		}
		self.set_part_infos(th_b,dic,self.set_infos,"Infos Directeurs Général")
		
		self.infos_surf.add_padd((.35,h))
		if "écritures" in self.sc.DB.Get_access_of('Paramètre général'):
			self.infos_surf.add_button("Enrégistrer les informations",
			bg_color = self.sc.orange,text_color = self.sc.aff_col1,
			on_press = self.save_ent,size_hint = (.3,h*1.2))

	def set_part_infos(self,mother,dic,fonc,title):
		b = stack(self,radius = dp(10),
			spacing = dp(10),bg_color = self.sc.aff_col1)
		b.add_text(title,size_hint = (1,.1),
			text_color = self.sc.aff_col1,
			bold = True,italic = True,
			radius = [dp(10),dp(10),0,0],
			bg_color = self.sc.green,
			padding_left = dp(10))
		b = Get_border_surf(mother,b,self.sc.green)
		for txt,val in dic.items():
			b.add_text(txt,size_hint = (1,None),height = dp(20),
				padding_left = dp(10))
			b.add_padd((.05,.1))
			Get_border_input_surf(b,txt,(.9,.1),
				border_col = self.sc.green,
				bg_color = self.sc.aff_col1,
				on_text = fonc, default_text = str(val),
				)

	@Cache_error
	def add_fichier_surf(self):
		self.fichier_surf.clear_widgets()
		self.fichier_surf.add_text_input('fichier RCCM :',(.27,.5),(.5,.5),
			self.sc.text_col1,bg_color = self.sc.aff_col3,
			text_color = self.sc.text_col1,readonly = True,
			default_text = self.ent_info.get('fichier RCCM',str()),
			shorten = True,strip = False)
		self.fichier_surf.add_button('Parcourir',text_color = self.sc.text_col3,
			bg_color = self.sc.aff_col2,on_press = self.set_RCCM,
			size_hint = (.2,.5))

		self.fichier_surf.add_text_input('fichier déclaration :',(.27,.5),(.5,.5),
			self.sc.text_col1,bg_color = self.sc.aff_col3,
			text_color = self.sc.text_col1,readonly = True,
			default_text = self.ent_info.get('fichier déclaration',str()),
			shorten = True,strip = False)
		self.fichier_surf.add_button('Parcourir',text_color = self.sc.text_col3,
			bg_color = self.sc.aff_col2,on_press = self.set_decla,
			size_hint = (.2,.5))
		
# Gestion des actions des bouttons
	def save_ent(self,wid):
		if self.set_new_client:
			self.ent_info['End verification time'] = self.sc._get_day_to(30)
		#self.excecute(self.sc.DB.save_entreprise,self.ent_info)
		self.sc.DB.save_entreprise(self.ent_info)
		self.sc.add_refused_error("Les enformations concernant l'entreprise mise à jour")
		self.add_infos_surf()

	def upload_fic(self,selection):
		self.ent_info["logo"] = selection
		self.img_surf.clear_widgets()
		self.img_surf.add_image(selection)
		self.img_surf.add_button('',bg_color = None,
			on_press = self.get_img_from,)

	def set_RCCM(self,wid):
		root = Tk()
		root.withdraw()
		fichier = askopenfilename(
			title = "Choix du fichier Régistre de commerce",
			filetypes = [("Fichier PDF","*.pdf")]
		)
		self.ent_info["fichier RCCM"] = fichier
		self.add_fichier_surf()

	def set_decla(self,wid):
		root = Tk()
		root.withdraw()
		fichier = askopenfilename(
			title = "Choix du fichier de déclaration d'établissement",
			filetypes = [("Fichier PDF","*.pdf")]
		)
		self.ent_info["fichier déclaration"] = fichier
		self.add_fichier_surf()

	def set_infos(self,wid,val):
		self.ent_info[wid.info] = val

class autre_param(box):
	@Cache_error
	def initialisation(self):
		self.orientation = 'horizontal'
		self.spacing = dp(10)
		self.p_liste = ["Lexend","Segoe","Sfpro","Roboto","Inter"]
		self.size_pos()
		self.param_dic = dict()
		self.verified_dic = {
			"Sigle":self.sc.DB.Get_ent_part('sigle'),
			"Durée":365,
			"Message":"J'aimerai obtenir la licence de ZoeCorp pour une durée de 365 Jours. Pour bénéficier de 30 Jours suplémentaire.",
		}
		self.penalite_info = self.sc.DB.Get_ent_part("Paramètre Pénalité")
		if not self.penalite_info:
			self.penalite_info = dict()
		self.add_all()

	def size_pos(self):
		self.ergo_part = stack(self,spacing = dp(10),
			bg_color = self.sc.aff_col1,
			padding_left = dp(10),radius = dp(10))

		self.verified_surf = stack(self,spacing = dp(10),
			padding = dp(10),bg_color = self.sc.aff_col1,
			radius =dp(10))

		self.add_surf(self.verified_surf)
		self.add_surf(self.ergo_part)

	@Cache_error
	def Foreign_surf(self):
		self.add_ergo_part()
		self.add_verified_surf()

	def add_ergo_part(self):
		h = .05
		self.ergo_part.clear_widgets()
		self.add_penalite_setting()

	@Cache_error
	def add_penalite_setting(self):
		h = .05
		#self.ergo_part.add_padd((1,h*2))
		self.ergo_part.add_text("Paramètre de gestion des pénalités",
			size_hint = (1,h),text_color = self.sc.text_col1,
			underline = True,italic = True, bold = True)
		dic = {
			"Pourcentage des pénalités :":"Pourcentage",
			"Pourcentage limite :":"limite",
			"Nombre de jours de grâce":"Jours décompte"
		}
		for txt,info in dic.items():
			self.ergo_part.add_text_input(txt,(.2,h),
				(.28,h),self.sc.text_col1,bg_color = self.sc.aff_col3,
				inp_info = info,text_color = self.sc.text_col1,
				default_text = self.format_val(self.penalite_info.get(info,str())),
				on_text = self.modif_penal_info)
		
		self.ergo_part.add_button_custom("Enrégistrer",self.Save_penale,
			size_hint = (.3,h),padd = (.15,h),
			text_color = self.sc.aff_col1)

	@Cache_error
	def add_verified_surf(self):
		h = .05
		self.verified_surf.clear_widgets()
		if not self.sc.DB.Get_ent_part("Verified"):
			self.verified_surf.add_text('Demande de la licence pour une utilisation complète',
				size_hint = (1,h),underline = True,
				bold = True, italic = True)
			th_dic = {
				"Sigle":self.verified_dic["Sigle"],
				"Durée":self.verified_dic["Durée"],
			}
			for k,v in th_dic.items():
				self.verified_surf.add_padd((.1,h))
				self.verified_surf.add_text_input(k,(.2,h),(.6,h),
					self.sc.text_col1, text_color = self.sc.text_col1, 
					bg_color = self.sc.aff_col3, default_text = str(v),
					on_text = self.Set_verifie_info)
				self.verified_surf.add_padd((.1,h))
			self.verified_surf.add_padd((.1,h))
			self.verified_surf.add_text_input("Message",(.2,h),(.6,h*5),
				self.sc.text_col1,text_color = self.sc.text_col1,
				default_text = str(self.verified_dic['Message']),
				multiline = True,on_text = self.Set_verifie_info,
				bg_color = self.sc.aff_col3)
			self.verified_surf.add_padd((.1,h))
			self.verified_surf.add_button_custom("Soumettre votre demande",
				self.send_verified_info,size_hint = (.3,h),padd = (.35,h),
				text_color = self.sc.aff_col1)

			self.verified_surf.add_padd((1,h))
			self.verified_surf.add_text('Vous avez un code?',size_hint = (1,h),
				text_color = self.sc.green,halign = 'center',underline = True)
			self.verified_surf.add_padd((.1,h))
			self.verified_surf.add_text_input('Votre code',(.2,h),(.6,h),
				self.sc.text_col1,text_color = self.sc.text_col1,
				on_text = self.set_code_text)
			self.verified_surf.add_button_custom('Valider',self.Valide_code,
				text_color = self.sc.aff_col1,padd = (.35,h),
				size_hint = (.3,h),)
		else:
			date = self.sc.DB.Get_ent_part('Last Verified date')
			curent = self.sc.get_today()
			date_obj = datetime.strptime(date,self.date_format)
			cur_date_obj = datetime.strptime(curent,self.date_format)
			end_date_obj = date_obj + timedelta(days=int(self.sc.DB.Get_ent_part("Durée")))
			end_date = end_date_obj.strftime(self.date_format)
			self.verified_surf.add_text(f"Votre Logiciel est Vérifier et \
Valider ce {date}, et valide jusqu'au {end_date}",halign = "center", 
				text_color = self.sc.text_col1,	font_size = "18sp",)

# Gestion des actions des méthodes
	def set_code_text(self,wid,val):
		self.my_code = wid.text

	@Cache_error
	def Save_penale(self,wid):
		ent = self.sc.DB.get_entreprise()
		ent["Paramètre Pénalité"] = self.penalite_info
		self.sc.DB.save_entreprise(ent)

	def modif_penal_info(self,wid,val):
		wid.text = self.regul_input(wid.text)
		val = wid.text
		if not val:
			val = float()
		self.penalite_info[wid.info] = val

	@Cache_error
	def Valide_code(self,wid):
		th_code = self.sc.DB.Get_ent_part('pending code')
		if self.my_code.upper() == th_code.upper():
			dic = self.sc.DB.get_entreprise()
			dic['Verified'] = True
			dic["Last Verified date"] = self.sc.get_today()
			dic['End verification time'] = self.get_end_time()
			dic['Licence actuelle'] = self.my_code.upper()
			self.sc.DB.save_entreprise(dic)
			self.add_verified_surf()
			self.sc.add_refused_error('Votre entreprise est Vérifier')
		else:
			self.sc.add_refused_error("Le code saisi n'est conforme Veillez contacter ZoeCorp")

	def get_end_time(self):
		end_t = int(self.verified_dic.get('Durée'))
		if end_t == 365:
			end_t += 30
		return self.sc._get_day_to(end_t)

	def Set_verifie_info(self,wid,val):
		if wid.info == 'Durée':
			wid.text = self.regul_input(wid.text)
			if not wid.text:
				wid.text = "0"
			val = int(wid.text)
		self.verified_dic[wid.info] = val

	def send_verified_info(self,wid):
		if not self.check(self.verified_dic):
			self.sc.add_refused_error("Toutes les informations sont obligatoires!")
		else:
			text_form = str()
			dic = self.sc.DB.get_entreprise()
			for k,v in self.verified_dic.items():
				text_form += f"{k}:{v}"
				dic[k] = v
			text_form+=f"date:{self.sc.get_today()}"
			mont_Jour = 150
			mont = self.verified_dic.get('Durée') * mont_Jour
			text_form+=f"Montant:{mont}"

			code = self.sc.DB.Genere_code(text_form)
			dic['pending code'] = code 
			self.sc.DB.save_entreprise(dic)
			send_wht_message("https://wa.me/22944695607",text_form)
			txt = f"Votre demande a été généré. Vous aurez [b]{self.format_val(mont)}F CFA[/b] à déverser. Veillez visiter votre navigateur pour finaliser la demande"
			self.sc.add_refused_error(txt)

	def set_text_size(self,info):
		self.param_dic['text_size'] = info

	def set_them(self,info):
		self.param_dic['thème'] = info

	def set_type(self,info):
		self.param_dic['type_police'] = info

	@Cache_error
	def Save_param(self,wid):
		if self.check(self.param_dic):
			#self.sc.DB.Update_param(self.param_dic)
			self.sc.DB.Param_info = self.sc.DB.Get_param()
			self.sc.set_color_obj()
			self.sc.add_refused_error('Mise à jour des informations réussit')
			self.sc.root.__init__(self.sc)
			self.sc.root.clear_widgets()
			self.sc.root.size_pos()
			self.sc.root.Foreign_surf()

			self.add_all()
		else:
			self.sc.add_refused_error('Toutes les informations doivent être définie')
		
class Normalisation(box):
	@Cache_error
	def initialisation(self):
		self.spacing = dp(10)
		#self.orientation = 'horizontal'
		self.Ent_obj = self.sc.DB.get_entreprise()
		d,m,y = self.sc.get_today().split('-')
		self.th_mois = m
		self.th_year = y
		self.curent_mois = f'{self.th_mois}_{self.th_year}'
		#self.curent_data = self.sc.DB.Get_normalisation(self.curent_mois)

		self.th_val_st = "en attente"
		self.th_val_list = 'en attente', "validée", "erreur"
		self.client = str()
		self.size_pos()

	def size_pos(self):
		self.connexion_part = stack(self,size_hint = (.5,.6),
			spacing = dp(10),padding = dp(10),radius = dp(10),
			bg_color = self.sc.aff_col1,
			pos_hint = (.25,0))
		self.Hist_part = stack(self,size_hint = (.7,1),
			spacing = dp(10),padding = dp(10),radius = dp(10),
			bg_color = self.sc.aff_col1)
		#if "écritures" in self.sc.DB.Get_access_of("Connexion"):
		self.add_text('',size_hint = (1,.12))
		self.add_surf(self.connexion_part)
		self.add_text('',size_hint = (1,.28))

		#self.add_surf(self.Hist_part)


	@Cache_error
	def Foreign_surf(self):
		self.add_connex()
		#self.add_histo_part()

	def add_histo_part(self):
		h = .05
		self.Hist_part.clear_widgets()
		self.Hist_part.add_text("Historique des factures normalisées du",
			text_color = self.sc.text_col1, underline = True,
			size_hint = (.3,h))
		self.Hist_part.add_text_input('Mois :',(.08,h),(.08,h),
			self.sc.text_col1, text_color = self.sc.text_col1,
			default_text = self.th_mois,
			bg_color = self.sc.aff_col3,on_text = self.set_mois)
		self.Hist_part.add_text_input('Année :',(.08,h),(.08,h),
			self.sc.text_col1, text_color = self.sc.text_col1,
			default_text = self.th_year,
			bg_color = self.sc.aff_col3,on_text = self.set_year)
		self.Hist_part.add_button_custom("Lancer le trie",self.Lance_Trie,
			size_hint = (.15,h),text_color = self.sc.aff_col1,
			bg_color = self.sc.green)

		dic = {
			"status de validation emecf":(self.th_val_st,self.th_val_list,
				self.set_th_val_st),
		}
		for k, tup in dic.items():
			txt,lis,fonc = tup
			self.Hist_part.add_text(k,text_color = self.sc.text_col1,
				size_hint = (.25,h),)
			self.Hist_part.add_surf(liste_set(self,txt,lis,mother_fonc = fonc,
				size_hint = (.25,h),mult = 1))

		self.Hist_part.add_text_input('Nom du client :',(.15,h),(.2,h),
			self.sc.text_col1, text_color = self.sc.text_col1,
			default_text = self.client,
			bg_color = self.sc.aff_col3, on_text = self.set_nom_clt)

		self.th_Tab = Table(self,size_hint = (1,.88),
			exec_fonc = self.show_nor_details,
			exec_key = 'N°',bg_color = self.sc.aff_col3)
		self.Hist_part.add_surf(self.th_Tab)
		self.up_Tab()

	@Cache_error
	def up_Tab(self):
		entete = ("nom client","tel client","nombre d'article","montant TTC",
			"date d'émission",'auteur','uid_emecf',"status_emecf")
		wid_l = [.13,.13,.1,.12,.12,.11,.18,.11]
		mois = f"{self.th_mois}_{self.th_year}"
		if mois != self.curent_mois:
			self.curent_data = self.sc.DB.Get_normalisation(mois)
			self.curent_mois = mois
		
		all_info = self.curent_data
		liste = [i for i in map(self.Tri,all_info.values()) if i]
		self.th_Tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.065),
			ligne_h = .08)

	def Tri(self,dic):
		if self.client:
			if client.lower() not in dic.get('nom client').lower():
				return None
		if self.th_val_st:
			if self.th_val_st.lower() != dic.get('status_emecf').lower():
				return None
		return dic

	@Cache_error
	def add_connex(self):
		h = .09
		IFU = self.Ent_obj.get("IFU")
		nom = self.Ent_obj.get('sigle')
		tocken = self.Ent_obj.get("tocken",str())
		self.connexion_part.clear_widgets()
		self.connexion_part.add_text('Paramètre de connexion',underline = True,
			font_size = "20sp",text_color = self.sc.text_col1,halign = 'center',
			size_hint = (1,h))
		dic = {
			"IFU":IFU,"sigle":nom,
		}
		place = {
			"IFU":"IFU de votre entreprise",
			"sigle":"Le nom commerciale de votre entreprise",
			'tocken':"Le tocken obtenu depuis votre compte développeur e-MECEF"
		}
		for k,v in dic.items():
			self.connexion_part.add_text(k+" :",
				size_hint = (.2,h))
			Get_border_input_surf(self.connexion_part,k,
				size_hint = (.8,h),
				border_col = self.sc.aff_col3,
				text_color = self.sc.text_col1,
				default_text = str(v), 
				placeholder = place.get(k),
				on_text = self.write_modif_ent,
				bg_color = self.sc.aff_col3)
		self.connexion_part.add_text("tocken :",
			size_hint = (.2,h), text_color = self.sc.text_col1,
			)
		Get_border_input_surf(self.connexion_part,'tocken',
			placeholder = place.get("tocken"),
			border_col = self.sc.aff_col3,
			size_hint = (.8,.4),
			text_color = self.sc.text_col1,
			multiline = True,
			default_text = self.Ent_obj.get('tocken',str()),
			bg_color = self.sc.aff_col3,
			on_text = self.write_modif_ent)

		txt = "Vérifier la connexion"
		bg_col = self.sc.red
		if self.sc.DB.Get_ent_part('Lien_e-MECEF'):
			txt = "Connexion Vérifier"
			bg_col = self.sc.green

		self.connexion_part.add_button_custom(txt,self.Connect,
			size_hint = (.4,h),padd = (.3,h),
			text_color = self.sc.aff_col1,
			bg_color = bg_col)

# Méthode de gestion des actions
	def set_nom_clt(self, wid,info):
		self.client  = info

	def set_th_val_st(self,info):
		self.th_val_st = info
		self.up_Tab()

	def set_mois(self,wid,info):
		wid.text = self.regul_input(wid.text)
		if len(wid.text) > 2:
			wid.text = wid.text[:2]
		self.th_mois = wid.text

	def set_year(self,wid,info):
		wid.text = self.regul_input(wid.text)
		if len(wid.text) > 4:
			wid.text = wid.text[:4]
		self.th_year = wid.text

	def Lance_Trie(self,wid):
		self.up_Tab()

	@Cache_error
	def Connect(self,wid):
		Window.set_system_cursor('wait')
		tocken = self.Ent_obj.get('tocken')
		if tocken:
			result = self.sc.tester_connexion_emecf(tocken)
			if result['success']:
				self.Ent_obj['Lien_e-MECEF'] = True
				self.sc.add_refused_error('Connexion Réussit')
			else:
				self.Ent_obj['Lien_e-MECEF'] = False
				self.sc.add_refused_error('Connexion Echouer! Veillez verifier les informations de connexion')

			self.excecute(self.sc.DB.save_entreprise(self.Ent_obj))
			self.add_all()
		else:
			self.sc.add_refused_error('Veillez coller votre API Tocken obtenu depuis vote compte e-MECEF !')
		Window.set_system_cursor('arrow')

	def write_modif_ent(self,wid,text):
		if text:
			self.Ent_obj[wid.info] = text
		self.excecute(self.sc.DB.save_entreprise(self.Ent_obj))

	def show_nor_details(self,wid):
		if "écritures" in self.sc.DB.Get_access_of('Normalisation'):
			ident = wid.info
			cmd = self.curent_data.get(ident)
			cmd_surf = valid_surf(self,cmd,bg_color = self.sc.aff_col1)

			self.add_modal_surf(cmd_surf,size_hint = (.3,.45))
		else:
			self.sc.add_refused_error("Impossible de continuer à cause d'une restriction système !! Parlez-en à votre supérieur hiérachique")

class valid_surf(stack):
	def __init__(self,mother,cmd_dic,h = .1,**kwargs):
		stack.__init__(self,mother,**kwargs)
		self.padding = dp(10)
		self.spacing = dp(10)
		self.cmd_dic = cmd_dic
		self.h = h
		if self.cmd_dic['status_emecf'] == "en attente":
			self.add_en_attente()
		if self.cmd_dic['status_emecf'] == 'validée':
			self.add_impression_surf()
		if self.cmd_dic['status_emecf'] == "erreur":
			self.add_erreur_surf()

	@Cache_error
	def add_erreur_surf(self):
		self.clear_widgets()
		self.add_text('Finaliser la normalisation de cette factures',
			text_color = self.sc.text_col1,halign = "center",
			size_hint = (.9,self.h),underline = True,
			font_size = "20sp")
		self.add_icon_but(icon = "close", text_color = self.sc.red,
			on_press = self.mother.close_modal,size_hint = (.05,self.h))
		mont_ht = float()
		taxe = float()
		for art_d in self.cmd_dic.get("articles"):
			mont_ht += art_d.get('montant HT')
			taxe += art_d.get('taxes')
		self.cmd_dic["montant HT"] = mont_ht
		self.cmd_dic['taxes'] = taxe
		dic = {
			"Client":self.cmd_dic.get('nom client'),
			"Montant de la Commande":mont_ht,
			"Taxes appliquer":taxe,
			"Montant TTC":mont_ht + taxe
		}
		for k,v in dic.items():
			self.add_padd((.2,self.h))
			self.add_text_input(k + ' :',(.3,self.h),(.3,self.h),self.sc.text_col1,
				text_color = self.sc.text_col1, bg_color = self.sc.aff_col1,
				readonly = True,default_text = self.format_val(v))
			self.add_padd((.2,self.h))
		self.add_button_custom("Soumettre à la normalisation",self.soumettre,
			size_hint = (.5,self.h),padd = (.25,self.h),text_color = self.sc.aff_col1,
			bg_color = self.sc.orange)

	@Cache_error
	def add_impression_surf(self):
		self.clear_widgets()
		self.add_text("Cette est déjà normalisé. Vous pouvez l'imprimer",
			text_color = self.sc.text_col1,halign = "center",
			size_hint = (.9,self.h),underline = True,
			font_size = "20sp")
		self.add_icon_but(icon = "close", text_color = self.sc.red,
			on_press = self.mother.close_modal,size_hint = (.05,self.h))
		mont_ht = float()
		taxe = float()
		for art_d in self.cmd_dic.get("articles"):
			mont_ht += art_d.get('montant HT')
			taxe += art_d.get('taxes')
		self.cmd_dic["montant HT"] = mont_ht
		self.cmd_dic['taxes'] = taxe
		dic = {
			"Client":self.cmd_dic.get('nom client'),
			"Montant de la Commande":mont_ht,
			"Taxes appliquer":taxe,
			"Montant TTC":mont_ht + taxe
		}
		for k,v in dic.items():
			self.add_padd((.2,self.h))
			self.add_text_input(k + ' :',(.3,self.h),(.3,self.h),self.sc.text_col1,
				text_color = self.sc.text_col1, bg_color = self.sc.aff_col1,
				readonly = True,default_text = self.format_val(v))
			self.add_padd((.2,self.h))
		self.add_button_custom("Imprimer la facture",self.Impression,
			size_hint = (.5,self.h),padd = (.25,self.h),text_color = self.sc.aff_col1,
			bg_color = self.sc.green)

	@Cache_error
	def add_en_attente(self):
		self.clear_widgets()
		self.add_text('Finaliser la normalisation de cette factures',
			text_color = self.sc.text_col1,halign = "center",
			size_hint = (.9,self.h),underline = True,
			font_size = "20sp")
		self.add_icon_but(icon = "close", text_color = self.sc.red,
			on_press = self.mother.close_modal,size_hint = (.05,self.h))
		mont_ht = float()
		taxe = float()
		for art_d in self.cmd_dic.get("articles"):
			mont_ht += art_d.get('montant HT')
			taxe += art_d.get('taxes')
		self.cmd_dic["montant HT"] = mont_ht
		self.cmd_dic['taxes'] = taxe
		dic = {
			"Client":self.cmd_dic.get('nom client'),
			"Montant de la Commande":mont_ht,
			"Taxes appliquer":taxe,
			"Montant TTC":mont_ht + taxe
		}
		for k,v in dic.items():
			self.add_padd((.2,self.h))
			self.add_text_input(k + ' :',(.3,self.h),(.3,self.h),self.sc.text_col1,
				text_color = self.sc.text_col1, bg_color = self.sc.aff_col1,
				readonly = True,default_text = self.format_val(v))
			self.add_padd((.2,self.h))
		self.add_button_custom("Valider la normalisation",self.valider,
			size_hint = (.5,self.h),padd = (.25,self.h),text_color = self.sc.aff_col1,
			bg_color = self.sc.orange)

# Gestion des actions
	@Cache_error
	def soumettre(self,wid):
		self.sc.DB.This_normalis(self.cmd_dic)
		self.mother.close_modal()
		self.mother.add_histo_part()

	@Cache_error
	def valider(self,wid):
		ret = self.sc.Confirmation_normaliser(self.cmd_dic)
		if ret:
			self.cmd_dic["status_emecf"] = 'validée'
			self.cmd_dic["Information_normalisation"] = ret
			date = self.cmd_dic.get("date de la normalisation",self.sc.get_today())
			self.sc.DB._Save_nor(date,self.cmd_dic)
		self.mother.close_modal()
		self.mother.add_histo_part()

	@Cache_error
	def Impression(self,wid):
		self.typ = 'FACTURE'
		Obj = Factures_normal
		Obj.cmd_dic = self.cmd_dic
		Obj(self)
		self.mother.close_modal()




