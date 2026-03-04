#Coding:utf-8
"""
	Gestion de la partie profile
"""
from lib.davbuild import *
from General_surf import *
from ..RH.perso_surf import Define_surf
import datetime

from ..RH.perso_surf3 import Missions,Salaires,fiche_show,mission_show

class Profile(box):
	@Cache_error
	def initialisation(self):
		self.orientation = "horizontal"
		self.modifier = False
		self.try_modif = False

		self.size_pos()

	def size_pos(self):
		self.infos_surf = stack(self,
			size_hint = (1,1),
			bg_color = self.sc.aff_col1,
			padding = dp(10),
			radius = dp(10),
			spacing = dp(5))

		self.add_surf(self.infos_surf)

	@Cache_error
	def add_infos_surf(self):
		h = .035
		#self.aff_surf.add_all()
		self.infos_surf.clear_widgets()
		perso = self.sc.get_profile_perso()
		self.perso_infos = self.sc.DB.Get_this_perso(perso)
		self.infos_surf.add_text('Informations générales',text_color = self.sc.text_col1,
			halign = 'left',size_hint = (1,h),
			underline = True,bold = True,italic = True)
		self.img_surf = float_l(self,size_hint = (.4,.4))
		img = self.perso_infos.get('img')
		if not img:
			img ="media/logo.png"
		self.img_surf.add_image(img)
		self.img_surf.add_button('',bg_color = None,
			on_press = self.get_img_from)
		self.infos_surf.add_surf(self.img_surf)
		self.info_set_surf = stack(self,size_hint = (.6,.4),
			spacing = dp(10))
		self.infos_surf.add_surf(self.info_set_surf)
		self.add_info_set_surf()

		adress_dic = {
			"pays":self.perso_infos.get('pays de résidence'),
			"ville":self.perso_infos.get('ville de résidence'),
			"quartier":self.perso_infos.get("quartier"),
			"maison":self.perso_infos.get('maison')
		}
		inp_infos = {
			"pays":"pays de résidence",
			"ville":"ville de résidence",
			"quartier":"quartier",
			"maison":"maison",
		}

		for k,v in adress_dic.items():
			inf = inp_infos.get(k)
			self.info_set_surf.add_text(k,size_hint = (.15,.1))
			Get_border_input_surf(self.info_set_surf,inf,(.3,.1),
				border_col = self.sc.green,
				bg_color = self.sc.aff_col3,
				on_text = self.set_infos,
				default_text = v,placeholder = inf)

			self.info_set_surf.add_padd((.025,.1))

		self.part1 = stack(self,size_hint = (.4,.5))

		self.part2 = stack(self,size_hint = (.6,.5))
		self.part2.add_text('Informations Non modifiable',
			text_color = self.sc.text_col1,
			halign = "left",size_hint = (1,.1),
			italic = True, bold = True,underline = True)

		self.infos_surf.add_surf(self.part1)
		self.infos_surf.add_surf(self.part2)

		self.part1.add_text('Informations de Connexion',
			halign = "left",size_hint = (1,.1),
			underline = True,
			text_color = self.sc.text_col1,
			italic = True, bold = True)
		self.connex_surf = stack(self,size_hint = (1,.9),
			padding = dp(5),spacing = dp(10))
		self.part1.add_surf(self.connex_surf)
		self.add_connex_surf()
		poste = self.perso_infos.get('poste actuel')
		poste_infos = self.sc.DB.Get_this_poste(poste)
		jour = self.perso_infos.get('durée de contrat','Indéterminé')
		if jour == 'Indéterminé':
			jour = 2000
		date = self.perso_infos.get('date de prise de fonction')
		if not date:
			date = self.sc.get_today()
		d,m,y = [int(i) for i in date.split("-")]
		begin = datetime.date(y,m,d)
		d1,m1,y1 = [int(i) for i in self.sc.get_today().split('-')]
		actuel = datetime.date(y1,m1,d1)
		restant = (actuel-begin).days

		fin_date = begin+datetime.timedelta(days = int(jour))
		fin_date = f"{fin_date.day}-{fin_date.month}-{fin_date.year}"

		l_dic = {
			"catégorie de poste":self.perso_infos.get('type'),
			"niveau hiérachique":poste_infos.get('niveau hiérachique'),
			"fonction principal":poste_infos.get("fonction principal"),
			"poste actuelle":poste,
			"date de prise de fonction":date,
			"durée du contrat actuelle":str(jour)+' Jours',
			"jours écroullé depuis le contrat":f"{restant} Jours",
			"fin de contrat":fin_date,
			"salaire minimum":poste_infos.get('salaire minimal'),
			"augmentation":self.perso_infos.get("augmentation",float())
		}
		for k,v in l_dic.items():
			try:
				float(v)
			except:
				pass
			else:
				v = self.format_val(v)
			self.part2.add_text(k,size_hint = (.2,.1),
				text_color = self.sc.text_col1)
			self.part2.add_text(str(v),size_hint = (.3,.1),
				text_color = self.sc.text_col1,bold = True)

		b = box(self,size_hint = (.5,.05),orientation = 'horizontal',
			spacing = dp(10))

		b.add_button('Voir le contrat',on_press = self.see_contrat,
			info = self.perso_infos.get('contrat de travail'),
			bg_color = self.sc.aff_col3,text_color = self.sc.text_col3)

		b.add_button('Voir votre CV',on_press = self.see_cv,
			info = self.perso_infos.get('cv'),
			bg_color = self.sc.orange,text_color = self.sc.text_col3)

		b.add_button('Save modifications',text_color = self.sc.text_col3,
			bg_color = self.sc.green,on_press = self.Save_info)
		self.infos_surf.add_padd((.25,.04))
		self.infos_surf.add_surf(b)

	@Cache_error
	def add_connex_surf(self):
		self.connex_surf.clear_widgets()
		dic = {
			"username":self.perso_infos.get('username'),
			"password":self.perso_infos.get('mot de pass')
		}
		self.modif_c = {
			"username":self.perso_infos.get("username"),
			"password":str(),
			"password again":str(),
		}
		if self.modifier:
			b1 = stack(self,size_hint = (.6,1),spacing = dp(5))
			b2 = stack(self,size_hint = (.4,1))
			for k,v in self.modif_c.items():
				passw = False
				if k != "username":
					passw = True
				b1.add_text(k,size_hint = (1,.1))
				b1.add_padd((.05,.1))
				Get_border_input_surf(b1,k,(.9,.1),border_col = self.sc.green,
					bg_color = self.sc.aff_col3,on_text = self.modif_conn,
					default_text = v,password = passw)
			b2.add_padd((1,.3))
			b2.add_button('Définire',
				text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,
				on_press = self.Set_con_infos,
				size_hint = (.7,.1))
			self.connex_surf.add_surf(b1)
			self.connex_surf.add_surf(b2)

		elif self.try_modif:
			self.connex_surf.add_text('password actuelle :',
				size_hint = (1,.1))
			self.connex_surf.add_padd((.05,.1))
			Get_border_input_surf(self.connex_surf,"password actuelle :",
				(.9,.1),border_col = self.sc.green,
				bg_color = self.sc.aff_col3,on_text = self.set_last_pass,
				password = True)

			"""
			self.connex_surf.add_text_input(,
				(1,.1),(.9,.1),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				on_text = self.set_last_pass,password = True)
			"""
			self.connex_surf.add_text(self.error_text,text_color = self.sc.red,
				halign = 'center',size_hint = (1,.1),)
		else:
			b1 = stack(self,size_hint = (.6,1),spacing = dp(5))
			b2 = stack(self,size_hint = (.3,1))
			for k,v in dic.items():
				passw = False
				if k != "username":
					passw = True

				b1.add_text(k,
				size_hint = (1,.1))
				b1.add_padd((.05,.1))
				Get_border_input_surf(b1,k,(.9,.1),border_col = self.sc.green,
					bg_color = self.sc.aff_col3,on_text = self.modif_conn,
					default_text = v,password = passw)
				
				"""
				b1.add_text_input("username",(1,.1),(.9,.1),
					self.sc.text_col1,bg_color = self.sc.aff_col3,
					text_color = self.sc.text_col1,on_text = self.modif_conn,
					default_text = v,password = passw)
				"""
			b2.add_padd((1,.22))
			b2.add_button('Modifier',text_color = self.sc.white,
				bg_color = self.sc.green,on_press = self.Set_con_infos,
				size_hint = (1,.1))
			self.connex_surf.add_surf(b1)
			self.connex_surf.add_surf(b2)

	@Cache_error
	def add_info_set_surf(self):
		self.info_set_surf.clear_widgets()
		ident_list = ["nom","prénom","téléphone","whatsapp","email","NIP"]
		dic = {k:self.perso_infos.get(k) for k in ident_list}
		y_nais = float(self.perso_infos.get("date de naissance","29-12-1997").split("-")[-1])
		y_act = float(self.sc.get_today().split('-')[-1])
		age = int(y_act - y_nais)
		#dic['age'] = str(age)
		for k,v in dic.items():
			read = False
			bg_col = self.sc.aff_col3
			try:
				float(v)
			except:
				pass
			else:
				v = self.format_val(v)
			if k in ["nom",'prénom']:
				read = True
				bg_col = self.sc.aff_col1

			self.info_set_surf.add_text(k,
				size_hint = (.15,.1))
			Get_border_input_surf(self.info_set_surf,k,
				(.3,.1),border_col = self.sc.green,
				bg_color = bg_col,
				on_text = self.set_infos,
				readonly = read,
				default_text = v)
			self.info_set_surf.add_padd((.025,.1))

