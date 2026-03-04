#Coding:utf-8
"""
	Gestion des surfaces pour la surface de paiement
"""
from lib.davbuild import *
from General_surf import *
from .fr_surf2 import Commandes
from ..CMPT.paie_surfs import decaisse_paie
from ..CMPT.general_obj2 import paie_fourni

class paiement_Surf(Commandes):
	@Cache_error
	def size_pos(self):
		self.clear_widgets()
		w,h = self.show_article_size = .4,1
		self.develop_size = 1-w,h

		self.show_cmd_surf = stack(self,size_hint = self.show_article_size,
			spacing = dp(5))
		self.develop_surf = Show_paie(self,size_hint = self.develop_size,
			spacing = dp(5),padding_left = dp(10),
			orientation = 'horizontal')
		self.add_surf(self.show_cmd_surf)
		self.add_text("",size_hint = (None,1),width = dp(1),
			bg_color = self.sc.text_col1)
		self.add_surf(self.develop_surf)

	@Cache_error
	def aff_cmds_surf(self):
		h = .045
		self.show_cmd_surf.clear_widgets()
		b = box(self,size_hint = (1,h),orientation = "horizontal",
			spacing = dp(5),padding_right = dp(10))
		b.add_text('Liste des Commandes',text_color = self.sc.text_col1,
			underline = True,halign = 'center')
		self.show_cmd_surf.add_surf(b)
		self.show_cmd_surf.add_surf(Periode_set(self,size_hint = (1,h),
			exc_fonc = self.Up_tab))
		self.show_cmd_surf.add_text('Satus commandes :',size_hint = (.35,h),
			text_color = self.sc.text_col1)
		self.show_cmd_surf.add_surf(liste_set(self,self.this_status,
			self.liste_status,size_hint = (.65,h),mult = 1,
			mother_fonc = self.Set_this_status))
		self.show_cmd_surf.add_text('Satus paiements :',size_hint = (.35,h),
			text_color = self.sc.text_col1)
		self.show_cmd_surf.add_surf(liste_set(self,self.this_paie,
			self.liste_paie,size_hint = (.65,h),mult = 1,
			mother_fonc = self.Set_this_paie))
		self.tab = Table(self,size_hint = (1,.78),
			bg_color = self.sc.aff_col3,exec_fonc = self.show_cmd,
			exec_key = 'N°')
		self.show_cmd_surf.add_surf(self.tab)
		self.Up_tab()

	def add_develop_surf(self):
		self.develop_surf.fact_dic = self.Fact
		self.develop_surf.add_all()

	def show_paiement(self,ident):
		self.recouv_to_developp = ident
		srf = paie_fourni(self,bg_color = self.sc.aff_col1,
			padding = dp(10),spacing = dp(5),radius = dp(10))
		self.clear_widgets()
		self.add_surf(srf)

	@Cache_error
	def add_paie_surf(self,wid):
		self.show_paiement(wid.info)

