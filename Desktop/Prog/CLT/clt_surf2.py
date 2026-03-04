#Coding:utf-8
from lib.davbuild import *
from General_surf import *

class annalys_client(box):
	def initialisation(self):
		self.padding = dp(10)
		self.spacing = dp(10)
		self.charger = str()
		self.regroup = str()
		self.name = str()
		self.p_achat = [self.day1,self.day2]
		self.p_ajout = list()
		self.total_dic = {
			"Montant total d'achat":float(),
			"Montant total recouvrit":float(),
			"Accompte total payé":float(),
			"Créance total en cours":float(),
			"Montant total restant":float(),
		}
		self.size_pos()

	def size_pos(self):
		h = .045
		self.entete = box(self,size_hint = (1,h),orientation = "horizontal",
			spacing = dp(10))
		self.tab_surf = Table(self,bg_color = self.sc.aff_col3)

		self.total_surf = box(self,size_hint = (1,h),orientation = 'horizontal',
			spacing = dp(10))

		self.add_surf(self.entete)
		self.add_surf(self.tab_surf)
		self.add_surf(self.total_surf)

	def add_total(self):
		self.total_surf.clear_widgets()
		for k,v in self.total_dic.items():
			self.total_surf.add_text(k,text_color = self.sc.text_col1,
				size_hint = (.15,1))
			self.total_surf.add_text(self.format_val(v),
				size_hint = (.1,1),
				bg_color = self.sc.aff_col3,padding_left = dp(10),
				text_color = self.sc.text_col1,radius = dp(10))


	def add_entete(self):
		self.entete.clear_widgets()
		self.entete.add_surf(Periode_set(self,size_hint = (.28,1),
			info = "Période d'achat",info_w = .35,exc_fonc = self.achat_date,
			input_color = self.sc.aff_col3))
		"""
		self.entete.add_text("chargée d'affaire",text_color = self.sc.text_col1,
			size_hint = (.09,1),)
		self.entete.add_surf(liste_set(self,self.charger,self.sc.get_all_charger()
			,size_hint = (.1,1),mother_fonc = self.set_charger
			))

		self.entete.add_text("Regroupement",text_color = self.sc.text_col1,
			size_hint = (.09,1),)
		self.entete.add_surf(liste_set(self,self.regroup,self.sc.DB.Get_association_list()
			,size_hint = (.1,1),mother_fonc = self.set_regroupement
			))
		"""
		self.entete.add_input('Trier',text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,on_text = self.set_name,
			default_text = self.name,placeholder = 'tirer par nom du client',
			size_hint = (.2,1))
		self.entete.add_surf(Periode_set(self,size_hint = (.3,1),
			info = "Période d'ajout",info_w = .35,exc_fonc = self.ajout_date,
			input_color = self.sc.aff_col3))
		self.entete.add_icon_but(icon = "printer",text_color = self.sc.black,
			size_hint = (None,None),size = (dp(25),dp(25)),
			font_size = '20sp',
			on_press = self.impression_xls)	

	@Cache_error
	def Foreign_surf(self):
		self.client_base = self.sc.DB.get_client()
		self.add_entete()
		self.add_tab()
		

	@Cache_error
	def add_tab(self):
		entete = ["code client","nom client","montant d'achat",
			"montant recouvrit","Accompte payé","créance en cours","montant restant à payé",
			"nature de la créance","date d'achat","date de fin de paiement"]
		wid_l = [.15,.1,.1,.1,.1,.1,.1,.1,.1,.1]
		liste = list(self.trie_clt_info())
		self.tab_surf.Creat_Table(wid_l,entete,liste,ent_size = (1,.06))
		self.add_total()

	@Cache_error
	def trie_clt_info(self):
		self.infos = dict()
		clt_list = map(self.trie,self.client_base.values())
		for clt in clt_list:
			if clt:
				cmds = self.get_real_cmds(clt.get('commandes'))
				for cmd in cmds:
					clt_infos = self.infos.get(clt.get('N°'))
					if cmd:
						if not clt_infos:
							clt_infos = {
								"code client":clt.get('N°'),
								"nom client":clt.get('nom')+' '+clt.get('prénom',str()),
								"montant d'achat":0,
								"montant recouvrit":0,
								"Accompte payé":0,
								"créance en cours":0,
								"montant restant à payé":clt.get('solde'),
								"nature de la créance":str(),
								"date d'achat":str(),
								"date de fin de paiement":str()
							}
							self.total_dic["Montant total restant"] += clt.get("solde")
						accompt = self.sc.DB.get_accompte_of(cmd)
						#print(cmd)
						clt_infos["montant d'achat"] += cmd.get('montant TTC',float())
						self.total_dic["Montant total d'achat"] += cmd.get('montant TTC',float())
						clt_infos['montant recouvrit'] += cmd.get('montant payé',float())
						self.total_dic["Montant total recouvrit"] += cmd.get('montant payé',float())
						clt_infos['Accompte payé'] += accompt
						self.total_dic["Accompte total payé"] += accompt
						if cmd.get('status du paiement',str()).lower() != "soldée":
							if cmd:
								clt_infos["créance en cours"]+=1
								self.total_dic["Créance total en cours"] += 1
							clt_infos['nature de la créance'] = cmd.get('status',str())
							clt_infos["date d'achat"] = cmd.get('date de livraison',str())
							clt_infos["date de fin de paiement"] = cmd.get('date de fin contrat',str())
						self.infos[clt.get('N°')] = clt_infos
				
		return self.infos.values()

	def get_real_cmds(self,liste):
		l = list()
		for cmd in liste:
			#print(self.p_achat)
			if self.p_achat:
				date = cmd.split("N°")[-1].split('_')[0]
				if date in self.p_achat:
					l.append(self.sc.DB.Get_this_cmd(cmd))
			else:
				l.append(self.sc.DB.Get_this_cmd(cmd))
		return l

	def trie(self,dic):
		if self.p_ajout:
			if dic.get("date d'enregistrement") not in self.p_ajout:
				return False
		name = dic.get('nom') + dic.get('prénom',str())
		if self.name.lower() not in name.lower():
			return False
		if self.charger:
			if dic.get("chargé d'affaire").lower() != self.charger.lower():
				return False
		if self.regroup:
			if str(dic.get("lien d'affiliation")).lower() != self.regroup.lower():
				return False
		return dic

