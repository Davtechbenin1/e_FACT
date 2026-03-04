#Coding:utf-8
"""
	Gestion des recrutements

"""
from lib.davbuild import *
from General_surf import *
from ..CMPT.paie_surfs import decaisse_paie
import os

class Recrutements(box):
	@Cache_error
	def initialisation(self):
		if self.mother.access_dic == "all":
			self.access_liste = "all"
		else:
			self.access_liste = self.mother.access_dic.get('Recrutements')
		self.size_pos()
		self.this_cate = str()
		self.this_status = str()
		self.poste_name = str()
		self.this_post = str()
		self.new_rec = False
		self.nbre_set = int()
		self.begin_date = self.sc.get_today()
		self.end_date = self.sc.get_today()
		self.recrut_day = self.sc.get_today()
		self.diffuse = str()
		self.depense = float()
		self.decaisse_obj = False
		self.diffuse_liste = ["radio",'reseaux sociaux',"télévision",
		"média","affiche local"]
		self.select_diffuse = list()

		self.recrut_list = Table(self,size_hint = (1,.85),
			bg_color = self.sc.aff_col3,
			exec_fonc = self.develop_recut,
			exec_key = 'N°')

	def check_access(self,access):
		if self.access_liste == "all":
			return True
		else:
			if access in self.access_liste:
				return True
			else:
				return False

	def size_pos(self):
		w,h = self.new_size = .4,1
		self.corps_size = 1-w,h

		self.this_new_surf = stack(self,size_hint = self.new_size,
			spacing = dp(5),padding = dp(10))

		self.corps_surf = box(self,size_hint = self.corps_size,
			spacing = dp(5),padding = dp(10))

		self.period1 = Periode_set(self,info_w = .25,
			exc_fonc = self.set_periode,size_hint = (1,.04))
		self.period2 = Periode_set(self,
				exc_fonc = self.add_recrute_day,size_hint = (.8,.04),
				one_part = True,info = 'Date de sélection :',
				info_w = .3)
		self.add_surf(self.this_new_surf)
		self.add_text('',size_hint = (None,1),width = dp(1),
			bg_color = self.sc.sep)
		self.add_surf(self.corps_surf)

	@Cache_error
	def Foreign_surf(self):
		self.All_recuit_dic = self.sc.DB.Get_recrutements_()
		self.corps_surf.clear_widgets()
		if self.new_rec:
			self.add_new_recrut()
		elif self.decaisse_obj and self.depense:
			self.add_new_recrut()
		else:
			self.add_aff_recrut()

	@Cache_error
	def add_new_recrut(self):
		h = .04
		self.this_new_surf.clear_widgets()
		self.this_new_surf.add_stack_but(self.aff_recuit)
		self.this_new_surf.add_padd((1,.0000001))
		self.this_new_surf.add_text('poste :',size_hint = (.15,h),
			text_color = self.sc.text_col1)
		self.this_new_surf.add_surf(liste_set(self,self.this_post,
			self.sc.DB.Get_all_post_list(),mother_fonc = self.set_post_name,
			size_hint = (.8,h),mult = 1))
		if self.decaisse_obj and self.depense:
			self.this_new_surf.add_text('Confirmer le décaissement',
				size_hint = (1,h),text_color = self.sc.text_col1,
				halign = "center",font_size = '18sp')
			self.this_new_surf.add_surf(decaisse_paie(self,
				.07,f'Recrutement N° {self.recrut_ident}',
				self.depense,size_hint = (1,.45),
				mother_fonc = self.add_this_decaiss,
				))
		elif self.this_post:
			self.this_post_dic = self.sc.DB.Get_this_poste(self.this_post)
			fonction = self.this_post_dic.get('fonction principal')
			self.this_new_surf.add_text_input("fonction :",(.2,h),(.7,h),
				self.sc.text_col1,text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,default_text = fonction,
				readonly = True)
			dic = {
				"profile :":'\n'.join(self.this_post_dic.get('profile')),
				"tâches :":'\n'.join(self.this_post_dic.get('tâches')),
			}
			for k,v in dic.items():
				self.this_new_surf.add_text_input(k,(.2,h),(.8,h*3),
					self.sc.text_col1,text_color = self.sc.text_col1,
					bg_color = self.sc.aff_col3,readonly = True,
					default_text = v)
			self.this_new_surf.add_text_input('nbres recherchés',(.3,h),(.6,h),
				self.sc.text_col1,text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,on_text = self.set_nbres,
				default_text = str(self.nbre_set))

			self.this_new_surf.add_surf(self.period1)

			self.this_new_surf.add_surf(self.period2)
			
			
			self.this_new_surf.add_text('Moyens de déffusion',
				text_color = self.sc.text_col1,halign = "center",
				underline = True,font_size = "18sp",size_hint = (1,h))
			for k in self.diffuse_liste:
				txt_col = self.sc.text_col1
				bg_color = self.sc.aff_col3
				if k in self.select_diffuse:
					txt_col = self.sc.aff_col2
					bg_color = self.sc.aff_col2
				b = box(self,size_hint = (.33,h),spacing = dp(4),
					orientation = "horizontal")
				b.add_button('',size_hint = (None,None),
					width = dp(20),height = dp(20),info = k,
					bg_color = bg_color,on_press = self.add_diffuse,
					pos_hint = (0,.1))
				b.add_button(k,bg_color = None,text_color = txt_col,
					on_press = self.add_diffuse,halign = "left")
				self.this_new_surf.add_surf(b)
			self.this_new_surf.add_padd((1,.00000001))

			self.this_new_surf.add_text_input("Dépense monétaires :",
				(.4,h),(.3,h),self.sc.text_col1
				,text_color = self.sc.text_col1,
				on_text = self.set_depense,
				bg_color = self.sc.aff_col3,
				default_text = str(self.depense))
			
			self.this_new_surf.add_padd((.3,h))
			self.this_new_surf.add_button_custom("Valider",
				self.valide_recruit,size_hint = (.5,h),
				padd = (.25,h))

	@Cache_error
	def add_aff_recrut(self):
		h = .04
		self.this_new_surf.clear_widgets()
		self.this_new_surf.add_text('Catégories',
			size_hint = (.2,h),
			text_color = self.sc.text_col1)
		self.this_new_surf.add_surf(liste_set(self,
			self.this_cate,self.sc.DB.Get_categories(),
			size_hint = (.8,h),mult = 1,
			mother_fonc = self.set_cat))

		self.this_new_surf.add_text('Natures',
			size_hint = (.2,h),
			text_color = self.sc.text_col1)
		self.this_new_surf.add_surf(liste_set(self,
			self.this_status,self.sc.DB.Get_recuit_nature(),
			size_hint = (.8,h),mult = 1,
			mother_fonc = self.set_nature))

		b = stack(self,size_hint = (1,h),spacing = dp(5))
		b.add_input('nom',size_hint = (.8,1),
			text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,
			on_text = self.Set_poste_name,
			placeholder = 'Nom du poste')
		if "écritures" in self.sc.DB.Get_access_of("Recrutements"):
			b.add_icon_but(icon = 'plus',size_hint = (.2,None),
				text_color = self.sc.green,
				on_press = self.new_recruit,
				size = (dp(50), dp(25)))
		self.this_new_surf.add_surf(b)

		self.this_new_surf.add_surf(self.recrut_list)
		self.add_recrut_list()

	@Cache_error
	def add_recrut_list(self):
		wid_l = [.4,.3,.3]
		entete = ["poste","nbres recherchés",'nature']
		liste = self.Trie_recruit()
		self.recrut_list.Creat_Table(wid_l,entete,liste,
			ent_size = (1,.05))

	def Trie_recruit(self):
		dic = self.All_recuit_dic
		dic = {i:j for i,j in dic.items() if 
		self.this_cate in j.get('catégorie',str())}
		dic = {i:j for i,j in dic.items() if 
		self.this_status in j.get('nature',str())}
		liste = [j for i,j in dic.items() if 
		self.poste_name in j.get('poste',str())]
		return liste

