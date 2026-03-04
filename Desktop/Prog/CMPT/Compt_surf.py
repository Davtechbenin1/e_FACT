#Coding:utf-8
"""
	Gestion des surface pour la définition des parties
	de l'interface du comptoire et de la gestion des
	commande
"""
from lib.davbuild import *
from General_surf import *
from .Commande import develop_cmd

class developpe_compt(develop_cmd):
	cmd_ident = str()
	def size_pos(self):
		parti1 = box(self,spacing = dp(10),size_hint = (1,.5),
			orientation = 'horizontal')
		parti2 = box(self,spacing = dp(10),size_hint = (1,.5),
			orientation = 'horizontal')

		self.add_surf(parti1)
		self.add_surf(parti2)

		self.plan_surf = stack(self,size_hint = (.3,1),
			padding = dp(10),radius = dp(10),bg_color = self.sc.aff_col1,
			spacing = dp(5))
		self.penal_surf = stack(self,size_hint = (.4,1),
			padding = dp(10),radius = dp(10),bg_color = self.sc.aff_col1,
			spacing = dp(10))

		self.clt_part = stack(self,size_hint = (.6,1))
		self.art_part = stack(self,size_hint = (1,1))

		parti1.add_surf(self.clt_part)
		parti1.add_surf(self.penal_surf)

		parti2.add_surf(self.art_part)

		self.plan_date = self.day1
		self.plan_mont = float()
	
	def Foreign_surf(self):
		if self.cmd_ident:
			self.cmd_dict = self.sc.DB.Get_this_cmd(self.cmd_ident)
			if not self.cmd_dict:
				pass
			else:
				self.clt_dict = self.sc.DB.Get_this_clt(self.cmd_dict.get('client'))
				self.add_clt_part()
				self.add_art_part()
				self.add_penel_surf()
				self.plan_surf.clear_widgets()
				self.plan_surf.add_text('Cette facture est déjà soldée',
					text_color = self.sc.text_col1,halign = 'center',
					font_size = '20sp')
		else:
			self.clear_widgets()
			self.size_pos()

	def add_penel_surf(self):
		this_h = .08
		self.penal_surf.clear_widgets()
		self.penal_surf.add_text('Information général sur la commande',
			text_color = self.sc.text_col1,halign = 'center',
			size_hint = (1,this_h),underline = True)
		infos = {
			"Identifiant de la commande" : self.cmd_dict.get('id de la commande'),
			"Status de la commande":self.cmd_dict.get('status de la commande'),
			"Status du paiement":self.cmd_dict.get('status du paiement'),
		}
		for k,v in infos.items():
			self.penal_surf.add_text_input(k,(.6,this_h),
				(.4,this_h),self.sc.text_col1,default_text = str(v),
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				readonly = True)
		self.penal_surf.add_text('Listes des paiements :',
			size_hint = (.35,this_h*1.5),text_color = self.sc.text_col1,
			)
		liste = self.cmd_dict.get('paiements')
		ind = 0
		for id_paie in liste:
			ind += 1
			self.penal_surf.add_button(str(ind)+'e',text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,size_hint = (.12,this_h),
				on_press = self.show_recouvr,info = id_paie)
		self.penal_surf.add_padd((1,.01))
		status = self.cmd_dict.get('status de la commande')
		status_paie = self.cmd_dict.get('status du paiement')
		but_list = self.get_button_dict(status)
		but_surf = box(self,size_hint = (1,this_h*1.3),
			orientation = 'horizontal',padding = dp(5),
			spacing = dp(5),radius = dp(5),
			bg_color = self.sc.aff_col3)
		but_surf.rejette_cmd = self.rejette_cmd
		info = self.cmd_dict.get('id de la commande')
		if self.check_access("gestion cmds"):
			for but,but_fonc in but_list.items():
				but_surf.add_button(but,
					info = info,
					text_color = self.sc.text_col3,
					bg_color = self.sc.green,
					on_press = but_fonc)
			if but_list:
				self.penal_surf.add_surf(but_surf)
		if status.lower() in ['en cours',"en traitement",'en attente']:
			if status.lower() == 'en traitement' and not self.cmd_dict.get('montant payé'):			
				self.modif_but()
			elif status.lower() != "en traitement":
				self.modif_but()

		self.penal_surf.add_padd((.066,this_h))
		self.penal_surf.add_button('Impression',
			text_color = self.sc.text_col3,bg_color = self.sc.aff_col2,
			size_hint = (.4,this_h),on_press = self.impression)

		self.penal_surf.add_padd((.066,.1))
		if not self.cmd_dict.get('montant payé') and self.cmd_dict.get('status de la commande') == "Livrée":
			self.penal_surf.add_button('Retour en stock',
				text_color = self.sc.text_col3,bg_color = self.sc.red,
				size_hint = (.4,.1),on_press = self.retour_en_stock)
			self.penal_surf.add_padd((.066,.1))


	def Save_vente(self):
		return self.cmd_ident

	def Get_mont(self):
		next_paie = self.sc.DB.Get_next_paie(self.cmd_dict)
		if next_paie:
			return next_paie[1]