# Gestion des actions des bouttons

	@Cache_error
	def set_name(self,wid,val):
		self.name = val
		self.add_tab()

	@Cache_error
	def set_charger(self,info):
		self.charger = info
		self.add_tab()

	@Cache_error
	def set_regroupement(self,info):
		self.regroup = info
		self.add_tab()

	@Cache_error
	def achat_date(self):
		self.p_achat = self.sc.get_date_list(self.day1,self.day2)
		self.add_tab()

	@Cache_error
	def ajout_date(self):
		self.p_ajout = self.sc.get_date_list(self.day1,self.day2)
		self.add_tab()

	@Cache_error
	def impression_xls(self,wid):
		this_all_info = self.trie_clt_info()
		wb = Workbook()
		ws = wb.active
		ws.title = "annalyse clientèle"
	# style entête
		font_bold = WS_style.Font(bold = True, color = "FFFFFF",size = 13)
		fill_blue = WS_style.PatternFill(start_color = "20AA6A",
			end_color = "20AA6A",fill_type = "solid")
		border = WS_style.Border(left = WS_style.Side(style = 'thin'),
			right = WS_style.Side(style = 'thin'),top = WS_style.Side(style = "thin"),
			bottom = WS_style.Side(style = "thin"))
		align_center = WS_style.Alignment(horizontal = "center",
			vertical = "center")
		th_font = WS_style.Font(bold = True,color = "000000",size = 13)
		colonnes = ["code client","nom client","montant d'achat",
			"montant recouvrit","Accompte payé","créance en cours","montant restant à payé",
			"nature de la créance","date d'achat","date de fin de paiement"]
		ws.append([i.upper() for i in colonnes])

		for col, titre in enumerate(colonnes,start = 1):
			cell = ws.cell(row = 1, column = col)
			cell.font = font_bold
			cell.fill = fill_blue
			cell.border = border
			cell.alignment = align_center
			width = round(len(titre.replace(' ',''))*2,0)
			if titre in ('localité',"adresse"):
				width = width * 3
			ws.column_dimensions[cell.column_letter].width = width

		for th_col,val in enumerate(this_all_info,start = 2):
			#print(val)
			clt_dic = self.sc.DB.Get_this_clt(val.get("Client"))
			for num,col in enumerate(colonnes,start = 1):
				th_val = val.get(col)
				
				cel = ws.cell(row = th_col,column = num,value = th_val)
				cel.border = border
				cel.font = th_font
		#sys.exit()

		try:
			wb.save(f"Infoclient.xlsx")
		except:
			self.sc.add_refused_error('Vous avez un fichier du même nom qui est ouverte')
		self.open_link(f"Infoclient.xlsx")
