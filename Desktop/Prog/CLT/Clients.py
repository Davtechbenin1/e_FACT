#Coding:utf-8
"""
Gestion complète des clients
"""
from lib.davbuild import *
from General_surf import *
from .clt_surf1 import *
from .clt_surf2 import *
from .clt_surf_use import *
from .association import association
from .clt_infos import *
from ..CMPT.old import New_clt_Def
from ...Model_acc import Model_acc

class client_part(box):
	@Cache_error
	def initialisation(self):
		self.orientation = 'horizontal'
		self.padding = dp(10)
		self.radius = dp(10)
		#self.spacing = dp(2)
		self.this_clt = str()
		self.this_date_dict = {
			"day1":self.sc.get_today(),
			"day2":self.sc.get_today(),
		}
		self.this_client = dict()
		self.trie_sur_p = False
		self.this_clt_name = str()

		self.status_clt = str()
		self.status_l = "Ordinaire",'Douteu','Litigieu'
		self.solde_clt = str()
		self.solde_l = "Normal","Négatif","Positif"
		self.size_pos()
		self.Init()

	@Cache_error
	def Init(self):
		self.th_typ = str()
		self.th_cate = str()
		self.th_name = str()
		self.th_association = list()
		self.New_clt = False
		self.New_dic = {
			"nom":str(),
			"IFU":str(),
			"pays":str(),
			"ville":str(),
			"quartier":str(),
			"email":str(),
			"téléphone":str(),
			"whatsapp":str(),
			"nom directeur":str(),
			"tél directeur":str(),
			"solde à la création":'0',
		}
		self.perso_cont = dict()

	def size_pos(self):
		w,h = self.liste_f_size = (.4,1)
		self.aff_fourn_size = 1-w,h

		self.liste_clt_surf = stack(self,size_hint = self.liste_f_size,
			padding = dp(10),radius = dp(10),spacing = dp(8),
			bg_color = self.sc.aff_col1)
		
		self.add_surf(self.liste_clt_surf)

	@Cache_error
	def Foreign_surf(self):
		T = time.time()
		self.clt_lis = self.sc.DB.Get_clt_list()
		if self.New_clt:
			clt_obj = New_clt_surf(self,spacing = dp(10))
			self.liste_clt_surf.clear_widgets()
			clt_obj.add_all()
			self.liste_clt_surf.add_surf(clt_obj)
		else:
			self.add_liste_clt_surf()

	def add_liste_clt_surf(self):
		h = .04
		self.liste_clt_surf.clear_widgets()
		self.liste_clt_surf.add_text("Liste des clients",halign = "center",
			text_color = self.sc.text_col1,underline = True,size_hint = (.96,h))
		self.liste_clt_surf.add_icon_but(icon = 'printer',text_color = self.sc.black,
			size_hint = (.03,h),on_press = self.options_set,info = "Imprimée")

		txt_col = self.sc.text_col1
		bg_col = None
		if self.trie_sur_p:
			txt_col = self.sc.aff_col2

		dic = {
			#"Lien d'affiliation":(self.th_typ,self.sc.DB.Get_association_list()
			#	,self.set_type),
			#"Chargé d'affaire":(self.th_cate,self.sc.get_all_charger(),
			#	self.set_cate),
			"Trier par solde":(self.solde_clt,self.solde_l,
				self.set_solde_clt)
		}
		for k,liste in dic.items():
			txt,liste,fonc = liste
			self.liste_clt_surf.add_text(k,text_color = self.sc.text_col1,
				size_hint = (.08,h))
			self.liste_clt_surf.add_surf(liste_set(self,txt,liste,
				size_hint = (.12,h),mult = 1,mother_fonc = fonc,))
		self.liste_clt_surf.add_text_input('Trier par nom',(.08,h),(.2,h),
			self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,on_text = self.set_name,
			placeholder ='Trier par nom du client')
		self.tab_surf = Table(self,size_hint = (1,.87),
			bg_color = self.sc.aff_col3,exec_fonc = self.show_clt,
			exec_key = "nom",padding = dp(5),radius = dp(10))

		self.liste_clt_surf.add_surf(self.tab_surf)
		self.update_tab()

	@Cache_error
	def update_tab(self):
		entete = ("nom","code client","chargé d'affaire","lien d'affiliation",
			"solde","Solde comptable","tel","status")
		wid_l = [.2,.11,.15,.1,.11,.11,.11,.11,]
		liste = self.Trie_clt()
		trie_entete = ("nom","solde","status","Solde comptable")
		self.tab_surf.Creat_Table(wid_l,entete,liste,ent_size = (1,.06),
			ligne_h = .075,trie_entete = trie_entete)

	def Trie_clt(self):
		liste = self.sc.DB.Get_clt_list()
		liste = [i for i in map(self.Trie,liste) if i]
		return liste

	def Trie(self,name):
		clt_d = self.sc.DB.Get_this_clt(name)
		if clt_d:
			if not clt_d.get('Solde comptable'):
				if clt_d.get('solde',int()) == 0:
					clt_d['Solde comptable'] = "Normal"

				elif clt_d.get('solde',int()) > 0:
					clt_d['Solde comptable'] = "Positif"
					
				elif clt_d.get("solde",int()) < 0:
					clt_d['Solde comptable'] = "Négatif"

			if self.this_clt_name.lower() not in clt_d.get('nom').lower():
				return None
			if self.th_typ:
				l_ff = clt_d.get("lien d'affiliation")
				if not l_ff:
					l_ff = str()
				if l_ff.lower() != self.th_typ.lower():
					return None
			if self.th_cate:
				l_ff = clt_d.get("chargé d'affaire")
				if not l_ff:
					l_ff = str()

				if l_ff.lower() != self.th_cate.lower():
					return None
			if self.solde_clt:
				l_ff = clt_d.get("Solde comptable")
				if not l_ff:
					l_ff = str()

				if l_ff.lower() != self.solde_clt.lower():
					return None 

			if clt_d['Solde comptable'] == "Négatif":
				clt_d['status'] = "A vérifier"
			elif clt_d['Solde comptable'] == "Normal":
				clt_d['status'] = "Ordinaire"
			return clt_d

