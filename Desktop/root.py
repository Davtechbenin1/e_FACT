#Coding:utf-8
"""
	L'écran principale est un stack
"""
from lib.davbuild import *
from General_surf import *
import sys,time
from color import *
from kivy.core.window import Window
from .Prog.CMPT.Ventes import Ventes,Factures
from .Prog.CMPT.stock import stock
from .Prog.CLT.Clients import client_part
from .Prog.RH.Personnel import all_General
from .Prog.FOUR.Fournisseur import Fournisseur
from .Prog.CLT.Clients import G_client
from .Prog.PROF.Profile import *
from .Prog.PROF.Parametre import *
from .Prog.CREAN.Creances import Creances
from .Prog.ACC.Accueil import Accueil
from .Prog.TRES.Tresorerie_g import (Tress_general,Tresorerie,
	Creance_charger)
from .Prog.PART.Partenaires import Partenaires
from .Prog.PROF.Aide import Aide
from .Prog.ANN.Annalyse import Annalyse
from kivymd.uix.label import MDLabel
from .Prog.CMPT.trs_surf2 import *

class profile_show(box):
	def initialisation(self):
		self.padding = dp(1)
		self.This_user = self.sc.root.This_user
		img = self.This_user.get('img')
		nom_prenom = self.This_user.get('nom',str())+' '+self.This_user.get('prénom',str())
		if not img:
			img = 'media/logo.png'
		self.add_image(img,size_hint = (1,.6), 
			bg_color = self.sc.aff_col1)
		self.add_text(nom_prenom,size_hint = (1,.11),
			halign = "center",bold = True,italic = True,
			bg_color = self.sc.aff_col1)
		b = box(self,size_hint = (1,.18),
			orientation = "horizontal",
			bg_color = self.sc.aff_col1,
			padding = dp(10))
		b.add_button("Voir le profile",size_hint = (.5,1),
			on_press = self.show_profile,halign = 'center',
			bg_color = self.sc.green,text_color = self.sc.aff_col1,
			font_size = dp(10))
		b.add_icon_but(icon = "power",text_color = self.sc.red,
			size_hint = (None,1),size = (dp(30),1),
			font_size = "20sp",on_press = self.deconnexion)
		b.add_button("Déconnexion", text_color = self.sc.red,
			size_hint = (.5,1),on_press = self.deconnexion,
			halign = 'left',bg_color = self.sc.aff_col1)
		self.add_surf(b)

	def show_profile(self,wid):
		self.sc.root.dropdown.dismiss()
		srf = Profile(self,bg_color = self.sc.green)
		self._custum_surf(srf,"Profile")

	def _custum_surf(self,srf,info):
		self.mother._change_screen(info)
		srf.add_all()
		self.mother.main_surf.add_surf(srf)

	def deconnexion(self,wid):
		self.sc.root.dropdown.dismiss()
		self.mother.initialisation()
		self.sc.actions_wids = list()
		self.mother.Foreign_surf()

