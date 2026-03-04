#Coding:utf-8
"""
	Gestion de la génération des documents d'impression et d'envoie.
"""

#"""
from lib.davbuild import *
from General_surf import *
import datetime as DAT_T
import os
from kivy.uix.popup import Popup
from .model_fact import *
from .model_normal import *
from .resumer import *

class Factures(box):
	@Cache_error
	def initialisation(self):
		f_ju = self.sc.DB.Get_ent_part("forme juridique")
		self.ent_infos = {
			"Enseigne":self.sc.DB.Get_ent_part("sigle")+ f' {f_ju}',
			"IFU":self.sc.DB.Get_ent_part("IFU"),
			"RCCM":self.sc.DB.Get_ent_part("RCCM"),
			"activite":self.sc.DB.Get_ent_part("activitée principal"),
			"téléphone":self.sc.DB.Get_ent_part("téléphone"),
			"whatsapp":self.sc.DB.Get_ent_part('whatsapp'),
			"addresse":self.sc.DB.Get_ent_part('addresse')
		}
		self.logo = self.sc.DB.Get_ent_part('logo')

		self.bg_col = (1,1,1)
		self.txt_col = (0,0,0)
		self.gris = (.4,.4,.4)
		self.model = "Modèle 1"
		self.model_part = {
			"Modèle 1":"media/model1.png"
		}
		self.model_list = ["Modèle 1"]#,"Modèle 2","Modèle 3","Modèle 4",]
		self.typ_list = "PROFORMA","FACTURE",'DEVIS'
		self.typ = str()
		self.size_pos()
		self.Fact_POPUP()

	def size_pos(self):
		self.model_entete = Model1(self)
	
	#@Cache_error
	def Create_fact(self,model):
		self.client = self.cmd_dic.get('client')
		self.clt_dic = self.sc.DB.Get_this_clt(self.client)
		
		self.model_entete.set_model1()

	@Cache_error
	def Fact_POPUP(self,*args):
		title = "Impression de facture"
		text = "Choix du modèle d'impression"

		Edit_surf = stack(self,bg_color = self.sc.aff_col1)
		Edit_surf.add_text(text,
			size_hint = (1,.07),text_color = self.sc.text_col1,
			halign = 'center',font_size = "20sp")

		Edit_surf.add_text('Type de facture :',size_hint = (.3,.07),
			text_color = self.sc.text_col1,
			padding_left = dp(10))
		
		but_st = stack(self,size_hint = (1,.12),spacing = dp(15),
			padding = dp(10))
		but_st.add_padd((.4,1))

		def dismis_fonc(*a):
			self.popup.dismiss()

		def chang_surf(info):
			self.model = info
			img = self.model_part.get(self.model,str())
			self.img_surf.clear_widgets()
			self.img_surf.add_image(img)

		def chang_typ(info):
			self.typ = info

		def accept_fonc(*a):
			if self.model and self.typ:
				self.Create_fact(self.model)
				self.popup.dismiss()
			else:
				self.sc.add_refused_error('Le choix du model et le type de factures est impératif!')

		self.typ = self.cmd_dic.get('type de facture').upper()
		Edit_surf.add_surf(liste_set(self,self.typ,self.typ_list,
			size_hint = (.2,.07),mult = 3,mother_fonc = chang_typ))

		Edit_surf.add_text('Modèle :',size_hint = (.3,.07),
			text_color = self.sc.text_col1,
			padding_left = dp(10))

		Edit_surf.add_surf(liste_set(self,self.model,self.model_list,
			size_hint = (.2,.07),mult = 3,mother_fonc = chang_surf))
		img = self.model_part.get(self.model,str())
		self.img_surf = box(self,size_hint = (1,.65))
		self.img_surf.add_image(img)
		Edit_surf.add_surf(self.img_surf)

		but_st.add_button("Annuler",text_color = self.sc.text_col3,
			bg_color = self.sc.green,size_hint = (.2,1),on_press = dismis_fonc)
		but_st.add_padd((.1,1))
		but_st.add_button("Imprimer",text_color =self.sc.text_col3,
			bg_color = self.sc.red,size_hint = (.2,1),on_press = accept_fonc)
		Edit_surf.add_surf(but_st)
		self.popup = Popup(title=title,content = Edit_surf,
			size_hint = (.35,.6))
		self.popup.open()