#Gestion des actions des méthodes
	@Cache_error
	def add_this_decaiss(self,ident):
		if "écritures" in self.sc.DB.Get_access_of("Décaissement"):
			dic = self.sc.DB.Get_this_recrut(self.recrut_ident)
			dic["dépense soldée"] = True
			dic["decaissement"] = ident
			self.sc.DB.Save_recrutements(dic)
		else:
			self.sc.add_refused_error("Impossible de continuer à cause d'une restriction système !! Parlez-en à votre supérieur hiérachique")

	def set_depense(self,wid,val):
		try:
			float(val)
		except:
			wid.text = self.regul_input(wid.text)
			if wid.text:
				self.depense = float(wid.text)
			else:
				self.depense = float()
		else:
			self.depense = float(val)

	@Cache_error
	def Valide_decais(self,wid):
		self.decaisse_obj = True
		self.recrut_ident = self.valide_recruit(wid)
		if self.recrut_ident:
			self.add_new_recrut()

	def add_diffuse(self,wid):
		if wid.info in self.select_diffuse:
			self.select_diffuse.remove(wid.info)
		else:
			self.select_diffuse.append(wid.text)
		self.add_new_recrut()

	def set_periode(self):
		self.begin_date = self.day1
		self.end_date = self.day2

		self.sc.day1 = self.sc.get_today()
		self.sc.day2 = self.sc.get_today()

	def add_recrute_day(self):
		self.recrut_day = self.day1
		self.sc.day1 = self.sc.get_today()

	@Cache_error
	def valide_recruit(self,wid):
		if self.nbre_set:
			self.new_rec = False
			This_rec_dic = self.sc.DB.Get_recrutement_format()
			This_rec_dic["poste"] = self.this_post
			This_rec_dic["catégorie"] = self.this_post_dic.get('catégorie')
			This_rec_dic["profile"] = self.this_post_dic.get('profile')
			This_rec_dic["tâches"] = self.this_post_dic.get('tâches')
			This_rec_dic["fonction principal"] = self.this_post_dic.get('fonction principal')
			This_rec_dic["date de lancement"] = self.begin_date
			This_rec_dic["date de clôture"] = self.end_date
			This_rec_dic["date de sélection"] = self.recrut_day
			This_rec_dic["nbres recherchés"] = self.nbre_set
			This_rec_dic["moyen de diffusion"] = self.select_diffuse
			This_rec_dic["dépense monétaire"] = self.depense
			self.sc.hand_recut_one(This_rec_dic)
			#self.sc.DB.Save_recrutements(This_rec_dic)
			self.sc.add_refused_error('recrutement sauvegardé')
			self.new_rec = False
			self.add_all()
			return This_rec_dic['N°']
		else:
			self.sc.add_refused_error('Vous devez spécifier le nombre de personnes souhaiter')

	@Cache_error
	def develop_recut(self,wid):
		self.corps_surf.clear_widgets()
		recrut_dic = self.sc.DB.Get_this_recrut(wid.info)
		surf = developpe_recrut(self,recrut_dic)
		surf.add_all()
		self.corps_surf.add_surf(surf)

	def set_nbres(self,wid,val):
		try:
			int(val)
		except:
			wid.text = self.regul_input(wid.text)
			if wid.text:
				self.nbre_set = int(wid.text)
			else:
				self.nbre_set = 0
		else:
			self.nbre_set = int(val)

	def set_post_name(self,info):
		if self.this_post:
			self.this_post = str()
		else:
			self.this_post = info

		self.add_new_recrut()

	def set_cat(self,info):
		if self.this_cate:
			self.this_cate = str()
		else:
			self.this_cate = info

	def set_nature(self,info):
		if self.this_status:
			self.this_status = str()
		else:
			self.this_status = info

	def Set_poste_name(self,wid,val):
		self.poste_name = val

	def new_recruit(self,wid):
		self.new_rec = True
		self.add_all()

	def aff_recuit(self,wid):
		self.new_rec = False
		self.add_all()