class Show_paie(box):
	@Cache_error
	def initialisation(self):
		self.fact_dic = dict()
		self.size_pos()
		self.add_all()

	@Cache_error
	def Foreign_surf(self):
		if self.fact_dic:
			#self.add_liste_surf()
			self.add_setting_surf()

	def size_pos(self):
		w,h = self.liste_size = .5,1
		self.setting_size = 1-w,h

		self.liste_surf = stack(self,size_hint = (1,1),
			spacing = dp(5),padding = dp(5))

		self.setting_surf = box(self,size_hint = (1,1))

		self.decais_surf = decaisse_paie(self,.06,"Reglement de fournisseur",
			self.fact_dic.get('fournisseur'),None,
			float(),spacing = dp(5),padding = dp(5),
			mother_fonc = self.add_fourn_paie,
			modif_mont = True)

	@Cache_error
	def add_liste_surf(self):
		h = .045
		self.clear_widgets()
		self.add_surf(self.liste_surf)
		self.liste_surf.clear_widgets()
		liste = self.fact_dic.get('paiements',list())
		self.liste_surf.add_text('Listes de paiements',text_color = self.sc.text_col1,
			halign = 'center',underline = True,size_hint = (.8,h))
		self.liste_surf.add_icon_but(icon = "close",on_press = self.set_new_pai,
			text_color = self.sc.red,size_hint = (.2,h))
		for ident in liste:
			self.liste_surf.add_button(ident,size_hint = (1,h),
				bg_color = None,text_color = self.sc.text_col1,
				on_press = self.mother.add_paie_surf,halign = 'left')

	@Cache_error
	def add_setting_surf(self):
		h = .035
		self.clear_widgets()
		self.add_surf(self.setting_surf)
		mont_T = self.fact_dic.get('montant TTC')
		mont_p = self.fact_dic.get('montant payé',float())
		txt1 = f"montant de la facture : {mont_T}"
		txt2 = f"montant total payé : {mont_p}"
		txt3 = f"Reste à payé : {mont_T - mont_p}"
		
		self.setting_surf.clear_widgets()
		b = stack(self,size_hint = (1,h))
		b.add_text("Enrégistrer un paiement fournisseur",
			text_color = self.sc.text_col1,halign = "center",
			size_hint = (.8,1),underline = True)
		b.add_icon_but(icon = 'history',on_press = self.set_hist,
			text_color = self.sc.black,size_hint = (.2,1))
		self.setting_surf.add_surf(b)
		if mont_p >= mont_T:
			self.setting_surf.add_text(f'Cette commande est déjà payé. \n{txt1}\n{txt2}\n{txt3}',
				text_color = self.sc.text_col1,font_size = "16sp",
				padding_left = dp(10),size_hint = (1,.3),valign = 'top')
		elif "écritures" in self.sc.DB.Get_access_of("Paiements Fournisseur"):
			lis = txt1,txt2,txt3
			for txt in lis:
				self.setting_surf.add_text(txt,size_hint = (1,h),
					text_color = self.sc.text_col1)
			self.decais_surf.cate_benef = 'Fournisseurs'
			four_id = self.fact_dic.get('fournisseur')
			four_dic = self.sc.DB.Get_this_fournisseur(four_id)
			self.decais_surf.benef = four_dic.get('nom')
			self.decais_surf.reference = self.fact_dic.get('N°')
			self.decais_surf.montant = mont_T - mont_p
			self.decais_surf.init()
			self.setting_surf.add_surf(self.decais_surf)
		else:
			self.setting_surf.add_text('')
			self.sc.add_refused_error("Impossible de continuer à cause d'une restriction système !! Parlez-en à votre supérieur hiérachique")

# Gestion des actions des buttons
	def show_decaiss(self,wid):
		info = wid.info

	def set_hist(self,wid):
		self.add_liste_surf()

	def set_new_pai(self,wid):
		self.add_setting_surf()

	@Cache_error
	def add_fourn_paie(self,wid):
		ident = wid.this_decaiss_info.get('N°')
		mont = self.decais_surf.montant
		dic = self.sc.DB.Get_paiement_f_cmd()
		four_id = self.fact_dic.get('fournisseur')
		four_dic = self.sc.DB.Get_this_fournisseur(four_id)
		dic['ecrit ident'] = ident
		dic['montant'] = mont
		dic['commande associée'] = self.fact_dic.get('N°')
		dic['solde précédent'] = four_dic.get("solde")
		dic['fournisseur'] = four_id

		self.fact_dic["paiements"].append(dic.get('N°'))
		self.fact_dic['paiement recente'] = dic.get('N°')
		paie = self.fact_dic.get('montant payé',float())
		paie += float(mont)
		self.fact_dic["montant payé"] = paie
		self.fact_dic["status du paiement"] = 'Avancée'
		if paie >= self.fact_dic.get('montant TTC'):
			self.fact_dic["status du paiement"] = 'Soldée'

		solde = four_dic.get('solde')
		if not solde:
			solde = float()
		solde -= mont
		four_dic["solde"] = solde
		self.excecute(self._vv,dic,four_dic)
		self.sc.add_refused_error("Paiement prise en compte!")
		self.add_liste_surf()

	def _vv(self,dic,four_dic):
		self.sc.DB.Save_fourn_paie(dic)
		self.sc.DB.Save_fourn_cmd(self.fact_dic)
		self.sc.DB.Modif_fournisseur(four_dic)
