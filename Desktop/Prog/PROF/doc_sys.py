#Coding:utf-8
"""
	Paramètre de gestion des documents de gestion
"""
from lib.davbuild import *
from General_surf import *

class doc_sys(box):
	def initialisation(self):
		self.doc_dic = self.sc.DB.get_all_doc()
		self.th_type = str()
		self.th_base = str()
		self.size_pos()

	def size_pos(self):
		self.entete_surf = stack(self,size_hint = (1,.05),
			padding = dp(10), spacing = dp(10))
		self.liste_surf = stack(self,size_hint = (1,None),
			padding = dp(10), spacing = dp(10))
		sr = scroll(self,size_hint = (1,.95),
			bg_color = self.sc.aff_col1)
		self.add_surf(self.entete_surf)
		self.add_surf(sr)
		sr.add_surf(self.liste_surf)

	def Foreign_surf(self):
		self.add_entete_surf()
		self.Up_liste_surf()

	def add_entete_surf(self):
		self.entete_surf.clear_widgets()
		self.entete_surf.add_text("Trier par type de document:",
			text_color = self.sc.text_col1,size_hint = (.15,1))
		self.entete_surf.add_surf(liste_set(self,self.th_type,("Word", "Excel"),
			size_hint = (.1,1),mother_fonc = self.set_th_type))

		self.entete_surf.add_text("Trier par type de document:",
			text_color = self.sc.text_col1,size_hint = (.15,1))
		self.entete_surf.add_surf(liste_set(self,self.th_base,self.sc.DB.get_all_doc_base(),
			size_hint = (.1,1),mother_fonc = self.set_th_base))

		self.entete_surf.add_icon_but(icon = 'plus',size_hint = (None,1),
			size = (dp(30),dp(1)),text_color = self.sc.green)
		self.entete_surf.add_button("Nouveau document",size_hint = (.15,1),
			text_color = self.sc.green,bg_color = None,
			halign = 'left',on_press = self.set_new_doc)

	def Up_liste_surf(self):
		self.liste_surf.clear_widgets()
		liste = map(self.trie_doc_info,self.doc_dic.values())
		for dic in liste:
			if dic:
				self.Add_infos(dic)
		self.Add_infos(None)

	def Add_infos(self,dic):
		if dic:
			fl = float_l(self,size_hint = (.12,None),
				)
			imag = box(self,
				padding = [dp(10),dp(10),dp(10),dp(2)],
				radius = dp(10),bg_color = self.sc.aff_col3)
			imag.add_image(dic.get('modèle_img',"media/logo.png"),
				keep_ratio = False,size_hint = (1,.8))
			imag.add_text(dic.get('nom'),text_color = self.sc.text_col1,
				size_hint = (1,.2),
				shorten = False,strip = False)
			fl.add_surf(imag)
			fl.add_button("",on_press = self.develop_image,
				info = dic.get('nom'),bg_color = None)
			self.liste_surf.add_surf(fl)
			fl.height = dp(130)
		else:
			fl = float_l(self,size_hint = (.12,None),)
			imag = box(self,
				padding = [dp(10),dp(10),dp(10),dp(2)],
				radius = dp(10),bg_color = self.sc.aff_col3)
			imag.add_icon_but(icon = 'plus',font_size = "30sp",
				size_hint = (1,.5),text_color = self.sc.white,
				on_press = self.set_new_doc)
			imag.add_button("Nouveau modèle",text_color = self.sc.orange,
				size_hint = (1,.5),font_size = '18sp',italic = True,
				bg_color = None,on_press = self.set_new_doc)
			fl.add_surf(imag)
			self.liste_surf.add_surf(fl)
			fl.height = dp(130)

	def trie_doc_info(self,dic):
		if self.th_name.lower() not in dic.get("nom").lower():
			return False
		if self.th_base:
			if dic.get('base').lower() != self.th_base.lower():
				return None
		if self.th_type:
			if dic.get('type').lower() != self.th_type.lower():
				return None
		return dic