class developpe_recrut(box):
	def __init__(self,mother,recrut_dic,**kwargs):
		box.__init__(self,mother,**kwargs)
		self.check_access = self.mother.check_access
		self.recrut_dic = recrut_dic
		self.questionaire = '\n'.join(self.recrut_dic.get('questionnaires entretient',list()))
		self.disponible = str()
		self.dispo_l = ['Immédiate',"sous contrat","en cas de besoin"]
		self.size_pos()

	def initialisation(self):
		self.this_dic = dict()
		self.show_cand_l = True
		self.cv_lien = str()
		self.quest_def = False

	@Cache_error
	def Foreign_surf(self):
		self.add_infos_recrut_surf()
		self.add_candidat_surf()

	def size_pos(self):
		self.clear_widgets()
		w,h = self.infos_recrut_size = 1,.47
		self.candidat_size = w,1-h

		self.infos_recrut_surf = stack(self,size_hint = self.infos_recrut_size,
			padding = dp(5),spacing = dp(5))
		self.candidat_surf = stack(self,size_hint = self.candidat_size,
			padding = dp(5),spacing = dp(10))

		self.add_surf(self.infos_recrut_surf)
		self.add_surf(self.candidat_surf)

	@Cache_error
	def add_infos_recrut_surf(self):
		h = .115
		self.infos_recrut_surf.clear_widgets()
		txt = f"Recrutement N° {self.recrut_dic.get('N°')}"
		self.infos_recrut_surf.add_text(txt,text_color = self.sc.aff_col2,
			halign = "center",font_size = '18sp',size_hint = (.5,h))
		txt2 = f"A la recherche de {self.recrut_dic.get('nbres recherchés')} Ps pour le poste de <{self.recrut_dic.get('poste')}>"
		self.infos_recrut_surf.add_text(txt2,text_color = self.sc.text_col1,
			size_hint = (.5,h),halign = 'center')
		if self.quest_def:
			self.infos_recrut_surf.add_text_input('Questionnaires :',
				(.2,h),(.7,h*7),self.sc.text_col1,on_text = self.quest_set,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				default_text = self.questionaire,multiline = True,
				placeholder = 'Questionnaires séparer par la touche entrée',
				)
			if "écritures" in self.sc.DB.Get_access_of("Recrutements"):
				self.infos_recrut_surf.add_padd((.3,h))
				self.infos_recrut_surf.add_button('Enrégistrer',
					text_color = self.sc.text_col3,bg_color = self.sc.aff_col2,
					on_press = self.Save_quest,size_hint = (.4,h))
		else:
			dic = {
				"Dossiers reçus":len(self.recrut_dic.get('dossiers reçus')),
				"Reçu en entretient":len(self.recrut_dic.get('reçus en entretient')),
				"Rejettés":len(self.recrut_dic.get('rejettés')),
				"Retenus":len(self.recrut_dic.get('retenus')),
			}
			for k,v in dic.items():
				self.infos_recrut_surf.add_text_input(k,(.18,h),(.32,h),
					self.sc.text_col1,text_color = self.sc.text_col1,
					bg_color = self.sc.aff_col3,readonly = True,
					default_text = self.format_val(v))
			profile = "\n".join(self.recrut_dic.get('profile'))
			self.infos_recrut_surf.add_text_input("Profile :",
				(.1,h),(.4,h*4),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				readonly = True,default_text = profile)
			st_b = stack(self,size_hint = (.5,h*3),spacing = dp(5))
			dic1 = {
				"Date de lancement :":{"day1":self.recrut_dic.get('date de lancement')},
				"Date de clôture :":{"day1":self.recrut_dic.get('date de clôture')},
				"Date de sélection :":{"day1":self.recrut_dic.get('date de sélection')},			
			}
			for k,d in dic1.items():
				st_b.add_surf(Periode_set(self, info = k,
					date_dict = d,one_part = True,
					info_w = .33,size_hint = (1,.33)))
			self.infos_recrut_surf.add_surf(st_b)

			self.infos_recrut_surf.add_text_input("Dépense :",
				(.15,h),(.15,h),self.sc.text_col1,text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,default_text = self.format_val(
					self.recrut_dic.get('dépense monétaire')),readonly = True)
			if self.recrut_dic.get('dépense soldée'):
				self.infos_recrut_surf.add_button(self.recrut_dic.get('decaissement'),
					text_color = self.sc.text_col3,
					bg_color = self.sc.aff_col2,
					on_press = self.show_decaisse,
					size_hint = (.35,h))
			else:
				if "écritures" in self.sc.DB.Get_access_of("Décaissement"):
					self.infos_recrut_surf.add_button_custom('Décaisser',
						self.add_decaisse,size_hint = (.2,h),)
			self.infos_recrut_surf.add_button("Questionnaires d'entretients",
				size_hint = (.33,h),on_press = self.def_question,
				text_color = self.sc.text_col3,bg_color = self.sc.orange,
				)
			if "écritures" in self.sc.DB.Get_access_of("Recrutements"):
				self.infos_recrut_surf.add_button("Archiver",
					size_hint = (.13,h),on_press = self.archiver,
					text_color = self.sc.text_col3,bg_color = self.sc.red,
					)
	@Cache_error
	def add_candidat_surf(self):
		h = .095
		self.cand_tab = Table(self,size_hint = (1,.79),
			exec_fonc = self.show_candidat,exec_key = 'N°',
			bg_color = self.sc.aff_col3)
		self.candidat_surf.clear_widgets()
		self.candidat_surf.add_text('Gestion des candidats',
			size_hint = (.8,.08),halign = 'center',font_size = '20sp',
			underline = True,text_color = self.sc.text_col1)
		if self.show_cand_l:
			self.add_cand_list()
			self.candidat_surf.add_surf(Periode_set(self,
				size_hint = (.8,h),exc_fonc = self.add_cand_list,
				info_w = .2))
			this_nature = self.recrut_dic.get('nature')
			if this_nature == 'En cours':
				if "écritures" in self.sc.DB.Get_access_of('Candidat'):
					self.candidat_surf.add_button('Nouveau candidat',
						size_hint = (.2,h),text_color = self.sc.text_col3,
						bg_color = (1,.5,.15),on_press = self.new_candidat)
			self.candidat_surf.add_surf(self.cand_tab)
		
		else:
			d1 = {
				"nom":str(),
				"prénom":str(),
				"téléphone":str(),
				"whatsapp":str(),
				'lieu de naissance':str(),
				"NIP":str(),
			}
			self.candidat_surf.add_icon_but(icon = "close", size_hint = (.2,.08),
				on_press = self.show_candidat_lis,text_color = self.sc.red)
			for k,v in d1.items():
				self.candidat_surf.add_text_input(k,(.2,h),(.3,h),
					self.sc.text_col1,text_color = self.sc.text_col1,
					bg_color = self.sc.aff_col3,
					on_text = self.set_info)
			self.candidat_surf.add_surf(Periode_set(self,
				size_hint = (.5,h),
				info = 'date de naissance :',info_w = .2,
				exc_fonc = self.set_naissance,one_part = True))
			d2 = {
				"pays de résidence":str(),
				"ville de résidence":str(),
				"quartier":str(),
				"maison":str(),
			}
			for k,v in d2.items():
				self.candidat_surf.add_text_input(k,(.2,h),(.3,h),
					self.sc.text_col1,text_color = self.sc.text_col1,
					bg_color = self.sc.aff_col3,
					on_text = self.set_info)
			self.candidat_surf.add_text('disponibilité :',
				text_color = self.sc.text_col1,size_hint = (.2,h),
				)
			self.candidat_surf.add_surf(liste_set(self,self.disponible,
				self.dispo_l,size_hint = (.3,h),mult = 1,
				mother_fonc = self.dispo_set
				))
			self.last_surf = box(self,size_hint = (1,h),
				orientation = 'horizontal',spacing = dp(10))
			self.add_last_surf()
			self.candidat_surf.add_surf(self.last_surf)
			self.candidat_surf.add_padd((1,.002))
			self.candidat_surf.add_padd((.25,h))
			self.candidat_surf.add_button("Ajouter le candidat",
				size_hint = (.5,h),text_color = self.sc.text_col3,
				bg_color = self.sc.aff_col2,on_press = self.add_cand)

	def add_cand_list(self):
		wid_l = [.15,.15,.2,.15,.2,.15]
		entete = ["nom","prénom","nationalité",
		"date de dépot","quartier","status"]
		liste = self.get_cand_list(self.recrut_dic.get('N°'))
		self.cand_tab.Creat_Table(wid_l,entete,liste,
			ent_size = (1,.12),ligne_h = .15)

	@Cache_error
	def add_last_surf(self):
		self.last_surf.clear_widgets()
		self.last_surf.add_text_input("CV:",(.06,1),(.5,1),
			self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,default_text = self.cv_lien,
			placeholder = 'Choisi le fichier du cv',
			readonly = True)
		self.last_surf.add_button('Parcourir',text_color = self.sc.text_col3,
			bg_color = self.sc.aff_col2,on_press = self.get_img_from,
			size_hint = (.2,1))

	def get_cand_list(self,ident):
		date_liste = self.get_date_list(self.day1,self.day2)
		liste = self.sc.DB.Get_cand_from(ident,date_liste)
		return liste

