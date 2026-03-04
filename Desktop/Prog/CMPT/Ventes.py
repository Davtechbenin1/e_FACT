#Coding:utf-8
from .old import *

class Ventes(box):
	def __init__(self,mother,**kwargs):
		kwargs['spacing'] = dp(10)
		kwargs["radius"] = dp(10)
		box.__init__(self,mother,**kwargs)
		if self.mother.access_dic == "all":
			self.access_liste = "all"
		else:
			self.access_liste = self.mother.access_dic.get('Comptoire')
		
		self.this_part = str()
		
		self.details_surf = Finalisation_surf(self,
			size_hint = (.35,1),radius = dp(10),
			bg_color = self.sc.aff_col1,spacing = dp(10),
			)
		self.V_SSSS = vente_article(self,size_hint = (.65,1),
			bg_color = self.sc.aff_col1,spacing = dp(10),
			radius = dp(10),padding = dp(10))

		self.size_pos()

	@Cache_error
	def check_access(self,access):
		if self.access_liste == "all":
			return True
		else:
			if access in self.access_liste:
				return True
			else:
				return False

	def reinit(self,*args):
		self.size_pos()
		self.add_all()

	@Cache_error
	def Foreign_surf(self):
		self.add_corps_surf()

	@Cache_error
	def size_pos(self):
		w,h = self.entete_size = 1,.035
		self.corps_size = w,1-h

		self.corps_surf = box(self,size_hint = self.corps_size,
			spacing = dp(10),radius = dp(10),
			bg_color = self.sc.gris,
			orientation = 'horizontal')

		self.add_surf(self.corps_surf)

	def add_corps_surf(self):
		self.corps_surf.clear_widgets()
		T = time.time()
		self.vente_surf = self.V_SSSS
		self.vente_surf.add_all()

		self.corps_surf.add_surf(self.vente_surf)
		self.corps_surf.add_surf(self.details_surf)

# Gestion des actions des méthodes
	def show_part(self,wid):
		info = wid.info
		self.this_part = info
		self.add_entete_surf()

class Factures(box):
	@Cache_error
	def initialisation(self):
		self.padding = dp(2)
		self.spacing = dp(2)
		self.orientation = 'horizontal'
		self.size_pos()
		self.add_all()

	def size_pos(self):
		self.cmd_ident = str()
		self.vente_surf = developpe_compt(self,size_hint = (.6,1),
			bg_color = self.sc.aff_col1,spacing = dp(10),
			radius = dp(10),padding = dp(10))

		self.details_surf = Liste_cmds(self,
			size_hint = (.4,1),
			bg_color = self.sc.aff_col1,spacing = dp(10),
			radius = dp(10))
		self.details_surf.add_all()

	@Cache_error
	def Foreign_surf(self):
		self.clear_widgets()
		if self.cmd_ident:
			self.vente_surf.cmd_ident = self.cmd_ident
			self.vente_surf.add_all()
			self.add_surf(self.vente_surf)
		else:
			self.details_surf.add_all()
			self.add_surf(self.details_surf)