class Factures_normal(box):
	@Cache_error
	def initialisation(self):
		f_ju = self.sc.DB.Get_ent_part("forme juridique")
		self.ent_infos = {
			"Enseigne":self.sc.DB.Get_ent_part("sigle")+ f' {f_ju}',
			"IFU":self.sc.DB.Get_ent_part("IFU"),
			"RCCM":self.sc.DB.Get_ent_part("RCCM"),
			"activite":self.sc.DB.Get_ent_part("activitée principal"),
			"téléphone":self.sc.DB.Get_ent_part("téléphone"),
			"whatsapp":self.sc.DB.Get_ent_part('whatsapp'),
			"addresse":self.sc.DB.Get_ent_part('addresse')
		}
		self.logo = self.sc.DB.Get_ent_part('logo')

		self.bg_col = (1,1,1)
		self.txt_col = (0,0,0)
		self.gris = (.4,.4,.4)
		self.model = "Modèle 1"
		self.model_part = {
			"Modèle 1":"media/model1.png"
		}
		self.model_list = ["Modèle 1"]#,"Modèle 2","Modèle 3","Modèle 4",]
		self.typ_list = "PROFORMA","FACTURE",'DEVIS'
		self.typ = str()
		self.size_pos()
		self.Fact_POPUP()

	def size_pos(self):
		self.model_entete = Model_norm(self)
	
	@Cache_error
	def Create_fact(self,model):
		self.client = self.cmd_dic.get('client')
		self.clt_dic = self.sc.DB.Get_this_clt(self.client)
		
		self.model_entete.set_model1()

	@Cache_error
	def Fact_POPUP(self,*args):
		title = "Impression de facture"
		text = "Choix du modèle d'impression"

		Edit_surf = stack(self,bg_color = self.sc.aff_col1)
		Edit_surf.add_text(text,
			size_hint = (1,.07),text_color = self.sc.text_col1,
			halign = 'center',font_size = "20sp")

		Edit_surf.add_text('Type de facture :',size_hint = (.3,.07),
			text_color = self.sc.text_col1,
			padding_left = dp(10))
		
		but_st = stack(self,size_hint = (1,.12),spacing = dp(15),
			padding = dp(10))
		but_st.add_padd((.4,1))

		def dismis_fonc(*a):
			self.popup.dismiss()

		def chang_surf(info):
			self.model = info
			img = self.model_part.get(self.model,str())
			self.img_surf.clear_widgets()
			self.img_surf.add_image(img)

		def chang_typ(info):
			self.typ = info

		def accept_fonc(*a):
			if self.model and self.typ:
				self.Create_fact(self.model)
				self.popup.dismiss()
			else:
				self.sc.add_refused_error('Le choix du model et le type de factures est impératif!')

		self.typ = self.cmd_dic.get('type de facture').upper()
		Edit_surf.add_surf(liste_set(self,self.typ,self.typ_list,
			size_hint = (.2,.07),mult = 3,mother_fonc = chang_typ))

		Edit_surf.add_text('Modèle :',size_hint = (.3,.07),
			text_color = self.sc.text_col1,
			padding_left = dp(10))

		Edit_surf.add_surf(liste_set(self,self.model,self.model_list,
			size_hint = (.2,.07),mult = 3,mother_fonc = chang_surf))
		img = self.model_part.get(self.model,str())
		self.img_surf = box(self,size_hint = (1,.65))
		self.img_surf.add_image(img)
		Edit_surf.add_surf(self.img_surf)

		but_st.add_button("Annuler",text_color = self.sc.text_col3,
			bg_color = self.sc.green,size_hint = (.2,1),on_press = dismis_fonc)
		but_st.add_padd((.1,1))
		but_st.add_button("Imprimer",text_color =self.sc.text_col3,
			bg_color = self.sc.red,size_hint = (.2,1),on_press = accept_fonc)
		Edit_surf.add_surf(but_st)
		self.popup = Popup(title=title,content = Edit_surf,
			size_hint = (.35,.6))
		self.popup.open()