# Gestion des actions au niveau des méthodes
	@Cache_error
	def archiver(self,wid):
		self.recrut_dic['nature'] = "Supprimer"
		self.sc.DB.Save_recrutements(self.recrut_dic)
		self.sc.add_refused_error(f'Recrutement {self.recrut_dic.get("N°")} Supprimer avec succès')
		self.mother.add_all()

	@Cache_error
	def Save_quest(self,wid):
		if self.questionaire:
			info_list = self.questionaire.split('\n')
			self.recrut_dic["questionnaires entretient"] = info_list
			self.sc.DB.Save_recrutements(self.recrut_dic)
			self.sc.add_refused_error('Questionnaires modifiés')
		else:
			pass
		self.quest_def = False
		self.add_infos_recrut_surf()

	def quest_set(self,wid,val):
		self.questionaire = val

	def upload_fic(self,selection):
		#if selection:
		self.cv_lien = selection
		self.add_last_surf()

	def def_question(self,wid):
		self.quest_def = True
		self.add_infos_recrut_surf()

	def new_candidat(self,wid):
		self.show_cand_l = False
		self.add_candidat_surf()

	def show_candidat_lis(self,wid):
		self.show_cand_l = True
		self.add_candidat_surf()

	@Cache_error
	def show_candidat(self,wid):
		self.clear_widgets()
		cnd_key = wid.info
		self.add_surf(gestion_candidat(self,self.recrut_dic,cnd_key))

	@Cache_error
	def Refresh(self,wid):
		self.clear_widgets()
		self.size_pos()
		self.add_all()

	@Cache_error
	def add_cand(self,wid):
		if not self.this_dic.get('nom'):
			self.sc.add_refused_error('Toutes les informations sont nécessaires')
		else:
			cand_info = self.sc.DB.Get_candidat_format()
			cand_info.update(self.this_dic)
			cand_info['disponibilité'] = self.disponible
			if self.cv_lien:
				cand_info['cv'] = self.sc.DB.Save_image(self.cv_lien)
			ident = self.recrut_dic.get('N°')
			self.excecute(self._add_cond,ident,cand_info)
			self.sc.add_refused_error(f"Candidat prise en compte")
			self.this_dic = {i:str() for i in self.this_dic}
			self.add_candidat_surf()
			self.add_infos_recrut_surf()

	def _add_cond(self,ident,cand_info):
		cand_n = self.sc.DB.Save_candidat(ident,cand_info)
		self.sc.DB.Add_dossier(cand_n,ident)

	def set_info(self,wid,val):
		self.this_dic[wid.info] = val

	def set_naissance(self):
		self.this_dic['date de naissance'] = self.day1
		self.sc.day1 = self.sc.get_today()

	def dispo_set(self,info):
		if self.disponible:
			self.disponible = str()
		else:
			self.disponible = info

	@Cache_error
	def add_decaisse(self,wid):
		self.infos_recrut_surf.clear_widgets()
		self.infos_recrut_surf.add_stack_but(self.back_surf)
		depense = self.recrut_dic.get("dépense monétaire")
		self.infos_recrut_surf.add_surf(
			decaisse_paie(self,.07,
				f'Recrutement N° {self.recrut_dic.get("N°")}',
				depense,size_hint = (.7,1),
				mother_fonc = self.add_this_decaiss,
				)
		)

	def back_surf(self,wid):
		self.add_infos_recrut_surf()
	
	def show_decaisse(self,wid):
		pass

	def add_this_decaiss(self,ident):
		self.recrut_dic["dépense soldée"] = True
		self.recrut_dic["decaissement"] = ident
		self.sc.DB.Save_recrutements(self.recrut_dic)