class vente_article(stack):
	def initialisation(self):
		self.size_pos()

	@Cache_error
	def init(self):
		self.check_access = self.mother.check_access
		self.This_client = str()
		self.New_clt = False
		self.clt_dict = dict()
		self.magasin = "Général"
		self.search_infos = str()
		self.type_fact = "Comptant"
		self.lancer_imp = str()
		self.finition_srf = self.mother.details_surf
		self.type_fact_list = ['Comptant',"Credit ou devis"]
		self.corps_surf = Vente_surf(self,
			size_hint = (1,.86))

	def size_pos(self):
		self.init()
		self.add_input_clt_set()

		self.this_clt_info = stack(self,size_hint = (.5,.12),
			spacing = dp(5))
		self.magasin_surf = stack(self,size_hint = (.4,.12),
			spacing = dp(5))

		self.new_clt_surf = New_clt_Def(self,size_hint = (.6,.9),
			spacing = dp(5))

	@Cache_error
	def Foreign_surf(self):
		self.clt_liste = self.sc.DB.Get_clt_list()
		self.add_entet_surf()	

	@Cache_error
	def add_entet_surf(self,*args):
		t = time.time()
		self.clear_widgets()
		self.add_text('Client :',text_color = self.sc.text_col1,
			size_hint = (.08,.04))
		if not self.This_client:

			self.up_this_clt_surf()
			if self.New_clt:
				self.new_clt_surf.add_all()
				self.add_surf(self.new_clt_surf)
			else:
				self.add_input_clt_set()
				self.add_surf(self.input_clt_surf)
				if self.check_access('ajouter un client'):
					self.add_icon_but(icon = "account-plus",size_hint = (None,None),
						size = (dp(50),dp(35)),font_size = "43sp",
						text_color = self.sc.green,
						on_press = self.Add_new_clt)

		if self.This_client:
			self.clt_dict = self.sc.DB.Get_this_clt(self.This_client)
			self.add_this_clt_info()
			self.add_surf(self.this_clt_info)
			self.Up_magasin_surf()
			self.add_surf(self.magasin_surf)
			self.corps_surf.clt_type = self.clt_type
			self.corps_surf.add_all()
			self.add_surf(self.corps_surf)

	def set_pied_surf_P2(self):
		self.mother.details_surf.add_all()

	@Cache_error
	def Up_magasin_surf(self):
		self.magasin_surf.clear_widgets()
		self.magasin_surf.add_text("Magasin de déstockage :",
			text_color = self.sc.text_col1,
			size_hint = (.3,.4))
		self.magasin_surf.add_surf(liste_set(self,self.magasin,
			[self.magasin],size_hint = (.7,.4),
			mother_fonc = self.set_mag,mult = 1))
	
	@Cache_error
	def add_input_clt_set(self):
		self.input_clt_surf = box(self,size_hint = (.7,.5),
			spacing = dp(5))
		self.up_inp_surf = liste_deroulante(self,self.This_client,
			self.sc.DB.Get_clt_list(),orientation = "V",
			mult = 1,size_hint = (1,1),sub_mod = 1,
			mother_fonc = self.Set_clt,
			)

		self.input_clt_surf.add_input("Recherche",
			size_hint = (1,.08),on_text = self.set_search,
			bg_color = self.sc.aff_col3,placeholder = 'Recherche')
		self.input_clt_surf.add_surf(self.up_inp_surf)

	def up_this_clt_surf(self):
		t = time.time()
		liste = [i for i in self.clt_liste 
		if self.search_infos.lower() in i.lower()]
		self.up_inp_surf.list_info = liste
		self.up_inp_surf.add_all()

	@Cache_error
	def add_this_clt_info(self):
		self.this_clt_info.clear_widgets()
		if self.This_client:
			clt_d = self.sc.DB.Get_this_clt(self.This_client)
			clt_name = f"""{clt_d.get("nom")} {clt_d.get("prénom",str())}""".strip()
			sol = clt_d.get('solde')
			if not sol:
				sol = 0
			dic = {
				"Type :":clt_d.get('type'),
				"Solde :":self.format_val(sol),
				"Tel :":self.format_val(clt_d.get('tel')),
				"WHTSP :":self.format_val(clt_d.get('whatsapp')),
			}
			self.clt_type = clt_d.get('catégorie')
			self.this_clt_info.add_text(clt_name,text_color = self.sc.text_col1,
				size_hint = (.75,.3),font_size = '18sp')
			self.this_clt_info.add_icon_but(icon = "account-edit",
				on_press = self.modif_clt,text_color = self.sc.orange,
				size_hint = (None,None),size = (dp(50),dp(35)),font_size = '43sp')
			self.this_clt_info.add_padd((1,.00000000001))
			for k,v in dic.items():
				try:
					int(v)
				except:
					val = v
				else:
					val = self.format_val(v)
				self.this_clt_info.add_text_input(k,(.15,.3),
					(.35,.3),self.sc.text_col1,bg_color = self.sc.aff_col3,
					text_color = self.sc.text_col1,
					default_text = val,readonly = True)

# Méthode de gestion des actions
	def Fact_mode(self,wid):
		pass

	def Save_fact(self,wid):
		pass

	def set_imp_auto(self,info):
		self.lancer_imp = info

	def Set_mode_fact(self,info):
		self.type_fact = info
		self.set_pied_surf_P2()

	def modif_clt(self,wid):
		self.This_client = str()
		self.add_all()

	def set_mag(self,info):
		self.magasin = info
		self.corps_surf.magasin = self.magasin
		self.corps_surf.this_art = str()
		self.corps_surf.add_def_surf()

	def Set_clt(self,info):
		self.This_client = info
		self.add_entet_surf()

	def Add_new_clt(self,wid):
		self.New_clt = True
		self.add_entet_surf()

	def set_search(self,wid,val):
		self.search_infos = val
		self.up_this_clt_surf()
	
		
