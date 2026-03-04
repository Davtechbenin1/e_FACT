#Coding:utf-8
from lib.davbuild import *
from General_surf import *
from .paie_surfs import decaisse_paie

class autre_montan_set(stack):
	@Cache_error
	def initialisation(self):
		self.mont_liste = {} #self.sc.DB.Get_autres_montants()
		self.spacing = dp(10)
		self.info_h = .18
		self.mont_select_list = list()
		self.autres_montant = dict()
		self.titre = str()
		self.mother_fonc = None

	def Foreign_surf(self):
		self.Set_autre_m()

	@Cache_error
	def Set_autre_m(self):
		self.clear_widgets()
		if self.titre:
			self.add_text(self.titre,text_color = self.sc.text_col1,
				size_hint = (1,None),height = dp(20),underline = True,
				halign = 'center')
		for mont in self.mont_liste:
			txt_col = self.sc.text_col1
			bg_col = self.sc.aff_col3
			read = True
			if mont in self.mont_select_list:
				txt_col = self.sc.green
				bg_col = self.sc.green
				read = False

			b = box(self,size_hint = (1,None),height = dp(45),
				orientation = 'horizontal',
				spacing = dp(10))
			b.add_button('',size_hint = (None,None),
				width = dp(20),height = dp(20),
				on_press = self.set_mont_sel,info = mont,
				bg_color = bg_col,radius = dp(10),pos_hint = (0,.25))
			b.add_button(mont,on_press = self.set_mont_sel,
				bg_color = None,text_color = txt_col,
				halign = 'left',size_hint = (.5,1))
			b.add_input(mont,text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,on_text = self.set_autre_mot,
				default_text = self.format_val(self.autres_montant.get(mont,0)),
				size_hint = (.4,1),readonly = read)
			b.add_text('',size_hint = (.1,1))
			self.add_surf(b)
		if not self.mont_liste:
			self.add_text('Aucun montants accessoires définie',
				text_color = self.sc.text_col1,halign = 'center',
				font_size = "18sp")

	def set_autre_mot(self,wid,info):
		wid.text = self.regul_input(wid.text)
		if wid.text:
			self.autres_montant[wid.info] = float(wid.text)
		else:
			self.autres_montant[wid.info] = float()
		self.mother.autres_montant = {i:self.autres_montant.get(i,float())
			for i in self.mont_select_list}
		if self.mother_fonc:
			self.mother_fonc(self)

	@Cache_error
	def set_mont_sel(self,wid):
		if wid.info not in self.mont_select_list:
			self.mont_select_list.append(wid.info)
		else:
			self.mont_select_list.remove(wid.info)
		self.mother.autres_montant = {i:self.autres_montant.get(i,float())
			for i in self.mont_select_list}
		if self.mother_fonc:
			self.mother_fonc(self)
		self.Set_autre_m()

class Decaissement_surf(stack):
	from .Save_infos_obj import (Fournisseur_save_decaisse,
		Partenaires_save_decaiss,Personnel_save_decaiss)
	@Cache_error
	def initialisation(self):
		self.padding = dp(10)
		self.spacing = dp(5)
		self.this_h = .05

		self.cate_dec = str()
		self.cate_dec_list = [i for i in self.sc.Get_charges()]
		self.motif = str()
		self.ref = str()

		self.ref_list = [i for i in self.sc.DB.Get_all_fiche_paie() if i]

		self.obj_decaisse = decaisse_paie(self,.09,
			' ',' ',None,modif_mont = True, size_hint = (1,.7),
			mother_fonc = self.Save_decai)
		self.add_all()

	@Cache_error
	def Foreign_surf(self):
		h = self.this_h
		self.clear_widgets()
		self.add_text("Règlement des charges de l'entreprise",
			size_hint = (1,h-.02),text_color = self.sc.text_col1,
			halign = "center")
		self.add_text('Catégorie de charges',size_hint = (.3,h),
			text_color = self.sc.text_col1)
		inp_obj = input_search_new(self,self.cate_dec,
			self.cate_dec_list, self.set_cat,size_hint = (.65,self.this_h))
		
		if self.cate_dec:
			self.add_text('Motif de décaissement',size_hint = (.3,h),
			text_color = self.sc.text_col1)
			motif_l = self.sc.Get_charges().get(self.cate_dec,list())
			inp_obj = input_search_new(self,self.motif,
				motif_l, self.set_motif,size_hint = (.65,self.this_h))
			
			if self.motif:
				self.obj_decaisse.motif = self.motif
				self.obj_decaisse.cate_benef = self.bene_t
				if self.motif == 'Salaires et traitements':
					self.add_text('Référence',text_color = self.sc.text_col1,
						size_hint = (.3,h))
					inp_obj = input_search_new(self,self.ref,self.ref_list,
						self.set_ref,size_hint = (.65,self.this_h))
					if self.ref:
						self.obj_decaisse.reference = self.ref
						self.obj_decaisse.add_all()
						self.add_surf(self.obj_decaisse)
				else:
					self.add_text_input('Référence',(.3,h),(.65,h),
						self.sc.text_col1,text_color = self.sc.text_col1,
						bg_color = self.sc.aff_col3,on_text = self.set_man_ref)
					self.obj_decaisse.reference = self.cate_dec
					self.obj_decaisse.add_all()
					self.add_surf(self.obj_decaisse)

# Gestion des actions des bouttons
	@Cache_error
	def Save_decai(self,wid):
		self.excecute(self.Personnel_save_decaiss,wid)
		#self.Personnel_save_decaiss(wid)
		if self.bene_t == 'Fournisseurs':
			self.excecute(self.Fournisseur_save_decaisse,wid)
			#self.Fournisseur_save_decaisse(wid)
		if self.bene_t == 'Partenaires':
			self.excecute(self.Partenaires_save_decaiss,wid)
			#self.Partenaires_save_decaiss(wid)
		self.cate_dec = str()
		self.motif = str()
		self.sc.add_refused_error('Décaissements prise en compte')
		self.mother.part2_surf.add_all()
		self.add_all()	

	def set_cat(self,info):
		self.cate_dec = info
		if self.cate_dec == "Achats consommés":
			self.bene_t = "Fournisseurs"
		elif self.cate_dec =="Charges du personnel":
			self.bene_t = "Personnel"
		elif self.cate_dec == "Services extérieurs":
			self.bene_t = "Autres"
		elif self.cate_dec == "Impôts et taxes":
			self.bene_t = 'Partenaires'
		elif self.cate_dec == "Charges diverses":
			self.bene_t = "Autres"
		self.motif = str()
		self.add_all()

	def set_motif(self,info):
		self.motif = info
		self.add_all()

	def set_ref(self,info):
		self.ref = info
		self.add_all()

	def set_man_ref(self,wid,val):
		self.ref = val
		self.obj_decaisse.reference = self.ref