class gestion_candidat(stack):
	def __init__(self,mother,recrut_dic,cnd_key,**kwargs):
		kwargs['spacing'] = dp(10)
		stack.__init__(self,mother,**kwargs)
		self.recrut_dic = recrut_dic
		ident = self.recrut_dic.get('N°')
		cnd_dic = self.sc.DB.Get_this_candidat(ident,cnd_key)
		self.cnd_dic = cnd_dic
		self.recruit_ident = self.recrut_dic.get("N°")
		self.quest_l = self.recrut_dic.get('questionnaires entretient')
		self.response_dic = {i:str() for i in self.quest_l}
		dic =  self.cnd_dic.get('reponses',dict())
		self.response_dic.update(dic)

		self.date_fonc = self.sc.get_today()
		self.contrat_fic = str()
		self.duree = float()

		self.size_pos()
		self.add_all()

	@Cache_error
	def Foreign_surf(self):
		self.add_infos()

	@Cache_error
	def size_pos(self):
		self.quest_surf = box(self,size_hint = (1,.45))
		self.entretient_surf = False
		
	@Cache_error
	def add_infos(self):
		h = .05
		self.clear_widgets()
		nom = self.cnd_dic.get('nom')+ ' ' + self.cnd_dic.get('prénom')
		self.add_text(f"Gestion du candidat {nom}",
			text_color = self.sc.text_col1, halign = "center",
			size_hint = (.9,h),underline = True)
		self.add_icon_but(icon = "close",text_color = self.sc.red,
			size_hint = (.1,h),on_press = self.mother.Refresh)
		dic1 = {
			"nom :":self.cnd_dic.get('nom'),
			"prénom :":self.cnd_dic.get('prénom'),
			"date de naissance :":self.cnd_dic.get('date de naissance'),
			"lieu de naissance :":self.cnd_dic.get('lieu de naissance'),
			"nationalité :":self.cnd_dic.get('nationalité'),
			"pays de résidence :":self.cnd_dic.get('pays de résidence'),
			"ville de résidence :":self.cnd_dic.get('ville de résidence'),
			"téléphone :":self.cnd_dic.get('téléphone'),
			"whatsapp :":self.cnd_dic.get('whatsapp'),
			"email :":self.cnd_dic.get('email'),
			"quartier :":self.cnd_dic.get('quartier'),
			"maison :":self.cnd_dic.get('maison'),
			"disponibilité :":self.cnd_dic.get('disponibilité'),
			"status :":self.cnd_dic.get('status'),
			"date de dépot :":self.cnd_dic.get('date de dépot'),
		}
		for k,v in dic1.items():
			self.add_text_input(k,(.15,h),(.18,h),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				default_text = str(v),readonly = True)
		self.add_padd((1,.0000001))
		self.add_padd((.1,h))
		if "écritures" in self.sc.DB.Get_access_of('Gestion Candidat'):
			self.add_button('Voir le cv',bg_color = self.sc.aff_col2,
				text_color = self.sc.text_col3,on_press = self.cv_show,
				info = self.cnd_dic.get('cv',str()),size_hint = (.3,h))
			liste = self.sc.DB.Get_candidat_opts(self.cnd_dic.get('status'))
			for opt in liste:
				bg_col = self.sc.aff_col2
				if "rejetter" in opt.lower():
					bg_col = self.sc.red
				elif "entretient" in opt.lower():
					bg_col = self.sc.orange
				elif "contrat" in opt.lower():
					bg_col = self.sc.orange
				self.add_button(opt,bg_color = bg_col,
					text_color = self.sc.text_col3,
					on_press = self.opt_set,
					info = opt,size_hint = (.3,h))
		self.add_surf(self.quest_surf)
		
		self.last_surf = stack(self,size_hint = (1,h*2),spacing = dp(5))
		self.add_surf(self.last_surf)
		self.add_ent_surf()

	@Cache_error
	def add_ent_surf(self):
		self.quest_surf.clear_widgets()
		self.quest_surf.add_text("Formulaire d'entretient",
			size_hint = (1,None),
			text_color = self.sc.text_col1,halign = 'center',
			height = dp(30),underline = True)
		readonly = True
		if self.entretient_surf:
			readonly = False
		
		h = dp(70)
		H = len(self.response_dic) * (h + dp(10))
		H += dp(10)
		stw = stack(self,size_hint = (1,None),height = H,
			spacing = dp(10))
		
		for k,v in self.response_dic.items():
			stw.add_text(k,text_color = self.sc.text_col1,
				size_hint = (.22,None),height = h)
			stw.add_input(k,text_color = self.sc.text_col1,
				size_hint = (.28,None),height = h,readonly = readonly,
				on_text = self.set_response,bg_color = self.sc.aff_col3,
				default_text = str(v),multiline = True)
		
		src = scroll(self)
		src.add_surf(stw)
		self.quest_surf.add_surf(src)
		self.add_last_surf()

	@Cache_error
	def add_retenue(self):
		h = .1
		self.quest_surf.clear_widgets()
		self.quest_surf.add_text("Finalisation",size_hint = (1,None),
			text_color = self.sc.text_col1,halign = 'center',
			height = dp(20))
		stw = stack(self,size_hint = (.6,1),
			pos_hint = (.2,0),spacing = dp(10))
		stw.add_surf(Periode_set(self,info = "Date de prise de fonction :",
			one_part = True,info_w = .3,exc_fonc = self.set_date_fonc,
			size_hint = (1,h),date_dict = {"day1":self.date_fonc}))
		stw.add_text_input('Contrat de travail :',(.3,h),(.4,h),
			self.sc.text_col1, text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,default_text = self.contrat_fic,
			readonly = True)
		stw.add_button('Parcourir',size_hint = (.2,h),
			text_color = self.sc.text_col3,bg_color = self.sc.orange,
			on_press = self.get_img_from)
		stw.add_text_input('Durée :',(.15,h),(.35,h),
			self.sc.text_col1, bg_color = self.sc.aff_col3,
			text_color = self.sc.text_col1,on_text = self.set_durer,
			default_text = str(self.duree))
		stw.add_text('Jours',size_hint = (.5,h),
			text_color = self.sc.text_col1)
		stw.add_padd((.3,h))
		stw.add_button('Valider',size_hint = (.4,h),
			on_press = self.Valide_prise_fonc,
			text_color = self.sc.text_col3,
			bg_color = self.sc.aff_col2)
		self.quest_surf.add_surf(stw)
	
	@Cache_error
	def add_last_surf(self):
		self.last_surf.clear_widgets()
		if self.entretient_surf:
			self.last_surf.add_padd((.3,.5))
			self.last_surf.add_button("Enrégistrer l'entretient",
				size_hint = (.4,.5),text_color = self.sc.text_col3,
				bg_color = self.sc.aff_col2,on_press = self.Save_entre)
	
	@Cache_error
	def quitter(self):
		self.mother.Refresh(self)