# Gestion des actions des bouttons
	def set_th_type(self,info):
		self.th_type = info
		self.Up_liste_surf()

	def set_th_base(self,info):
		self.th_base = info
		self.Up_liste_surf()

	def develop_image(self,wid):
		...

	def set_new_doc(self,wid):
		srf = New_doc_setting(self)
		srf.add_all()



class New_doc_setting(box):
	def initialisation(self):
		self.th_doc_format = self.sc.DB.doc_format()
		self.base_liste = (
			"Client","Personel",'Commandes','Comptes de trésorerie',
			"Encaissements","Décaissements",'stocks'
		)
		self.modal = None

	@Cache_error
	def Foreign_surf(self):
		if self.modal:
			self.modal.dismiss()


		if not self.th_doc_format.get('nom'):
			self.set_name()
		elif not self.th_doc_format.get('type'):
			self.add_doc_type()
		elif not self.th_doc_format.get('base'):
			self.add_doc_base()

	def set_name(self):
		b = box(self,bg_color = self.sc.aff_col1,
			radius = dp(10),spacing = dp(10),padding = dp(10))
		b.add_text("",size_hint = (1,.2))
		b.add_text("Le nom du document",text_color = self.sc.orange,
			halign = 'center', font_size = '18sp',italic = True,
			size_hint = (1,None),height = dp(50))
		b1 = box(self,size_hint = (.7,.12),padding = dp(5),
			radius = dp(10),bg_color = self.sc.aff_col3,
			)
		b1 = Get_border_surf(b,b1,self.sc.green,pos_hint = (.15,0))
		b1.add_input("nom",on_text = self.set_info,
			bg_color = self.sc.aff_col3,
			text_color = self.sc.text_col1)
		b.add_button('Continuer',on_press = self.next_page,
			size_hint = (.4,.12),
			pos_hint = (.3,0),bg_color = self.sc.green,
			text_color = self.sc.white)
		b.add_text("",size_hint = (1,.2))

		self.add_modal_surf(b,size_hint = (.3,.4),
			titre = 'Le nom de votre document')

	def add_doc_type(self):
		b = stack(self,bg_color = self.sc.aff_col1,
			radius = dp(10),spacing = dp(10),padding = dp(10))
		b.add_padd((1,.3))
		b.add_text("Le type de document",text_color = self.sc.orange,
			halign = 'center', font_size = '18sp',italic = True,
			size_hint = (.4,.12))
		
		b.add_surf(liste_set(self,self.th_doc_format.get('type'), 
			['Word','Excel'],mother_fonc = self.set_type,
			size_hint = (.6,.12)))
		b.add_padd((.3,.12))
		b.add_button('Continuer',on_press = self.next_page,
			size_hint = (.4,.12),
			pos_hint = (.3,0),bg_color = self.sc.green,
			text_color = self.sc.white)

		self.add_modal_surf(b,size_hint = (.3,.4),
			titre = 'Le type de votre document (Word ou Excel)')

	def add_doc_base(self):
		b = stack(self,bg_color = self.sc.aff_col1,
			radius = dp(10),spacing = dp(10),padding = dp(10))
		b.add_padd((1,.3))
		b.add_text("La base concernée",text_color = self.sc.orange,
			halign = 'center', font_size = '18sp',italic = True,
			size_hint = (.4,.12))
		
		b.add_surf(liste_set(self,self.th_doc_format.get('base'), 
			self.base_liste,mother_fonc = self.set_base,
			size_hint = (.6,.12)))

		b.add_padd((.3,.12))
		b.add_button('Continuer',on_press = self.next_page,
			size_hint = (.4,.12),
			pos_hint = (.3,0),bg_color = self.sc.green,
			text_color = self.sc.white)

		self.add_modal_surf(b,size_hint = (.3,.4),
			titre = 'La base de données à utiliser')

	def add_attribut_setting(self):
		...


