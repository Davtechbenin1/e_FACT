#Coding:utf-8
"""
	deuxieme module de définition des surfaces à utilisation
	générale.
"""
from lib.davbuild import *

class recouv_show(stack):
	def __init__(self,mother,**kwargs):
		stack.__init__(self,mother,**kwargs)
		self.size_pos()
		self.init(self.mother.recouv_to_developp)

	@Cache_error
	def init(self,ident):
		self.ident = ident
		self.paie_dict = dict()
		if self.ident:
			self.paie_dict = self.sc.DB.get_recette(
				self.ident)
			self.clt_dict = self.sc.DB.Get_this_clt(
				self.paie_dict.get('client'))
			self.cmd_dict = self.sc.DB.Get_this_cmd(
				self.paie_dict.get('id commande'))
		self.add_all()

	@Cache_error
	def size_pos(self):
		b = box(self,size_hint =(1,.04),orientation = 'horizontal')
		b.add_text(" ")
		b.add_icon_but(icon = "close",on_press = self.fermetture,
			text_color = self.sc.red,font_size = '24sp',size_hint = (None,None),
			size = (dp(30),dp(30)))
		self.add_surf(b)
		w,h = self.clt_size = (1,.48)
		w,h = self.cmd_size = (.5,.43)
		self.paie_size = 1-w,h
		self.bas_size = 1,.05

		self.clt_surf = stack(self,size_hint = self.clt_size,
			radius = dp(10),padding = dp(10),spacing = dp(10))

		self.cmd_surf = stack(self,size_hint = self.cmd_size,
			radius = dp(10),padding = dp(10),spacing = dp(10))

		self.paie_surf = stack(self,size_hint = self.paie_size,
			radius = dp(10),padding = dp(10),spacing = dp(10))

		self.bas_surf = stack(self,size_hint = self.bas_size,
			)

		self.add_surf(self.clt_surf)
		self.add_surf(self.cmd_surf)
		self.add_surf(self.paie_surf)
		self.add_surf(self.bas_surf)

	@Cache_error
	def Foreign_surf(self):
		if self.paie_dict:
			self.add_clt_surf()
			self.add_cmd_surf()
			self.add_paie_surf()
			self.add_bas_surf()

	def add_clt_surf(self):
		self.clt_surf.clear_widgets()
		img = self.clt_dict.get('img')
		self.clt_surf.add_padd((.9,.1))
		infos = {
			"type":self.clt_dict.get('type'),
			"catégorie":self.clt_dict.get('catégorie'),
			"contact":self.format_val(self.clt_dict.get('tel')),
			"IFU":self.clt_dict.get('IFU'),
			"Adresse":self.sc.DB.adresse_of(
				self.clt_dict.get('N°')),
		}
		self.imp_dic = infos
		self.clt_surf.add_image(img,size_hint = (.4,.9))
		second_P = stack(self,size_hint = (.6,.9),spacing = dp(10))
		second_P.add_text(self.clt_dict.get('nom'),size_hint = (1,.1),
			text_color = self.sc.text_col1,font_size = "18sp")
		for k,v in infos.items():
			second_P.add_text_input(k,(.3,.1),(.6,.1),
				self.sc.text_col1,text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,default_text = str(v),
				readonly = True)
		self.clt_surf.add_surf(second_P)

	def add_cmd_surf(self):
		self.cmd_surf.clear_widgets()
		ident = self.cmd_dict.get('id de la commande')
		self.cmd_surf.add_text(f'Commande associer : <{ident}>',
			text_color = self.sc.text_col1,halign = 'center',
			underline = True,font_size = "18sp",size_hint = (1,.1))
		a_mont = self.sc.DB.Get_autre_mont_of(self.cmd_dict)
		m_ttc = float(self.cmd_dict.get('montant TTC'))
		all_mont = m_ttc
		mont_p = self.cmd_dict.get('montant payé')
		infos = {
			"montant TTC":self.format_val(m_ttc),
			"autre montant":self.format_val(a_mont),
			"montant total":self.format_val(all_mont),
			"montant total payé":self.format_val(mont_p),
			"reste à payé":self.format_val(all_mont - mont_p)
		}
		self.imp_dic.update(infos)
		for k,v in infos.items():
			self.cmd_surf.add_text_input(k,(.4,.12),(.5,.12),
				self.sc.text_col1,text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,default_text = str(v),
				readonly = True)

	def add_paie_surf(self):
		self.paie_surf.clear_widgets()
		self.paie_surf.add_text(self.paie_dict.get('id du paiement'),
			text_color = self.sc.text_col1,font_size = '17sp',
			halign = 'center',size_hint = (1,.1))
		self.paie_surf.add_text(self.paie_dict.get('montant payé'),
			text_color = self.sc.text_col1,font_size = "20sp",
			size_hint = (.9,.12),bg_color = self.sc.aff_col3,
			halign = 'center',radius = dp(10))

		solde_p = self.paie_dict.get('solde précédent client',float())
		solde_a = solde_p - self.paie_dict.get('montant payé')
		infos = {
			"date du paiement":self.paie_dict.get('date de paiement'),
			"heure du paiement":self.paie_dict.get('heure de paiement'),
			"solde précédent":solde_p,
			"solde finale":solde_a,
			"pénalité":self.paie_dict.get('pénalité',float())
		}
		self.imp_dic.update(infos)
		for k,v in infos.items():
			try:
				float(v)
			except:
				pass
			else:
				v = self.format_val(v)
			if k == "pénalité":
				v = v+" %"
			self.paie_surf.add_text_input(k,(.4,.12),(.5,.12),
				self.sc.text_col1,text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,default_text = str(v),
				readonly = True)

	def add_bas_surf(self):
		self.bas_surf.clear_widgets()
		self.bas_surf.add_padd((.66,1))
		self.bas_surf.add_button('Imprimer',text_color = self.sc.text_col3,
			bg_color = self.sc.aff_col2,on_press = self.Impression,
			size_hint = (.2,1))