# Gestion des actions de méthodes
	def Save_info(self,wid):
		self.excecute(self.sc.DB.Modif_this_perso,self.perso_infos)
		#self.sc.DB.Modif_this_perso(self.perso_infos)
		self.sc.add_refused_error('Informations modifier avec succès')
		self.add_infos_surf()

	def see_contrat(self,wid):
		self.open_link(wid.info)

	def see_cv(self,wid):
		self.open_link(wid.info)

	def upload_fic(self,selection):
		self.perso_infos["img"] = selection
		self.img_surf.clear_widgets()
		self.img_surf.add_image(selection)
		self.img_surf.add_button('',bg_color = None,
			on_press = self.get_img_from)

	def set_infos(self,wid,val):
		if val:
			self.perso_infos[wid.info] = val

	def Set_con_infos(self,wid):
		if wid.info == "Modifier":
			self.try_modif = True
			self.add_connex_surf()
		else:
			if self.check(self.modif_c):
				pass1 = self.modif_c.get('password')
				pass2 = self.modif_c.get('password again')
				if pass1 == pass2:
					self.perso_infos["username"] = self.modif_c.get('username')
					self.perso_infos['mot de pass'] = self.modif_c.get('password')
					self.sc.add_refused_error('Mot de pass modifier avec succès')
				else:
					self.sc.add_refused_error('Les mots de pass ne corresponde pas')
			else:
				self.sc.add_refused_error('Action de modifications annuler')
			self.modifier = False
			self.try_modif = False
			self.add_connex_surf()

	def modif_conn(self,wid,val):
		self.modif_c[wid.info] = val

	def set_last_pass(self,wid,val):
		if self.perso_infos.get("mot de pass") == val:
			self.modifier = True
			self.add_connex_surf()
		elif len(self.perso_infos.get('mot de pass')) == len(val):
			self.sc.add_refused_error("Mot de pass erroné")
			self.try_modif = False
			self.add_connex_surf()
		else:
			pass

	def Foreign_surf(self):
		self.add_infos_surf()