class root(box):
	@Cache_error
	def initialisation(self):
		self.init_all()

	@Cache_error
	def init_all(self,*args):
		self.sc.iniiii(self)

	def th_init(self):
		self.clear_widgets()
		My_ent = self.sc.DB.get_entreprise()
		self.nom_app = My_ent.get("sigle")
		self.size_pos()

	@Cache_error
	def size_pos(self):
		w,h = self.Menu_haut_size = 1,.045
		self.Aff_size = w,1-h

		self.menu_haut_surf = box(self,size_hint = self.Menu_haut_size,
			bg_color = self.sc.aff_col1,orientation = 'horizontal',
			padding_top = dp(5))
		
		self.Aff_surf = app_surf(self,size_hint = self.Aff_size,
			bg_color = self.sc.green)
		self.root = self.Aff_surf
		
		self.add_surf(self.menu_haut_surf)
		self.add_surf(self.Aff_surf)

		self.Aff_surf.add_all()
		self.This_user = self.Aff_surf.This_user
		
		self.rac_in_show = "accueil"

		self.add_prev_menu()

	@Cache_error
	def add_prev_menu(self):
		self.menu_haut_surf.clear_widgets()
		col = self.sc.red
		txt = "Mode OFFLINE activé"
		if self.sc.DB.connected:
			col = get_color_from_hex("#106A1D")
			txt = "Mode ONLINE STREAN activé"

		self.aff_menu = box(self,size_hint = (None,1),
			width = dp(450),orientation = 'horizontal')
		self.operateur = self.menu_haut_surf.add_text(txt, 
			text_color = col,
			padding_left = dp(50),font_size = "15sp",
			bold = True, italic = True)
		self.clock_surf = self.menu_haut_surf.add_text(
			self.sc.get_now(),
			text_color = self.sc.menu_txt_col)

		Clock.schedule_interval(self.update_clock,1)

	@Cache_error
	def add_menu_haut(self,*args):
		self.add_prev_menu()
		
		lis = [
			("home",(0.18, 0.55, 0.95, 1),"accueil",
				'accueil'),
			("bank",(0.18, 0.70, 0.44, 1),'entreprise',
				'entreprise'),
			('cog-outline',(0.55, 0.55, 0.55, 1),'upgrade',
				"upgrade"),
			("help",(1.00, 0.76, 0.03, 1),"aide","aide")
		]
		self.th_rac_dic = {}
		for tup in lis:
			icon,col,txt,info = tup
			bold = False
			f_s = '12sp'
			if self.rac_in_show == info:
				bold = True
				f_s = '12sp'

			b = box(self,size_hint = (None,1),
				width = dp(75))
			self.menu_haut_surf.add_surf(b)
			b.add_icon_but(icon=icon,
				size_hint = (1,.6),
				text_color = col,
				font_size = "20sp",
				on_press = self.action_but,info = info)
			but_srf = b.add_button(txt,font_size = f_s,
				size_hint = (1,.4),on_press = self.action_but,
				info = info,text_color = self.sc.text_col1,
				bold = bold)
			self.th_rac_dic[info] = but_srf

			Clock.schedule_interval(self.update_clock,1)

	def set_th_bold_of(self,info):
		try:
			for th_w in self.th_rac_dic.values():
				th_w.bold = False
			if info in self.th_rac_dic:
				self.th_rac_dic.get(info).bold = True
		except:
			pass

	def update_clock(self,*args):
		txt = self.sc.get_now()
		txt = txt.replace("-",'/')
		txt = txt.replace(". ",'    ')
		self.clock_surf.text = txt

# Gestion des actions des bouttons
	def action_but(self,wid):
		self.th_wid = wid
		if wid.info != 'aide':
			self.rac_in_show = wid.info
		#Clock.schedule_once(self.add_menu_haut,.01)
		self.set_th_bold_of(wid.info)
		self._action_but_(wid.info)

	def _action_but_(self,info):
		if info.lower() == "accueil":
			th_srf = self.app_used.get(info)
			if not th_srf:
				th_srf = Accueil(self,radius = [dp(20),
					dp(20),0,0],bg_color = self.sc.aff_col1)
				self.app_used[info] = th_srf
			else:
				th_srf.add_all()
			self._custum_surf(th_srf,info)

		elif info.lower() == 'stop':
			th_srf = self.app_used.get(info)
			if not th_srf:
				th_srf = profile_show(self.Aff_surf,bg_color = self.sc.sep,
				size_hint = (1,None),height = dp(300))
				self.app_used[info] = th_srf
			else:
				th_srf.add_all()
			
			self.dropdown = modal_list(auto_width = False,width = dp(300),
				)
			self.dropdown.add_widget(th_srf)
			self.dropdown.open(self.th_wid)

		elif info.lower() == "upgrade":
			th_srf = self.app_used.get(info)
			if not th_srf:
				th_srf = autre_param(self,radius = dp(10),
				bg_color = self.sc.aff_col1)
				self.app_used[info] = th_srf
			else:
				th_srf.add_all()
			
			self._custum_surf(th_srf,info)

		elif info.lower() == "aide":
			webbrowser.open("https://www.youtube.com/@DavtechBenin")

		elif info.lower() == "entreprise":
			th_srf = self.app_used.get(info)
			if not th_srf:
				th_srf = Par_General(self,bg_color = self.sc.aff_col1,
				radius = dp(10))
				self.app_used[info] = th_srf
			else:
				th_srf.add_all()
			
			self._custum_surf(th_srf,info)

	def _custum_surf(self,srf,info):
		self.Aff_surf._change_screen(info)
		srf.padding = dp(10)
		srf.add_all()
		self.Aff_surf.main_surf.add_surf(srf)