# Méthode de gestion des actions
	def Impression(self,wid):
		nom = self.sc.DB.Get_ent_part("sigle")
		tel = self.sc.DB.Get_ent_part("téléphone")
		wh = self.sc.DB.Get_ent_part("whatsapp")
		doc = DocxTemplate("static/model recus.docx")
		logo = InlineImage(doc, "media/logo.png", Cm(1))
		num = tel
		obj = self.sc.DB.get_entreprise()
		if wh:
			num += f" / {wh}"
		th_dic = {
			"logo":logo,
			"nom_entreprise":obj.get('sigle'),
			"num":num,
			"num_recu":self.paie_dict.get('N°'),
			"date_emission":self.imp_dic.get('date du paiement'),
			"heur_emission":self.imp_dic.get('heure du paiement'),
			"Objet_paiement":"Recouvrement de fond",
			"nom_client":self.clt_dict.get('nom').upper(),
			"tel_client":self.clt_dict.get('tel'),
			"mode_paie":self.paie_dict.get('mode de paiement'),
			"ref":self.paie_dict.get('objet de paiement'),
			"mont_pay":self.format_val(self.paie_dict.get('montant payé')),
			"mont_finale":self.format_val(self.imp_dic.get('solde finale')),
			"operateur":self.paie_dict.get('opérateur'),
			"deposant":self.paie_dict.get('déposant'),
		}
		
		doc.render(th_dic)
		try:
			doc.save(f"{self.paie_dict.get('N°')}.docx")
		except:
			self.sc.add_refused_error('Un fichier du même non est ouvert')
		self.open_link(f"{self.paie_dict.get('N°')}.docx")

	def Send_fact(self,wid):
		self.sc.add_refused_error('Reste à définir')

	def fermetture(self,wid):
		self.mother.recouv_to_developp = str()
		self.mother.clear_widgets()
		self.mother.size_pos()
		self.mother.add_all()

class paie_show(recouv_show):
	def fermetture(self,wid):
		self.mother.close_modal()