class Agenda(box):
	"""
		Définition d'un agenda pour programmer de façon personnel ses 
		journées
	"""


class Salaire(Salaires):
	@Cache_error
	def add_liste_surf(self):
		h = .035
		self.liste_surf.clear_widgets()
		self.liste_surf.add_text("Liste des fiches de paie",
			size_hint = (1,h),underline = True,text_color = self.sc.text_col1,
			halign = 'center')
		b = box(self,size_hint = (1,h),orientation = 'horizontal')
		b.add_text('status :',size_hint = (.2,1),text_color = self.sc.text_col1)
		b.add_surf(liste_set(self,self.status,self.status_list,
			mother_fonc = self.set_status,mult = 1,size_hint = (.6,1)))
		self.liste_surf.add_surf(b)

		self.tab_surf = Table(self,bg_color = self.sc.aff_col3,
			padding = dp(10),radius = dp(10),exec_fonc = self.show_fiche,
			exec_key = 'N°')
		self.liste_surf.add_surf(self.tab_surf)
		self.add_tab_surf()

	def size_pos(self):
		w,h = self.liste_size = .4,1
		self.details_size = 1-w,h

		self.liste_surf = box(self,size_hint = self.liste_size,
			spacing = dp(5),padding = dp(10))
		self.details_surf = this_fiche_show(self,dict(),size_hint = self.details_size,
			spacing = dp(5),padding = dp(10))

		self.add_surf(self.liste_surf)
		self.add_surf(self.details_surf)

	@Cache_error
	def add_tab_surf(self):
		entete = "date d'émissions","montant total","status"
		wid_l = .3,.35,.35
		liste = self.Trie_fich()
		self.tab_surf.Creat_Table(wid_l,entete,liste,ent_size = (1,.07))