class app_surf(box):
	def initialisation(self):
		self.spacing = dp(10)
		self.radius = dp(10)
		self.orientation = "horizontal"
		self.Sync_srf = LoadingView(self,
			th_text = "Synchronisation des données en cours...",
			bg_color = (1,1,1,1),
			overlay_color = (1,1,1,1))

		self.icon_dic = {
			"Factures & Créances":"finance",
			"Resources Humaines":"account-group-outline",
			"Clients":"account-cash",
			"Fournisseurs":"briefcase-account",
			"Partenaires":"handshake-outline",
			"Finances":"bank-check",
			"Analyse":"chart-bar",
			"Ventes":'file-document',
			"Stocks":'warehouse',
			"Encaissements":'cash-register',
			"e-MECEF":"invoice-text",
			"Dépenses":"cash-minus",
			"Historique financier":'history',
			"Trésorerie interne": "treasure-chest",
			"Gestion des documents":'file-document-edit-outline'
		}
		"""
		self.This_user = self.sc.DB.Get_DAVID()
		self.mother.This_user = self.This_user
		self.size_pos()
		#"""
		self.agence_list = ["Général"]
		self.agence = "Général"
		self.sc.magasin = self.agence
		self.menu_dict = dict()
		self.menu_in_action = str()
		self.Racc_surf = None
		self.This_user = dict()#self.sc.DB.Get_DAVID()
		self.local_param = ("Général","Admin","Admin")
		
		self.poste = str()
		self.username = str()
		self.this_pass = str()
		self.sep = 'DAVBUILDDAVIDO'
		if self.local_param:
			self.agence,self.poste,self.username = self.local_param#.split(self.sep)

		"""
		#self.sc.DB.Get_Agences()
		self.poste_list = self.sc.DB.Get_all_post_list()

		self.all_perso = self.sc.DB.Get_all_perso()
		
		if not self.all_perso:
			self.sc.DB.Save_personnel(self.sc.DB.Get_DAVID())
			self.sc.DB.Save_personnel(self.sc.DB.Get_Admin())
			self.all_perso = self.sc.DB.Get_all_perso()
		"""
		self.mother.app_used = dict()

	def Set_logi_part(self):
		this_dic = {
			"Accueil":Accueil,
			"Ventes":Ventes,
			"Stocks":stock,
			"Factures & Créances":Creances,
			#"Encaissements":encaiss_en_attente,
			"Dépenses":decaissement,
			"Clients":client_part,
			"Fournisseurs":Fournisseur,
			"Partenaires":Partenaires,
			"Resources Humaines":all_General,
			"Historique financier":desk_finance_histo,
			"Analyse":Annalyse,
			"e-MECEF":Normalisation,
			"Aide":Aide,
			"Trésorerie interne": show_details,
			"Gestion des documents":doc_sys
		}
		liste = ["Ventes","Stocks","Factures & Créances",
		"Trésorerie interne","Dépenses","Historique financier",
		"Clients","Fournisseurs",#"Resources Humaines",#"Analyse",
		"e-MECEF"]#,"Gestion des documents"]

		if self.sc.get_in_progress() < 0:
			liste = ["Ventes","Factures & Créances",
			"e-MECEF"]

		#poste = self.This_user.get('poste actuel')
		
		#self.sc.DB.Get_this_poste_access(poste)

		for i in liste:
			if self.sc.get_access(i):
				this_surf = this_dic.get(i)
				self.add_menu(i,this_surf)
		if not self.sc.DB.Get_ent_part('sigle'):
			self.menu_in_action = "entreprise"

	@Cache_error
	def Connexion_part(self):
		self.clear_widgets()
	
		inf_srf = float_l(self,size_hint = (1,1))
		inf_srf.add_image("media/acc2.png",
			keep_ratio = False)
		h = .07
		#"""
		col = self.sc.red
		if self.sc.DB.connected:
			col = get_color_from_hex("#106A1D")
		th_but = inf_srf.add_button("Continuer",
			on_press = self.valid_con,
			bg_color = col,
			font_size = '20sp',
			bold = True,
			text_color = self.sc.aff_col1,
			size_hint = (.3,h),
			pos_hint = (.35,.03))
		#"""
		#self.add_padd((.25,h))
		#self.sc.set_default_button(th_but)
		self.add_surf(inf_srf)
	
	@Cache_error
	def Foreign_surf(self):
		if self.sc.DB.get_inprogress():
			self.Sync_srf.show()
			self.excecute(self.show_app)
			#Clock.schedule_once(self.show_app,.1)
			#print("-----------------------------------------------")
		else:
			self.show_app_content()

	def show_app_content(self,*args):
		#self.sc.loading_srf.show()

		if self.This_user:
			self.th_t = time.time()
			self.add_all_surfs(True)
			if self.menu_in_action.lower() == "upgrade".lower():
				srf = self.mother.app_used.get(self.menu_in_action)
				if not srf:
					srf = Par_General(self,bg_color = self.sc.aff_col1,
						radius = dp(10))
					self.mother.app_used[self.menu_in_action] = srf
				else:
					srf.add_all()
				self.mother._custum_surf(srf,"upgrade")
			elif self.menu_in_action.lower() == "Upgrade".lower():
				srf = self.mother.app_used.get(self.menu_in_action)
				if not srf:
					srf = autre_param(self,radius = dp(10),
						bg_color = self.sc.aff_col1)
					self.mother.app_used[self.menu_in_action] = srf
				else:
					srf.add_all()
				self.mother._custum_surf(srf,"Upgrade")
			else:
				self.menu_in_action = "Accueil"
				srf = self.mother.app_used.get(self.menu_in_action)
				if not srf:
					srf = Accueil(self,radius = dp(10),
						bg_color = self.sc.aff_col1)
					self.mother.app_used[self.menu_in_action] = srf
				else:
					srf.add_all()
				self.mother._custum_surf(srf,"Accueil")
			#self.mother.titre.text = self.menu_in_action
		else:
			self.Connexion_part()
		#self.sc.loading_srf.hide()
		#My_ent = self.sc.DB.get_entreprise()

	def show_app(self,*args):
		while self.sc.DB.get_inprogress():
			time.sleep(.01)
			if self.sc.DB.connected == False:
				break
			
		Clock.schedule_once(self._show_th_app)

	def _show_th_app(self,*args):
		self.Sync_srf.hide()
		self.show_app_content()

	def add_menu(self,menu,surf):
		self.menu_dict[menu] = surf

	def size_pos(self):
		self.clear_widgets()
		if self.This_user:
			self.Set_logi_part()
		
		w,h = self.menu_size = .1,1
		self.surf_size = 1-w,1
		self.menu_color = self.sc.menu_color
		self.surf_color = self.sc.green
		self.menu_surf = stack(self,size_hint = self.menu_size,
			bg_color = self.sc.menu_color,radius = [dp(20),dp(20),dp(20),dp(20)],
			padding = dp(10),)
		self.main_surf = box(self,size_hint = self.surf_size,
			bg_color = self.surf_color,
			radius = dp(20),
			padding = dp(10))
		self.add_surf(self.menu_surf)
		self.add_surf(self.main_surf)

	@Cache_error
	def add_all_surfs(self,first = None):
		self.menu_surf.clear_widgets()
		self.main_surf.clear_widgets()
		H = (len(self.menu_dict) + 1)*dp(70)
		H += dp(60)
		for menu in self.menu_dict:
			bg_opact = 0
			txt_col = self.sc.aff_col1
			bg_color = None
			bg_col = self.sc.menu_color
			f_s = "20sp"
			f = '16sp'
			if self.menu_in_action == menu:
				bg_opact = 0
				txt_col = self.sc.green
				bg_col = self.sc.aff_col1
				f_s = "24sp"
				#f = '16sp'
			w = len(menu)*dp(10)

			b = box(self,size_hint = (1,None),height = dp(75),
				orientation = 'horizontal',
				radius = dp(20),bg_color = bg_col)
			ico = self.icon_dic.get(menu)
			if not ico:
				ico = str()
			b.add_icon_but(icon = ico,info = menu,
				text_color = txt_col,font_size = f_s,radius = dp(5),
				size_hint = (.2,1),
				on_press = self.Change_screen,
				)
			b.add_button(menu,text_color = txt_col,bg_color = None,
				size_hint = (.8,1),info = menu,halign = 'left',
				font_size = f,on_press = self.Change_screen)
			
			self.menu_surf.add_surf(b)
		if not first:
			Clock.schedule_once(self.set_prt)
			
	def set_prt(self,dt):
		self.but_part = box(self,orientation = 'horizontal',
			)
		srf = self.menu_dict.get(self.menu_in_action)
		if srf:
			surf = self.mother.app_used.get(self.menu_in_action)
			if not surf:
				surf = srf(self,bg_color = self.sc.aff_col1,
					radius = dp(10))
				self.mother.app_used[self.menu_in_action] = surf

			#if self.sc.get_profile_perso() in self.sc.get_all_charger():
			#	surf = Creance_charger(self)
			if surf:
				surf.add_all()
				self.main_surf.add_surf(surf)

	def Get_mot_pas(self):
		for name,dic in self.all_perso.items():
			if dic.get('username') == self.username:
				return dic.get('mot de pass'),name
			elif dic.get('email') == self.username:
				return dic.get('mot de pass'),name
		return False