class encaiss_show(recouv_show):
	def __init__(self,mother,**kwargs):
		stack.__init__(self,mother,**kwargs)
		self.size_pos()
		self.init(self.mother.recouv_to_developp)

	def init(self,ident):
		self.ident = ident
		if self.ident:
			self.paie_dict = self.sc.DB.Get_this_encaissement(
				self.ident)
			if self.paie_dict:
				self.clt_dict = self.sc.DB.Get_this_clt(
					self.paie_dict.get('origine'))
				self.cmd_dict = self.sc.DB.Get_this_cmd(
					self.paie_dict.get('référence'))
				self.add_all()

	@Cache_error
	def add_paie_surf(self):
		self.heure = self.mother.mouvement.get('heure')
		mouv_ident = self.mother.mouvement.get("N°")

		paie_asso = self.Get_paie_asso()
		mont_pay = self.paie_dict.get('montant encaissé')
		self.paie_surf.clear_widgets()
		self.paie_surf.add_text(mouv_ident,
			text_color = self.sc.text_col1,font_size = '17sp',
			halign = 'center',size_hint = (1,.1))
		self.paie_surf.add_text(f"Montant encaissé: {self.format_val(mont_pay)}",
			text_color = self.sc.text_col1,font_size = "20sp",
			size_hint = (.9,.12),bg_color = self.sc.aff_col3,
			halign = 'center',radius = dp(10))
		solde_p = paie_asso.get("solde précédent client")
		solde_f = solde_p - mont_pay

		infos = {
			"date du paiement":self.paie_dict.get('date'),
			"heure du paiement":self.heure,
			"motif":self.paie_dict.get("motif d'encaissements"),
			"solde initial client":solde_p,
			"solde final client":solde_f,
		}
		self.imp_dic.update(infos)
		for k,v in infos.items():
			try:
				float(v)
			except:
				pass
			else:
				v = self.format_val(v)
			
			self.paie_surf.add_text_input(k,(.4,.12),(.5,.12),
				self.sc.text_col1,text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,default_text = str(v),
				readonly = True)

	def compare_heur(self,heur1,heur2):
		if heur1 and heur2:
			H_l1 = heur1.split(":")
			if len(H_l1) == 3:
				H_l2 = heur2.split(":")
				if len(H_l2) == 3:
					H1 = str()
					for i in H_l1:
						if len(i) == 1:
							i = "0"+i
						H1 += i
					H2 = str()
					for j in H_l2:
						if len(j) == 1:
							j = "0"+j
						H2 += j
					if abs(int(H1)-int(H2)) <= 3:
						return True
		return False

	@Cache_error
	def Get_paie_asso(self):
		date = self.paie_dict.get('date')
		paie_liste = list()
		for info in self.clt_dict.get('paiements'):
			if date in info:
				paie_d = self.sc.DB.Get_this_paie_info(info)
				if paie_d:
					if paie_d.get('montant payé') == self.paie_dict.get('montant encaissé'):
						heure = paie_d.get('heure de paiement')
						if self.compare_heur(heure,self.heure):
							return paie_d
		return dict()

	@Cache_error
	def add_bas_surf(self):
		self.bas_surf.clear_widgets()
		self.bas_surf.add_padd((.066,1))
		self.bas_surf.add_button('Imprimer',text_color = self.sc.text_col1,
			bg_color = self.sc.green,on_press = self.Impression,
			size_hint = (.4,1))
		self.bas_surf.add_padd((.066,1))
		self.bas_surf.add_button('Révoquer',text_color = self.sc.text_col1,
			bg_color = self.sc.red,on_press = self.Revoque,
			size_hint = (.4,1))