class this_fiche_show(fiche_show):
	@Cache_error
	def Foreign_surf(self):
		h = .04
		self.clear_widgets()
		if self.New:
			txt = 'Nouvelle fiche de paie'
		else:
			txt = "Détails de la fiche de paie"
		self.add_text(txt,halign = "center",text_color = self.sc.text_col1,
			underline = True,size_hint = (1,h))
		addresse = ', '.join([self.perso_info.get('pays de résidence'),
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
					on_text = self.modif_val,default_text = v,
					readonly = True)
				self.add_padd((.2,h))
		self.obj_deduction_surf = stack(self,size_hint = (1,h),
			spacing = dp(5),bg_color = self.sc.aff_col1,padding = dp(5),
			radius = dp(5))
		self.add_surf(self.obj_deduction_surf)
		self.Up_obj_surf()

		self.last_surf = stack(self,size_hint = (1,h*3),
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

		self.last_surf.add_padd((.3,.5))
		self.last_surf.add_button("imprimer",size_hint = (.4,.5),
			text_color = self.sc.text_col3,bg_color = self.sc.orange,
			on_press = self.imprimer)

	@Cache_error
	def Up_obj_surf(self):
		if self.modif_dic.get('Objet de déduction'):
			deduc = self.modif_dic.get('Objet de déduction')
			self.obj_deduction_surf.clear_widgets()
			self.obj_deduction_surf.add_text('Objet de déduction',
				size_hint = (.2,1),text_color = self.sc.text_col1)
			self.obj_deduction_surf.add_surf(liste_set(self,
				deduc,[deduc],size_hint = (.3,1),mult = 1,
				mother_fonc = self.modif_obj))
			
			self.obj_deduction_surf.add_input("détails",
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				default_text = self.modif_dic.get("détails"),
				size_hint = (.5,1),placeholder = "Détails",
				on_text = self.modif_val)
 
class Agenda(box):
	...

class Connexion(box):
	...

class Postes(box):
	...