#Gestion des actions des bouttons
	def set_info(self,wid,val):
		self.th_doc_format[wid.info] = val

	def next_page(self,wid):
		self.add_all()

	def set_type(self,info):
		self.th_doc_format["type"] = info

	def set_base(self,info):
		self.th_doc_format['base'] = info

class attribut_set(stack):
	def initialisation(self):
		self.th_doc_format = self.mother.th_doc_format
		self.base_of = {
			"Client":None
		}
		self.base_dics = dict()

		self.curent_attr1 = str()
		self.curent_attr2 = str()
		self.curent_attr3 = str()

		self.attr_1_develop = dict()
		self.attr_2_develop = dict()

		self.typ_curent_art = str()

		self.add_text('Surface de définition des attributs de génération',
			size_hint = (1,.07),halign = 'top',font_size = "18sp",
			text_color = self.sc.orange,italic = True)

		self.base_attribut_part = box(self,size_hint = (.5,.92),
			bg_color = self.sc.aff_col3,spacing = dp(3),
			padding = dp(10),radius = [dp(20),dp(0),dp(0),dp(20)])

		self.doc_attribut_part = box(self,size_hint = (.5,.92),
			bg_color = self.sc.aff_col1,spacing = dp(3),
			padding = dp(10),radius = [dp(0),dp(20),dp(20),dp(0)])

		self.add_surf(self.base_attribut_part)
		self.add_surf(self.doc_attribut_part)

	def add_base_attr_part(self):
		self.base_attribut_part.clear_widgets()
		self.base_attr1 = box(self,size_hint = (1,None),
			spacing = dp(10))
		self.base_attr2 = box(self,size_hint = (1,None),
			spacing = dp(10))
		self.base_attr3 = box(self,size_hint = (1,None),
			spacing = dp(10))

		src1 = scroll(self)
		src2 = scroll(self)
		src3 = scroll(self)

		src1.add_surf(self.base_attr1)
		src2.add_surf(self.base_attr2)
		src3.add_surf(self.base_attr3)

		self.base_attribut_part.add_surf(src1)
		self.base_attribut_part.add_surf(src2)
		self.base_attribut_part.add_surf(src3)

		self.add_base_attr1()
		self.add_base_attr2()
		self.add_base_attr3()

	def add_base_attr1(self):
		self.base_attr1.clear_widgets()
		attr_list = self.base_dics.keys()

		for attr in attr_list:
			col = self.sc.text_col1
			bg_col = None
			if attr.lower() == self.curent_attr1.lower():
				bg_col = self.sc.green
				col = self.sc.text_col1

			self.base_attr1.add_button(attr,text_color = col,
				bg_color = bg_col,on_press = self.set_base_attr1)


	def start_setting_1(self):
		...



		



#Gestion des actions des bouttons
	def set_base_attr1(self,wid):
		self.curent_attr1 = wid.info
		self.add_base_attr1()
		self.start_setting_1()

	def set_typ_curent_art(self,info):
		self.typ_curent_art = info


class art_dev_set(box):
	def initialisation(self):
		self.curent_attr = self.mother.curent_set
		self.base_liste = self.mother.base_liste
		self.typ_curent_art = str()


	def Foreign_surf(self):
		h = .1
		self.add_text('',size_hint = (1,.1))
		self.add_text("type d'attribut",size_hint = (.35,h),
			text_color = self.sc.text_col1)
		self.add_surf(liste_set(self,self.typ_curent_art,
			("simple","develop"),size_hint = (.6,h),
			mother_fonc = self.set_typ_curent_art))

		if self.typ_curent_art.lower() == 'develop':
			self.add_text("type de base",size_hint = (.35,h),
				text_color = self.sc.text_col1)
			self.add_surf(liste_set(self,self.curent_art_base,
				self.base_liste,size_hint = (.6,h),
				mother_fonc = self.set_typ_curent_art))
			