# Gestion des actions des bouttons
	def Revoque(self,wid):
		self.sc.add_refused_error("Pour revoquer un récouvrement, il faut identifier la commande et le paiement associée au niveau du plan de paiement puis enrégistrer un paiements négatif au montant.!")

	@Cache_error
	def Impression(self,wid):
		tel = self.sc.DB.Get_ent_part("téléphone")
		wh = self.sc.DB.Get_ent_part("whatsapp")
		doc = DocxTemplate("static/model recus.docx")
		logo = InlineImage(doc, "media/logo.png", Cm(1))
		num = tel
		decais = self.paie_dict.get("N°")
		obj = self.sc.DB.get_entreprise()
		if wh:
			num += f" / {wh}"
		th_dic = {
			"logo":logo,
			"nom_entreprise":obj.get('sigle'),
			"num":num,
			"num_recu":decais,
			"date_emission":self.imp_dic.get('date du paiement'),
			"heur_emission":self.imp_dic.get('heure du paiement'),
			"Objet_paiement":self.paie_dict.get("motif d'encaissements"),
			"nom_client":self.clt_dict.get('nom').upper(),
			"tel_client":self.format_val(self.clt_dict.get('tel')),
			"mode_paie":self.paie_dict.get("mode d'entrée"),
			"ref":self.paie_dict.get('référence'),
			"mont_pay":self.format_val(self.paie_dict.get('montant encaissé')),
			"mont_finale":self.format_val(self.imp_dic.get('solde final client')),
			"operateur":self.paie_dict.get('opérateur'),
			"deposant":self.mother.mouvement.get('déposant',"Lui Même"),
		}
		
		doc.render(th_dic)
		try:
			doc.save(f"{self.paie_dict.get('N°')}.docx")
		except:
			self.sc.add_refused_error('Un fichier du même non est ouvert')
		self.open_link(f"{self.paie_dict.get('N°')}.docx")

	@Cache_error
	def fermetture(self,wid):
		self.mother.close_modal()

class decaiss_show(stack):
	@Cache_error
	def initialisation(self):
		h = .1
		self.ident = self.mother.recouv_to_developp
		self.mouvement = self.mother.mouvement
		self.paie_dict = self.sc.DB.Get_this_decaissement(self.ident)
		self.add_text(self.ident,text_color = self.sc.text_col1,
			halign = 'center',font_size = "20sp",size_hint = (1,h))
		self.imp_dic = dict()
		dic = {
			"Date d'émission":self.paie_dict.get('date'),
			"Heure d'émission":self.mouvement.get('heure'),
			"Motif de décaissement":self.paie_dict.get('motif de décaissement'),
			"Qualité du bénéficiaire":self.paie_dict.get('type de bénéficiaires'),
			"Bénéficiaire":self.paie_dict.get('bénéficiaire'),
			"Opérateur":self.paie_dict.get('opérateur'),
		}

		self.imp_dic.update(dic)
		for k,v in dic.items():
			self.add_text_input(k,(.2,h),(.3,h),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				default_text = self.format_val(v),readonly = True)
		mont = self.paie_dict.get('montant décaissé')
		b = box(self,size_hint = (.6,h*2.5),padding = dp(10),radius = dp(10),
			bg_color = self.sc.aff_col3)
		b.add_text("Montant décaissé",halign = "center",text_color = self.sc.text_col1,
			font_size = "17sp")
		b.add_text(self.format_val(mont),halign = "center",text_color = self.sc.black,
			font_size = "20sp")
		self.add_padd((.2,h))
		self.add_surf(b)
		self.add_padd((.2,h))
		dic = {
			"Mode de sortie":self.paie_dict.get('mode de sortie'),
			"Mode de reception":self.paie_dict.get('mode de reception'),
		}

		self.imp_dic.update(dic)
		for k,v in dic.items():
			self.add_text_input(k,(.2,h),(.3,h),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col1,
				default_text = self.format_val(v),readonly = True)
		self.add_button_custom("Imprimer",self.Impression,
			text_color = self.sc.text_col1,size_hint = (.3,h),
			padd = (.133,h))
		self.add_button_custom("Révoquer",self.Revoque,
			text_color = self.sc.text_col1,size_hint = (.3,h),
			padd = (.133,h),bg_color = self.sc.red)

 # Gestion des actions des bouttons
	@Cache_error
	def Impression(self,wid):
		tel = self.sc.DB.Get_ent_part("téléphone")
		wh = self.sc.DB.Get_ent_part("whatsapp")
		doc = DocxTemplate("static/model decaiss.docx")
		logo = InlineImage(doc, "media/logo.png", Cm(1))
		num = tel
		decais = self.paie_dict.get("N°")
		obj = self.sc.DB.get_entreprise()
		if wh:
			num += f" / {wh}"
		th_dic = {
			"logo":logo,
			"nom_entreprise":obj.get('sigle'),
			"num":num,
			"num_recu":decais,

			"date_emission":self.imp_dic.get("Date d'émission"),
			"heur_emission":self.imp_dic.get("Heure d'émission"),
			"Objet_paiement":self.imp_dic.get('Motif de décaissement'),
			"nom_client":self.imp_dic.get('Bénéficiaire'),
			"tel_client":str(),
			"mode_paie":self.imp_dic.get('Mode de sortie'),
			"ref":self.paie_dict.get('référence'),
			"mont_pay":self.format_val(self.paie_dict.get('montant décaissé')),
			"mont_finale":"indéterminé",
			"operateur":self.paie_dict.get('opérateur'),
			"deposant":self.mother.mouvement.get('déposant',"Lui Même"),
		}
		
		doc.render(th_dic)
		try:
			doc.save(f"{self.paie_dict.get('N°')}.docx")
		except:
			self.sc.add_refused_error('Un fichier du même non est ouvert')

		self.mother.close_modal()
		self.open_link(f"{self.paie_dict.get('N°')}.docx")

	@Cache_error
	def Revoque(self,wid):
		self.mother.close_modal()
		self.sc.add_refused_error("Pour revoquer un décaissement, il faut enrégistrer un décaissement négatif!")