# Gestion des actions des buttons
	@Cache_error
	def Valide_prise_fonc(self,wid):
		dic = {
			"date de prise de fonction":self.date_fonc,
			"durée de contrat":self.duree
		}
		if self.check(dic):
			self.cnd_dic["status"] = "Retenue"
			self.cnd_dic['contrat'] = self.contrat_fic
			rec_id = self.cnd_dic.get('recrutement id')

			
			perso_dic = self.sc.DB.Get_perso_save_format()
			perso_dic.update(self.cnd_dic)
			perso_dic.update(dic)
			if self.contrat_fic:
				perso_dic['contrat de travail'] = self.contrat_fic
			perso_dic['type'] = self.recrut_dic.get('catégorie')
			perso_dic['poste actuel'] = self.recrut_dic.get('poste')
			perso_dic['postes occupés'] = {
			self.recrut_dic.get('poste'):{
				"contrat":self.contrat_fic,
				"durée":self.duree,
				"date de début":self.date_fonc,
			}}
			self.excecute(self._valid_info,perso_dic,rec_id)
			self.sc.add_refused_error('Personnel Ajouté avec succès')
			self.quitter()
		else:
			self.sc.add_refused_error("Les informations sont obligatoires")

	def _valid_info(self,perso_dic,rec_id):
		self.sc.DB.Save_candidat(rec_id,self.cnd_dic)
		self.sc.DB.Add_dossier_retenus(self.cnd_dic.get("N°"),
			rec_id)

		perso_id = self.sc.DB.Save_personnel(perso_dic)
		self.sc.DB.add_employer(self.recrut_dic.get('poste'),
			perso_id)

	def set_durer(self,wid,val):
		wid.text = self.regul_input(wid.text)	
		if wid.text:
			self.duree = float(wid.text)
		else:
			self.duree = 0

	def set_date_fonc(self):
		self.date_fonc = self.day1
		self.sc.day1 = self.sc.get_today()

	@Cache_error
	def Save_entre(self,wid):
		if self.check(self.response_dic):
			self.cnd_dic['reponses'] = self.response_dic
			self.cnd_dic['status'] = "Reçus en entretient"
			self.excecute(self._Save_entre)
			self.sc.add_refused_error('Questionnaires prise en compte')
			self.quitter()
		else:
			self.sc.add_refused_error('Toutes les champs sont obligatoires')

	def _Save_entre(self):
		self.sc.DB.Save_candidat(self.recruit_ident,self.cnd_dic)
		self.sc.DB.Add_recus_en_entretient(self.cnd_dic.get("N°"),
			self.recruit_ident)
	
	def cv_show(self,wid):
		lien = wid.info
		if lien:
			os.startfile(lien)

	def upload_fic(self,selection):
		self.contrat_fic = selection
		self.add_retenue()

	def set_response(self,wid,val):
		self.response_dic[wid.info] = val

	@Cache_error
	def opt_set(self,wid):
		if wid.info == 'Entretient':
			self.entretient_surf = True
			self.add_ent_surf()

		elif wid.info == "Retenue":
			if self.sc.DB.Check_recruit_add_perso(self.recruit_ident):
				self.retenue_surf = True
				self.add_retenue()
			else:
				self.sc.add_refused_error('Vous avez atteint la limite de recrutement')
				self.mother.size_pos()
				self.mother.add_all()

		elif wid.info == "Voir le contrat":
			lien = self.cnd_dic.get('contrat')
			if lien:
				os.startfile(lien)
			else:
				self.sc.add_refused_error('Aucun fichier pour le contrat trouvé')

		elif wid.info == "Rejetter":
			self.cnd_dic["status"] = "Rejettés"
			rec_id = self.cnd_dic.get('recrutement id')
			self.excecute(self._opt_set1_,rec_id)
			self.mother.size_pos()
			self.mother.add_all()

		elif wid.info == "Relancer":
			self.cnd_dic["status"] = "En étude"
			rec_id = self.cnd_dic.get('recrutement id')
			self.excecute(self._opt_set2_,rec_id)
			self.mother.size_pos()
			self.mother.add_all()

	def _opt_set1_(self,rec_id):
		self.sc.DB.Save_candidat(rec_id,self.cnd_dic)
		self.sc.DB.Add_dossier_rejetter(self.cnd_dic.get("N°"),
			rec_id)

	def _opt_set2_(self,rec_id):
		self.sc.DB.Save_candidat(rec_id,self.cnd_dic)
		self.sc.DB.Sup_dossier_rejetter(self.cnd_dic.get("N°"),
			rec_id)