# Gestion des actions des bouttons
	def set_name(self,wid,val):
		self.this_clt_name = val
		self.update_tab()

	def set_solde_clt(self,info):
		self.solde_clt = info
		self.update_tab()

	def set_status_clt(self,info):
		self.status_clt = info
		self.update_tab()

	@Cache_error
	def options_set(self,wid):
		if wid.info == "Imprimée":
			obj = self.sc.imp_part_dic('Résumé')(self)
			liste = self.Trie_clt()
			liste.sort(key = itemgetter('N°'))
			entete = ["nom","code client","chargé d'affaire","lien d'affiliation",
				"solde","Solde comptable","tel","status"]
			wid_l = [round(1/len(entete),2)]*len(entete)
			wid_l[0] += .05
			wid_l[1] -= .05
			
			info = str()
			if self.th_typ:
				info+=f"Lien d'affiliation: {self.th_typ}<br/>"
			if self.th_cate:
				info+=f"Chargé d'affaire: {self.th_cate}<br/>"
			if self.solde_clt:
				info+=f"Status de solde: {self.solde_clt}<br/>"
			if self.status_clt:
				info+=f"status du clients: {self.status_clt}<br/>"
			if self.trie_sur_p:
				info+=f"Période d'ajout: du {self.day1} au {self.day2}<br/>"
			titre = 'Liste des clients'
			info += 'Agence TOKPOTA1'
			obj.Create_fact(wid_l,entete,liste,titre,info)

		elif wid.info == "Nouveau":
			self.New_clt = True
			self.add_all()

	def set_type(self,info):
		self.th_typ = info
		self.update_tab()

	def set_cate(self,info):
		self.th_cate = info
		self.update_tab()

	def set_periode(self):
		self.this_date_dict = self.periode_surf.date_dict
		self.update_tab()

	def set_periode_surf(self,wid):
		if self.trie_sur_p:
			self.trie_sur_p = False
		else:
			self.trie_sur_p = True

		self.add_liste_clt_surf()

	@Cache_error
	def show_clt(self,wid):
		#self.clear_widgets()
		self.aff_clt_surf = TH_det_client(self,
			radius = dp(10),bg_color = self.sc.aff_col1,
			padding = dp(10))
		self.this_clt = wid.info
		num = self.sc.DB.Get_this_clt_num(self.this_clt)
		self.this_client = self.sc.DB.get_client(num)
		self.aff_clt_surf.this_client = self.this_client
		self.aff_clt_surf.add_all()
		self.add_modal_surf(self.aff_clt_surf,size_hint = (.95,.9))
		#self.add_surf(self.aff_clt_surf)

class G_client(Model_acc):
	def Set_but_icon_info(self):
		self.but_dic = {
			"Clients":client_part,
			"Nouveau clients":New_clt_surf,
			#"Affiliation":association,
			"Annalyse clientèle":annalys_client
		}
		self.icon_dic = {
			"Clients":'account-group',
			"Nouveau clients":"account-plus",
			"Affiliation":'link-variant',
			"Annalyse clientèle":"finance"
		}
		self.clt_list = self.sc.DB.get_client()
		self.my_info_dict = {
			"Clients":len(self.clt_list),
			"Nouveau clients":str(),
			#"Affiliation":len(self.sc.DB.Get_association_list()),
			"Annalyse clientèle":str()
		}
		self.titre = 'Histogramme des soldes comptable des clients'
		self.data_dict = self.depart_client()
		self.y_label = self.data_dict.keys()
		self.cols = [
		self.sc.text_col1,self.sc.red,self.sc.black,self.sc.green
			]
		self.th_padd = 5

	def depart_client(self):
		all_clt = self.sc.DB.get_client()
		debs = int()
		cres = int()
		ords = int()
		for k,dic in all_clt.items():
			K = k.upper()
			if K in self.clt_list.keys():
				if float(dic.get('solde'))<0.0:
					cres += 1
				elif float(dic.get('solde'))>0.0:
					debs += 1
				elif float(dic.get('solde')) == 0.0:
					ords += 1
		return {
			"":int(),
			"Clients débiteurs":debs,
			"Clients créanciers":cres,
			"Clients ordinaire":ords,
		}