class Resumer_imp(box):
	@Cache_error
	def initialisation(self):
		self.forma_liste = "Portrait",'Paysage'
		self.forma = 'Portrait'
	
	@Cache_error
	def Create_fact(self,wid_l,entete,liste,titre,info):
		self.wid_l = list(wid_l)
		self.entete = list(entete)
		self.liste = list(liste)
		self.titre = titre
		self.info = info

		self.Fact_POPUP()

	@Cache_error
	def Fact_POPUP(self,*args):
		h = .15
		Edit_surf = stack(self,bg_color = self.sc.aff_col1)
		Edit_surf.add_text('Forme du document ',size_hint = (.3,h),
			text_color = self.sc.text_col1,
			padding_left = dp(10))

		but_st = stack(self,size_hint = (1,h),
			spacing = dp(10))
		
		def dismis_fonc(*a):
			self.popup.dismiss()

		def chang_typ(info):
			self.forma = info

		def accept_fonc(*a):
			if self.forma:
				obj = Resumer(self,self.titre,self.info,self.forma)
				obj.Create(self.wid_l,self.entete,self.liste)
				self.popup.dismiss()
			else:
				self.sc.add_refused_error('Le choix du forma est impératif !')

		Edit_surf.add_surf(liste_set(self,self.forma,self.forma_liste,
			size_hint = (.2,h),mult = 3,mother_fonc = chang_typ))
		Edit_surf.add_padd((1,h*4))
		but_st.add_padd((.4,1))
		but_st.add_button("Annuler",text_color = self.sc.text_col3,
			bg_color = self.sc.red,size_hint = (.2,1),on_press = dismis_fonc)
		but_st.add_padd((.1,1))
		but_st.add_button("Imprimer",text_color =self.sc.text_col3,
			bg_color = self.sc.green,size_hint = (.2,1),on_press = accept_fonc)
		Edit_surf.add_surf(but_st)
		self.popup = Popup(title=self.titre,content = Edit_surf,
			size_hint = (.35,.3))
		self.popup.open()

class Fiche(Resumer_imp):
	@Cache_error
	def Create_fact(self,wid_l,entete,liste,titre,info,total_ent):
		self.wid_l = list(wid_l)
		self.entete = list(entete)
		self.liste = list(liste)
		self.titre = titre
		self.info = info
		self.total_ent = list(total_ent)

		self.Fact_POPUP()

	@Cache_error
	def Fact_POPUP(self,*args):
		h = .15
		Edit_surf = stack(self,bg_color = self.sc.aff_col1)
		Edit_surf.add_text('Forme du document ',size_hint = (.3,h),
			text_color = self.sc.text_col1,
			padding_left = dp(10))

		but_st = stack(self,size_hint = (1,h),
			spacing = dp(10))
		
		def dismis_fonc(*a):
			self.popup.dismiss()

		def chang_typ(info):
			self.forma = info

		def accept_fonc(*a):
			if self.forma:
				obj = Th_Fiche(self,self.titre,self.info,self.forma)
				obj.Create(self.wid_l,self.entete,self.liste,self.total_ent)
				self.popup.dismiss()
			else:
				self.sc.add_refused_error('Le choix du forma est impératif !')

		Edit_surf.add_surf(liste_set(self,self.forma,self.forma_liste,
			size_hint = (.2,h),mult = 3,mother_fonc = chang_typ))
		Edit_surf.add_padd((1,h*4))
		but_st.add_padd((.4,1))
		but_st.add_button("Annuler",text_color = self.sc.text_col3,
			bg_color = self.sc.red,size_hint = (.2,1),on_press = dismis_fonc)
		but_st.add_padd((.1,1))
		but_st.add_button("Imprimer",text_color =self.sc.text_col3,
			bg_color = self.sc.green,size_hint = (.2,1),on_press = accept_fonc)
		Edit_surf.add_surf(but_st)
		self.popup = Popup(title=self.titre,content = Edit_surf,
			size_hint = (.35,.3))
		self.popup.open()


#"""