class Liste_cmds(stack):
	def __init__(self,mother,**kwargs):
		stack.__init__(self,mother,**kwargs)
		self.status = str()
		self.spacing = dp(5)
		self.padding = dp(10)
		self.paiem = str()
		self.clt_name = str()
		self.size_pos()
		#self.add_all()

	def Foreign_surf(self):
		self.add_entete()
		self.add_details_surf()

	def size_pos(self):
		w,h = self.ent_s = 1,.2
		self.det_s = w,1-h

	def add_entete(self):
		self.clear_widgets()
		h = .045
		self.add_text('Status de la commande :',
			text_color = self.sc.text_col1,size_hint= (.1,h),
			)
		self.add_surf(liste_set(self,self.status,
			self.sc.Get_cmd_typ_list(),mother_fonc = self.set_status,
			size_hint = (.12,h),mult = 1))

		self.add_text('Status de paiement :',
			text_color = self.sc.text_col1,size_hint= (.1,h),
			)
		self.add_surf(liste_set(self,self.paiem,
			("soldée",'non soldée'),mother_fonc = self.set_paiem,
			size_hint = (.12,h),mult = 1))

		self.add_surf(Periode_set(self,info_w = .2,
			exc_fonc = self.add_details_surf,size_hint = (.3,h)))
		self.add_text('Trier par nom :',size_hint = (.1,h),
			text_color = self.sc.text_col1)
		self.add_input('Clients',placeholder = 'Trier par nom du client',
			size_hint = (.12,h),on_text = self.set_clt,
			text_color= self.sc.text_col1,bg_color = self.sc.aff_col3,)

		self.details_surf = Table(self,size_hint = (1,.95),
			exec_fonc = self.show_details,exec_key = 'N°',
			bg_color = self.sc.aff_col3,padding = dp(5))
		self.add_details_surf()
		self.add_surf(self.details_surf)

	@Cache_error
	def add_details_surf(self):
		wid_l = .03,.1,.1,.09,.09,.09,.1,.1,.1,.1,.1
		entete = ["N° d'ordre","Code client","Nom du client",
			"catégorie","affiliation","date d'émission",
			"montant TTC","montant payé","montant restant",
			"status de la commande","status du paiement"]
		liste = self.Get_fact_list()
		self.details_surf.Creat_Table(wid_l,entete,
			liste,ent_size = (1,.06))

	def Get_fact_list(self):
		date_liste = self.get_date_list(self.day1,self.day2)
		all_cmds = [dic for i,dic in self.sc.DB.Get_all_cmd_liste(
			date_liste).items()]
		liste = [i for i in map(self.Trie, all_cmds) if i]
		liste.sort(key = itemgetter("th_sort"),reverse = True)
		i = 1
		for dic in liste:
			dic["N° d'ordre"] = i
			i += 1
		return liste

	def Trie(self,cmd_d):
		try:
			if self.status:
				if cmd_d.get('status de la commande').lower() != self.status.lower():
					return None
			if self.clt_name.lower() not in cmd_d.get("Nom du client").lower():
				return None
			if self.paiem:
				if self.paiem.lower() != cmd_d.get('status du paiement').lower():
					return None
			cmd_d['N°'] = cmd_d.get('id de la commande')

			client_obj = self.sc.DB.Get_this_clt(cmd_d.get('client'))
			if not client_obj:
				client_obj = dict()
			cmd_d['nom client'] = client_obj.get('nom',str())
			cmd_d['Code client'] = client_obj.get('N°',str())
			th_asso = self.sc.DB.Get_this_association(client_obj.get("association appartenue"))
			cmd_d["affiliation"] = th_asso.get('nom',str())
			cmd_d["catégorie"] = cmd_d["type de contrat"]
			mttc = cmd_d.get('montant TTC')
			mp = cmd_d.get('montant payé')
			cmd_d["montant restant"] = mttc - mp
			cmd_d['th_sort'] = int(self.Get_real_num(cmd_d.get("N°")))
			
			return cmd_d
		except:
			return None

# Méthodes de gestion des actions
	def show_details(self,wid):
		if self.mother.cmd_ident == wid.info:
			self.mother.cmd_ident = str()
		else:
			self.mother.cmd_ident = wid.info
		self.mother.add_all()

	def set_clt(self,wid,val):
		self.clt_name = val
		self.add_details_surf()

	def set_status(self,info):
		if self.status:
			self.status = str()
		else:
			self.status = info
		self.add_details_surf()

	def set_paiem(self,info):
		if self.paiem:
			self.paiem = str()
		else:
			self.paiem = info
		self.add_details_surf()