# ---------------------------
class paie_fourni(recouv_show):
	@Cache_error
	def init(self,ident):
		self.ident = ident
		if self.ident:
			self.paie_dict = self.sc.DB.Get_this_fourn_paie(
				self.ident)
			fourn_id = self.paie_dict.get('fournisseur')
			cmd_id = self.paie_dict.get('commande associée')
			self.clt_dict = self.sc.DB.Get_this_fournisseur(
				fourn_id)
			self.cmd_dict = self.sc.DB.Get_this_fourn_cmd(
				cmd_id)
		self.add_all()

	@Cache_error
	def size_pos(self):
		w,h = self.clt_size = (1,.5)
		w,h = self.cmd_size = (.5,.4)
		self.paie_size = 1-w,h
		self.bas_size = 1,.07

		self.clt_surf = stack(self,size_hint = self.clt_size,
			radius = dp(10),padding = dp(10),spacing = dp(10))

		self.cmd_surf = stack(self,size_hint = self.cmd_size,
			radius = dp(10),padding = dp(10),spacing = dp(10))

		self.paie_surf = stack(self,size_hint = self.paie_size,
			radius = dp(10),padding = dp(10),spacing = dp(10))

		self.bas_surf = stack(self,size_hint = self.bas_size,
			padding_bottom = dp(10))

		self.add_surf(self.clt_surf)
		self.add_surf(self.cmd_surf)
		self.add_surf(self.paie_surf)
		self.add_surf(self.bas_surf)

	@Cache_error
	def Foreign_surf(self):
		if self.ident:
			self.add_clt_surf()
			self.add_cmd_surf()
			self.add_paie_surf()
			self.add_bas_surf()

	def add_clt_surf(self):
		self.clt_surf.clear_widgets()
		img = self.clt_dict.get('img','media/logo.png')
		self.clt_surf.add_padd((.9,.1))
		self.clt_surf.add_button('',bg_color = self.sc.red,
			on_press = self.fermetture,size_hint = (None,None),
			height = dp(20),width = dp(20))
		infos = {
			"type de fournisseur":self.clt_dict.get('type de fournisseur'),
			"secteur d'activité":', '.join(self.clt_dict.get("secteur d'activité")),
			"contact":self.clt_dict.get('téléphone'),
			"IFU":self.clt_dict.get('IFU'),
			"Adresse":self.clt_dict.get('addresse'),
		}
		self.imp_dic = infos
		self.clt_surf.add_image(img,size_hint = (.5,.9))
		second_P = stack(self,size_hint = (.5,.9),spacing = dp(10))
		second_P.add_text(self.clt_dict.get('nom'),size_hint = (1,.1),
			text_color = self.sc.text_col1,font_size = "20sp")
		for k,v in infos.items():
			second_P.add_text_input(k,(.3,.1),(.6,.1),
				self.sc.text_col1,text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,default_text = str(v),
				readonly = True)
		self.clt_surf.add_surf(second_P)

	def add_cmd_surf(self):
		self.cmd_surf.clear_widgets()
		ident = self.paie_dict.get('N°')
		self.cmd_surf.add_text(f'Commande associer : <{ident}>',
			text_color = self.sc.text_col1,halign = 'center',
			underline = True,font_size = "18sp",size_hint = (1,.15))
		a_mont = self.sc.DB.Get_autre_mont_of(self.cmd_dict)
		m_ttc = float(self.cmd_dict.get('montant TTC'))-a_mont
		all_mont = m_ttc
		mont_p = self.cmd_dict.get('montant payé')
		infos = {
			"montant TTC":m_ttc,
			"autre montant":a_mont,
			"montant total":all_mont,
			"montant payé":mont_p,
			"reste à payé":all_mont - mont_p
		}
		self.imp_dic.update(infos)
		for k,v in infos.items():
			self.cmd_surf.add_text_input(k,(.3,.1),(.6,.1),
				self.sc.text_col1,text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,default_text = str(v),
				readonly = True)

	def add_paie_surf(self):
		self.paie_surf.clear_widgets()
		self.paie_surf.add_text(self.paie_dict.get('N°'),
			text_color = self.sc.text_col1,font_size = '17sp',
			halign = 'center',size_hint = (1,.1))
		self.paie_surf.add_text(self.paie_dict.get('montant'),
			text_color = self.sc.text_col1,font_size = "20sp",
			size_hint = (.9,.12),bg_color = self.sc.aff_col3,
			halign = 'center',radius = dp(10))
		solde_p = self.paie_dict.get('solde précédent',float())
		solde_a = (self.paie_dict.get('solde précédent',float()) - 
			self.paie_dict.get('montant'))
		infos = {
			"date du paiement":self.paie_dict.get('date'),
			"heure du paiement":self.paie_dict.get('heure',str()),
			"solde précédent":solde_p,
			"solde finale":solde_a,
		}
		self.imp_dic.update(infos)
		for k,v in infos.items():
			try:
				float(v)
			except:
				pass
			else:
				v = self.format_val(v)
			self.paie_surf.add_text_input(k,(.3,.1),(.6,.1),
				self.sc.text_col1,text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,default_text = str(v),
				readonly = True)

	@Cache_error
	def add_bas_surf(self):
		self.bas_surf.clear_widgets()
		self.bas_surf.add_padd((.066,1))
		self.bas_surf.add_button('Imprimer',text_color = self.sc.text_col3,
			bg_color = self.sc.aff_col2,on_press = self.Impression,
			size_hint = (.4,1))
		self.bas_surf.add_padd((.066,1))
		self.bas_surf.add_button('Envoyer',text_color = self.sc.text_col3,
			bg_color = self.sc.aff_col2,on_press = self.Send_fact,
			size_hint = (.4,1))

	@Cache_error
	def Impression(self,wid):
		tel = self.sc.DB.Get_ent_part("téléphone")
		wh = self.sc.DB.Get_ent_part("whatsapp")
		doc = DocxTemplate("static/model decaiss.docx")
		logo = InlineImage(doc, "media/logo.png", Cm(1))
		num = tel
		decais = self.paie_dict.get('ecrit ident')
		dec_obj = self.sc.DB.Get_this_decaissement(decais)
		obj = self.sc.DB.get_entreprise()
		if wh:
			num += f" / {wh}"
		th_dic = {
			"logo":logo,
			"nom_entreprise":obj.get('sigle'),
			"num":num,
			"num_recu":decais,
			"date_emission":self.imp_dic.get('date du paiement'),
			"heur_emission":self.imp_dic.get('heure du paiement'),
			"Objet_paiement":"Décaissement de fond",
			"nom_client":self.clt_dict.get('nom').upper(),
			"tel_client":self.clt_dict.get('téléphone'),
			"mode_paie":dec_obj.get('mode de sortie'),
			"ref":self.paie_dict.get('commande associée'),
			"mont_pay":self.format_val(self.paie_dict.get('montant')),
			"mont_finale":self.format_val(self.imp_dic.get('solde finale')),
			"operateur":dec_obj.get('opérateur'),
			"deposant":dec_obj.get('motif de décaissement'),
		}
		
		doc.render(th_dic)
		try:
			doc.save(f"{self.paie_dict.get('N°')}.docx")
		except:
			self.sc.add_refused_error('Un fichier du même non est ouvert')
		self.open_link(f"{self.paie_dict.get('N°')}.docx")