# Gestion des actions des bouttons
	def deconnexion(self,wid):
		self.initialisation()
		self.sc.actions_wids = list()
		self.Foreign_surf()

	def def_poste(self,info):
		if self.poste:
			self.poste = str()
		else:
			self.poste = info

	def valid_con(self,wid):
		"""
		if not self.sc.magasin:
			self.sc.add_refused_error("Le magasin est obligatoire !")
		else:
			this_pass = self.Get_mot_pas()
			if not this_pass:
				self.sc.add_refused_error("Le nom d'utilisateur est incorrecte")
			else:
				if self.this_pass == this_pass[0]:
					self.This_user = self.sc.DB.Get_this_perso(this_pass[1])
					self.mother.This_user = self.This_user
					if not self.poste:
						self.poste = "Admin"
					infos = f"{self.agence}{self.sep}{self.poste}{self.sep}{self.username}"
					self.sc.DB.Save_local("param",infos)
					self.size_pos()
					self.add_all()
					self.mother.add_menu_haut()
					self.mother.operateur.text = f"Opérateur:   [b][i]{self.This_user.get('nom')} {self.This_user.get('prénom')}[/i][/b]"
				else:
					self.sc.add_refused_error("Le mot de pass est incorrecte")
		"""
		#self.sc.loading_srf.show()
		Clock.schedule_once(self._valid_con_,.1)

	def _valid_con_(self,*args):
		self.This_user = {"nom":"ZoeCorpUser",
			"prénom":'','poste':"Admin"} #self.sc.DB.Get_this_perso(self.TH_TH_paa[1])
		self.mother.This_user = self.This_user
		"""
		if not self.poste:
			self.poste = "Admin"
		infos = f"{self.agence}{self.sep}{self.poste}{self.sep}{self.username}"
		self.sc.DB.Save_local("param",infos)
		t = time.time(,"root")
		"""
		self.size_pos()
		self.add_all()
		self.mother.add_menu_haut()
		#self.sc.loading_srf.hide()

	def set_info(self,wid,val):
		if wid.info == 'username':
			self.username = val
		elif wid.info == "password":
			self.this_pass = val

	def def_agence(self,info):
		self.agence = info
		self.sc.magasin = info

		self.excecute(self.sc.DB.Save_local,
			"Magasin",self.sc.magasin)
		#self.sc.DB.Save_local("Magasin",self.sc.magasin)

	@Cache_error
	def Change_screen(self,value):
		self.sc.actions_wids = list()
		self._change_screen(value.info)

	def _change_screen(self,info):
		self.mother.set_th_bold_of(info)
		txt = str()
		self.menu_in_action = info
		if not self.sc.DB.Get_ent_part("sigle"):
			self.menu_in_action = "entreprise"
			txt = 'Vous dévez définir les informations de votre entreprise avant de continuer'
		self.add_all_surfs()
		try:
			self.mother.modal.dismiss()
		except:
			...
		#self.mother.titre.text = self.menu_in_action
		if txt:
			self.sc.add_refused_error(txt)

class default(box):
	def Another_event(self,*args):
		self.add_all()

	def Foreign_surf(self):
		self.add_text('Not yet set',text_color = self.sc.text_col1,
			halign = "center",font_size = '15sp')







		