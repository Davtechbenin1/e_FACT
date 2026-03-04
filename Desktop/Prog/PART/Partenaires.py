#Coding:utf-8
"""
	Gestion des partenaires d'affaires de l'entreprise
"""
from lib.davbuild import *
from General_surf import *
from ..CMPT.general_obj2 import *
from ..CMPT.paie_surfs import *

class Partenaires(box):
	@Cache_error
	def initialisation(self):
		self.orientation = 'horizontal'
		self.cmpt_num = str()
		self.padding = dp(2)
		self.spacing = dp(2)
		self.typ_part = ""
		self.p_nom = str()
		self.clas_cmpt = str()
		self.cmpt_ass = str()
		self.size_pos()

	@Cache_error
	def Up_Base(self):
		self.typ_part_list = self.sc.DB.Get_all_part_typ()
		self.cmpt_ass_list = self.sc.DB.Get_all_compts_list()
		self.clas_cmpt_list = [i for i in self.sc.DB.Get_plan_class().keys()]

	@Cache_error
	def Foreign_surf(self):
		self.add_liste_surf()

	def size_pos(self):
		w,h = self.liste_size = .39,1
		self.aff_size = 1-w,h

		self.liste_surf = stack(self,size_hint = self.liste_size,
			padding = dp(10),radius = dp(10),bg_color = self.sc.aff_col1,
			spacing = dp(10))
		self.add_surf(self.liste_surf)

	@Cache_error
	def add_liste_surf(self):
		self.Up_Base()
		h = .045
		self.liste_surf.clear_widgets()
		self.liste_surf.add_text('Liste de vos Partenaires',text_color = self.sc.text_col1, 
			halign = 'center',underline = True, size_hint = (.95,h))
		self.liste_surf.add_icon_but(icon = 'printer',
			text_color = self.sc.black,size_hint = (.05,h))
		d = {
			'Type de partenaires :':(self.typ_part,self.typ_part_list,self.set_typ_part),
			"Class comptable :":(self.clas_cmpt,self.clas_cmpt_list,self.set_clas_cmpt)
		}
		for info,tup in d.items():
			txt,lis,fonc = tup
			self.liste_surf.add_text(info,text_color = self.sc.text_col1,
				size_hint = (.12,h))
			self.liste_surf.add_surf(liste_set(self,txt,lis,size_hint = (.18,h),
				mult = 1,mother_fonc = fonc))
		self.liste_surf.add_text_input('Trier par nom :',(.1,h),(.2,h),
			self.sc.text_col1,text_color = self.sc.text_col1,
			bg_color = self.sc.aff_col3,default_text = self.p_nom,
			on_text = self.set_p_nom,placeholder = 'Trier par nom')
		if "écritures" in self.sc.DB.Get_access_of('Partenaire'):
			self.liste_surf.add_icon_but(icon = 'plus',size_hint = (.05,h),
				text_color = self.sc.green,font_size = '34sp',on_press = self.new_prest)
		self.tab = Table(self,size_hint = (1,.9),padding = dp(10),
			radius = dp(10),bg_color = self.sc.aff_col3,exec_fonc = self.show_pres,
			exec_key = 'N°')
		self.liste_surf.add_surf(self.tab)
		self.Up_tab()

	@Cache_error
	def Up_tab(self):
		entete = ("nom","date d'enregistement",'IFU',
			'RCCM','type',"téléphone","solde")
		wid_l = .2,.13,.13,.13,.13,.13,.13
		liste = self.Get_prest()
		self.tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.06))

	def Get_prest(self):
		liste = [self.sc.DB.Get_this_partenaires(i) for i in self.sc.DB.Get_all_partenaires().keys()]
		liste = [i for i in map(self.Trie,liste) if i]
		return liste

	def Trie(self,pres_dict):
		if self.typ_part:
			if pres_dict.get('type').lower() != self.typ_part.lower():
				return None
		if self.clas_cmpt:
			if pres_dict.get('class comptable').lower() != self.clas_cmpt.lower():
				return None
		if self.p_nom:
			if self.p_nom.lower() not in pres_dict.get('nom').lower():
				return None
		return pres_dict

	@Cache_error
	def add_new_prest(self):
		h = .08
		self.part_info = self.sc.DB.partenaire_format()
		#self.liste_surf.clear_widgets()
		th_part_s = stack(self,bg_color = self.sc.aff_col1,padding = dp(10),
			spacing = dp(10))
		th_part_s.add_text("",size_hint = (.9,h),
			text_color = self.sc.text_col1,halign = 'center',underline = True,)

		th_part_s.add_padd((.15,h))
		th_part_s.add_text_input('Partenaires N° :',(.3,h),(.4,h),self.sc.text_col1
			,text_color = self.sc.black,font_size = "20sp",default_text = self.part_info.get('N°'),
			readonly = True)
		th_part_s.add_padd((.15,h))

		self.dict_oblig = {
			"nom":str(),
			"téléphone":str(),
			"IFU":" ",
			"RCCM":" ",
			"pourcentage":str(100),
		}
		for k,v in self.dict_oblig.items():
			th_part_s.add_padd((.15,h))
			th_part_s.add_text_input(k,(.3,h),(.4,h),self.sc.text_col1,
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				on_text = self.set_oblij_info,default_text = v)
			th_part_s.add_padd((.15,h))

		dic = {
			'Type de partenaires :':(self.typ_part,self.typ_part_list,self.set_typ_part),
		}
		for info,tup in dic.items():
			txt,lis,fonc = tup
			th_part_s.add_padd((.15,h))
			th_part_s.add_text(info,text_color = self.sc.text_col1,
				size_hint = (.3,h))
			th_part_s.add_surf(liste_set(self,txt,lis,size_hint = (.4,h),
				mult = 1,mother_fonc = fonc))
			th_part_s.add_padd((.15,h))
		"""
		th_part_s.add_text("compte comptable associé :",size_hint = (.3,h*1.2),
			text_color = self.sc.text_col1)
		th_part_s.add_surf(input_search_lay_new(self,
			self.cmpt_ass,self.cmpt_ass_list,self.set_cmpt_ass,
			size_hint = (.65,.3),mult = 7,sub_mod = 1,
			text_size = (.35,1),inp_size = (1,.12)))
		"""
		th_part_s.add_button_custom("Ajouter",self.save_part,
			size_hint =(.5,h),padd = (.25,h))

		self.add_modal_surf(th_part_s,titre = "Nouvel partenaire",
			size_hint = (.6,.7))

# Gestion des actions de comptes
	@Cache_error
	def save_part(self,wid):
		if self.check(self.dict_oblig):
			
			self.part_info.update(self.dict_oblig)
			if self.clas_cmpt:
				self.part_info['class comptable'] = self.clas_cmpt
			self.part_info["compte comptable associé"] = self.cmpt_ass
			self.part_info['type'] = self.typ_part or "Prestataires"

			ret = self.sc.DB.Save_partenaire(self.part_info)
			if ret:
				self.typ_part = str()
				self.add_liste_surf()
				self.modal.dismiss()
				self.sc.add_refused_error('Partenaire enrégistrer avec succès')
		else:
			self.sc.add_refused_error('Informations incomplètes')

	def set_cmpt_ass(self,info):
		self.cmpt_ass = info

	def set_oblij_info(self,wid,val):
		self.dict_oblig[wid.info] = val

	def close(self,wid):
		self.add_liste_surf()

	def show_pres(self,wid):
		self.cmpt_num = wid.info
		aff_surf = Show_partner(self,
			padding = dp(10),radius = dp(10),bg_color = self.sc.aff_col1)

		aff_surf.cmpt_num = self.cmpt_num
		aff_surf.add_all()
		self.add_modal_surf(aff_surf,size_hint = (.8,.9),
			titre = f"Gestion du partenaire {self.cmpt_num}")

	def set_typ_part(self,info):
		self.typ_part = info
		self.Up_tab()

	def set_clas_cmpt(self,info):
		self.clas_cmpt = info
		self.Up_tab()
	
	def set_p_nom(self,wid,val):
		self.p_nom = val
		self.Up_tab()

	def new_prest(self,wid):
		self.add_new_prest()

class Show_partner(menu_surf_V_maquette):
	def Get_menu_infos(self):
		dic = {
			"Informations partenaire":detail_partner,
			"Historiques des actions":historiques,
			"Paiements partenaire":paiements,
		}
		self.wid_dict = dict()
		for i,srf in dic.items():
			if self.sc.DB.Get_access_of(i):
				self.wid_dict[i] = srf
		self.icon_dict = {
			'Informations partenaire':"card-account-details-outline",
			"Historiques des actions":'file-document-edit-outline',
			"Paiements partenaire":'cash-multiple',
		}

class detail_partner(box):
	@Cache_error
	def initialisation(self):
		self.orientation = 'horizontal'
		self.cmpt_num = self.mother.cmpt_num

		self.nat_liste = 'passif','actif',"produit"
		self.typ = str()

		self.sold_n = str()
		self.typ_list = self.sc.DB.Get_all_part_typ()
		self.sold_n_list = [i for i in self.sc.DB.Get_plan_class().keys()]
		self.etat_fi = str()

		self.th_hist_mois = str()
		self.th_hist_mois_list = list()

		self.size_pos()
		self.add_all()
	
	def size_pos(self):
		self.part_info = stack(self,size_hint = (.55,1),
			spacing = dp(10))
		self.part_ecrit = stack(self,size_hint = (.45,1),
			spacing = dp(10))

		self.add_surf(self.part_info)
		self.add_text('',size_hint = (None,1),width = dp(1))
		self.add_surf(self.part_ecrit)

	@Cache_error
	def Foreign_surf(self):
		self.add_part_info()
		self.add_part_ecrit()

	def add_part_info(self):
		h = .05
		self.part_info.clear_widgets()
		if self.cmpt_num:
			self.cmpt_infos = self.sc.DB.Get_this_partenaires(self.cmpt_num)
			part_d = self.cmpt_infos.get('montant associé',dict())
			self.th_hist_mois_list = list()
			for val in part_d.values():
				self.th_hist_mois_list.extend(self.sc.DB.All_mois_mont_hist(val.get("libelé")))
			dic_stact = {
				"Numéro unique :":self.cmpt_infos.get('N°'),
				"Solde actuel :":self.format_val(self.cmpt_infos.get('solde')),
				"Date d'ajout :":self.cmpt_infos.get("date d'enregistement"),
			}
			for k,v in dic_stact.items():
				self.part_info.add_text_input(k,(.19,h),(.3,h),self.sc.green,
					text_color = self.sc.black,bg_color = self.sc.aff_col1,
					readonly = True,default_text = str(v),font_size = "18sp")
			self.part_info.add_padd((1,.00001))
			th_d = {
				"nom":self.cmpt_infos.get('nom'),
				"téléphone":self.cmpt_infos.get('téléphone'),
				"IFU":self.cmpt_infos.get("IFU"),
				"RCCM":self.cmpt_infos.get("RCCM"),
			}
			for k,v in th_d.items():
				self.part_info.add_padd((.15,h))
				self.part_info.add_text_input(k,(.2,h),(.5,h),self.sc.text_col1,
					text_color = self.sc.black,bg_color = self.sc.aff_col3,
					default_text = str(v),on_text = self.set_new_info)
				self.part_info.add_padd((.15,h))
			self.part_info.add_padd((.15,h))
			self.part_info.add_text_input('pourcentage',(.2,h),(.5,h),
				self.sc.text_col1,text_color = self.sc.text_col1,
				bg_color = self.sc.aff_col3,on_text = self.set_new_info,
				default_text = self.format_val(self.cmpt_infos.get('pourcentage',float())))
			self.part_info.add_padd((.15,h))
			
			th_d = {
				"Type de partenaire":(self.cmpt_infos.get('type'),
					self.typ_list,self.set_nat_cmpt),
				}
			for info,tup in th_d.items():
				txt,lis,fonc = tup
				self.part_info.add_padd((.15,h))
				self.part_info.add_text(info,text_color = self.sc.text_col1,
					size_hint = (.2,h))
				self.part_info.add_surf(liste_set(self,txt,lis,size_hint = (.5,h),
					mult = 1,mother_fonc = fonc))
				self.part_info.add_padd((.15,h))
			
			if 'écritures' in self.sc.DB.Get_access_of('Informations partenaire'):
				self.part_info.add_button_custom('Modifer',self.set_modif_cmp,
					bg_color = self.sc.orange,size_hint = (.3,h),padd = (.35,h),
					text_color = self.sc.text_col1)


			self.part_info.add_padd((1,h))
			self.part_info.add_padd((.15,h))
			self.part_info.add_text("Générer le fichier du mois",size_hint = (.3,.06),
				text_color = self.sc.text_col1)
			self.part_info.add_surf(liste_set(self,self.th_hist_mois,
				self.th_hist_mois_list,mother_fonc = self.set_hist_mois,
				size_hint = (.4,h)))
			self.part_info.add_padd((.15,h))

			self.part_info.add_button_custom("Générer",self.generer,
				bg_color = self.sc.green,size_hint = (.3,h),
				padd = (.35,h),text_color = self.sc.text_col1)

	def add_part_ecrit(self):
		h = .05
		self.part_ecrit.clear_widgets()

		self.part_ecrit.add_text('Montants acessoires',text_color = self.sc.text_col1,
			halign ='center',size_hint = (1,h),underline = True)
		self.Tab = Table(self,size_hint = (1,.9),bg_color = self.sc.aff_col3,
			padding = dp(10),exec_key = 'référence',exec_fonc = self.show_mont)
		self.part_ecrit.add_surf(self.Tab)
		self.Up_th_tab()

	@Cache_error
	def Up_th_tab(self):
		entete = 'date','libelé',"pourcentage"
		wid_l = .3,.4,.3
		liste = self.Trie_ecrit()
		self.Tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.05))

	def Trie_ecrit(self):
		dic = self.cmpt_infos.get('montant associé',dict())
		liste = [i for i in dic.values()]
		return liste

	@Cache_error
	def show_th_info(self,info):
		h = .11
		th_DDD = self.cmpt_infos.get("montant associé",dict())
		mont_d = th_DDD.get(info,dict())
		mont_part = stack(self,padding = dp(10),spacing = dp(10),
			bg_color = self.sc.aff_col1)
		if mont_d:
			for k,v in mont_d.items():
				read = True
				aff_col = self.sc.aff_col1
				if k == "pourcentage":
					read = False
					aff_col = self.sc.aff_col3
				mont_part.add_text_input(k,(.3,h),(.6,h),self.sc.text_col1,
					inp_info = info,text_color = self.sc.text_col1,
					bg_color = aff_col,readonly = read,
					default_text = str(v),on_text = self.set_pour)
			if "écritures" in self.sc.DB.Get_access_of("Partenaires"):
				mont_part.add_button_custom('Modifier',self.save_mont_modif,size_hint = (.5,h),
					padd = (.25,h))
		self.add_modal_surf(mont_part,size_hint = (.3,.45),
			titre = f"Gestion du montant {info}")

# Gestion des actions des bouttons
	@Cache_error
	def generer(self,wid):
		this_all_info = self.sc.DB.Get_hist_autre_mont(self.th_hist_mois)
		wb = Workbook()
		ws = wb.active
		ws.title = self.th_hist_mois
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

		colonnes = ("localité","nom du client","prénom du client","téléphone",
			"date de naissance","lieu de naissance","adresse","date d'achat",
			"capital","prime","Bénéficiaire désigné en cas de décès","Téléphone Bénéficiaire")
		ws.append([i.upper() for i in colonnes])

		th_colonnes = ("localité","nom du client","prénom du client","téléphone",
			"date de naissance","lieu de naissance")

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

		for th_col,val in enumerate(this_all_info.values(),start = 2):
			#print(val)
			clt_dic = self.sc.DB.Get_this_clt(val.get("Client"))
			for num,col in enumerate(colonnes,start = 1):
				th_val = val.get(col)
				if col in th_colonnes:
					th_val = clt_dic.get(col,str())
				elif col == "Bénéficiaire désigné en cas de décès":
					th_val = clt_dic.get("Personne à contacter",str())
				elif col == "Téléphone Bénéficiaire":
					th_val = clt_dic.get('Téléphone personne à contacter',str())

				cel = ws.cell(row = th_col,column = num,value = th_val)
				cel.border = border
				cel.font = th_font
		#sys.exit()

		try:
			wb.save(f"Fiche du {self.th_hist_mois}.xlsx")
		except:
			self.sc.add_refused_error('Vous avez un fichier du même nom qui est ouverte')
		self.open_link(f"Fiche du {self.th_hist_mois}.xlsx")

	def set_hist_mois(self,info):
		self.th_hist_mois = info

	def save_mont_modif(self,wid):
		self.set_modif_cmp(wid)
		self.add_all()

	def set_pour(self,wid,val):
		wid.text = self.regul_input(wid.text)
		if wid.text:
			info = wid.info
			mont_ass = self.cmpt_infos.get('montant associé',dict()).get(info)
			mont_ass["pourcentage"] = float(wid.text)
			self.cmpt_infos['montant associé'][info] = mont_ass

	def show_mont(self,wid):
		info =  wid.info
		self.show_th_info(info)

	def set_new_info(self,wid,val):
		if val:
			if wid.info == "pourcentage":
				wid.text = self.regul_input(val)
				if wid.text:
					val = float(wid.text)
				else:
					val = float()
			self.cmpt_infos[wid.info] = val

	def set_modif_cmp(self,wid):
		ret = self.sc.DB.Save_partenaire(self.cmpt_infos)
		if ret:
			self.sc.add_refused_error('Partenaire modifié avec succès')
			self.add_all()

	def set_supp_cmp(self,wid):
		self.sc.DB.Supp_this_cmpt(self.cmpt_infos)
		self.add_all()

	def set_typ(self,info):
		if info:
			self.cmpt_infos['compte comptable associé'] = info

	def set_intitul(self,wid,val):
		if val:
			self.cmpt_infos['intitulé'] = val

	def set_nat_cmpt(self,info):
		if info:
			self.cmpt_infos['type'] = info

	def set_etat_fi(self,info):
		if info:
			self.cmpt_infos['état financier'] = info

	def set_sold_n(self,info):
		if info:
			self.cmpt_infos['class comptable'] = info

class historiques(stack):
	@Cache_error
	def initialisation(self):
		self.padding = [0,dp(10),0,0]
		self.spacing = dp(10)
		self.cmpt_num = self.mother.cmpt_num
		self.cmpt_infos = self.sc.DB.Get_this_partenaires(self.cmpt_num)
		h = .05
		self.ident = str()
		self.ident_liste = self.sc.DB.Get_autres_montants()
		self.credit = str()
		self.libele = str()

		self.add_surf(Periode_set(self,size_hint = (.3,h),exc_fonc = self.Up_tab,
			info_w = .2,))
		self.add_text("Montant accessoires :",size_hint = (.1,.06),
			text_color = self.sc.text_col1)
		self.add_surf(liste_set(self,self.ident,self.ident_liste,size_hint = (.15,h),
			mother_fonc = self.set_ident,mult = 1))
		self.add_text_input("L'acréditeur du montant :",(.1,.06),(.12,h),
			self.sc.text_col1,bg_color = self.sc.aff_col3,on_text = self.set_credit,
			text_color = self.sc.text_col1,default_text = self.credit,
			placeholder = 'Le crédit')
		self.add_text_input("Le libelé du montant :",(.1,.06),(.12,h),
			self.sc.text_col1,bg_color = self.sc.aff_col3,on_text = self.set_libele,
			text_color = self.sc.text_col1,default_text = self.libele,
			placeholder = 'Le libelé')
		self.tab = Table(self,size_hint = (1,.9),bg_color = self.sc.aff_col3)
		self.add_surf(self.tab)
		self.Up_tab()

	@Cache_error
	def Up_tab(self):
		entete = 'date',"heure","libelé",'référence',"montant","identifiant"
		wid_l = [round(1/len(entete),2)]*len(entete)
		liste = self.Trie_Histos()
		self.tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.06),
			ligne_h = .08)

	def Trie_Histos(self):
		his_dict = self.cmpt_infos.get('historiques',dict())
		lis = list()
		date_liste = self.get_date_list(self.day1,self.day2)
		for key,dic in his_dict.items():
			dat = get_date_from_N(key)
			if dat in date_liste:
				lis.append(dic)
		return [i for i in map(self.Trie,lis)]

	def Trie(self,his_dict):
		if self.ident:
			if his_dict.get('identifiant').lower() != self.ident:
				return None
		if self.credit:
			if self.credit not in his_dict.get('crédit'):
				return None
		if self.libele:
			if self.libele not in his_dict.get('libelé'):
				return None
		return his_dict

# Gestion des actions des boutons
	def set_ident(self,info):
		self.ident = info
		self.Up_tab()

	def set_credit(self,wid,val):
		self.credit = val
		self.Up_tab()

	def set_libele(self,wid,val):
		self.libele = val
		self.Up_tab()

class paiements(stack):
	@Cache_error
	def initialisation(self):
		self.padding = [0,dp(10),0,0]
		self.spacing = dp(10)
		self.cmpt_num = self.mother.cmpt_num
		self.cmpt_infos = self.sc.DB.Get_this_partenaires(self.cmpt_num)
		self.add_all()

	@Cache_error
	def Foreign_surf(self):
		self.clear_widgets()
		self.add_histo()

	@Cache_error
	def add_histo(self):
		h = .05
		self.ident = str()
		self.ident_liste = ["espèces",'virtuelle',"banque"]
		self.credit = str()
		self.libele = str()
		self.add_surf(Periode_set(self,size_hint = (.3,h),
			exc_fonc = self.Up_tab,info_w = .2))
		self.add_text("mode de paiement :",size_hint = (.08,.06),
			text_color = self.sc.text_col1)
		self.add_surf(liste_set(self,self.ident,self.ident_liste,
			size_hint = (.12,h),mult = 1,
			mother_fonc = self.set_ident))
		self.add_text_input("opérateur :",(.08,h),(.12,h),
			self.sc.text_col1,bg_color = self.sc.aff_col3,on_text = self.set_credit,
			text_color = self.sc.text_col1,default_text = self.credit,
			placeholder = "Le nom de l'opérateur")
		self.add_text_input("Le libelé du paiements :",(.1,.06),(.12,h),
			self.sc.text_col1,bg_color = self.sc.aff_col3,on_text = self.set_libele,
			text_color = self.sc.text_col1,default_text = self.libele,
			placeholder = 'Le libelé')
		if "écritures" in self.sc.DB.Get_access_of('Paiements partenaire'):
			B = box(self,orientation = 'horizontal',size_hint = (.08,h))
			B.add_icon_but(icon = 'plus',font_size = "34sp",
				size = (dp(30),dp(30)),text_color = self.sc.black,
				on_press = self.new_recouv,size_hint = (None,None))
			B.add_button("New",text_color = self.sc.black,
				on_press = self.new_recouv,bg_color = None,
				halign = 'left')
			self.add_surf(B)
	
		self.tab = Table(self,size_hint = (1,.85),bg_color = self.sc.aff_col3,
			exec_key = 'N°',exec_fonc = self.show_recouv)
		self.add_surf(self.tab)
		self.Up_tab()

	@Cache_error
	def Up_tab(self):
		entete = 'date',"heure","libelé",'opérateur',"montant","mode de paiement"
		wid_l = [round(1/len(entete),2)]*len(entete)
		liste = self.Trie_Histos()
		self.tab.Creat_Table(wid_l,entete,liste,ent_size = (1,.07))

	def Trie_Histos(self):
		his_dict = self.cmpt_infos.get('paiements',dict())
		if not his_dict:
			his_dict = dict()
		lis = list()
		date_liste = self.get_date_list(self.day1,self.day2)
		for num,dic in his_dict.items():
			dat = get_date_from_N(num)
			if dat in date_liste:
				lis.append(dic)
		return [i for i in map(self.Trie,lis)]

	def Trie(self,his_dict):
		if self.ident:
			if his_dict.get('mode de paiement').lower() != self.ident:
				return None
		if self.credit:
			if self.credit.lower() not in his_dict.get('opérateur').lower():
				return None
		if self.libele:
			if self.libele.lower() not in his_dict.get('libelé').lower():
				return None
		return his_dict

	@Cache_error
	def Save_vente(self,wid):
		ident = wid.this_decaiss_info.get('N°')
		dic = self.sc.DB.Get_paie_format()
		if not self.mont:
			self.mont = self.mont_liste[0]
		dic["libelé"] = self.mont
		dic['montant'] = self.paie_obj.montant
		dic['mode de paiement'] = self.paie_obj.mode_paie
		dic['N°'] = ident
		paie_dic = self.cmpt_infos.get("paiements",dict())
		if not paie_dic:
			paie_dic = dict()
		paie_dic[ident] = dic
		self.cmpt_infos['paiements'] = paie_dic
		self.cmpt_infos["solde"] -= self.paie_obj.montant
		h_dic = self.sc.DB.Get_paiement_f()
		h_dic['libelé'] = self.mont
		h_dic['référence'] = ident
		h_dic['montant'] = self.paie_obj.montant
		h_dic['débit'] = self.cmpt_infos.get('nom')
		self.excecute(self._SAVE,h_dic)
		self.close_modal()

	def _SAVE(self,h_dic):
		self.sc.DB.Save_m_access_credit(h_dic,self.mont)
		self.sc.DB.Update_partenaire(self.cmpt_infos)

# Gestion des actions des boutons
	def set_ident(self,info):
		self.ident = info
		self.Up_tab()

	def set_credit(self,wid,val):
		self.credit = val
		self.Up_tab()

	def set_libele(self,wid,val):
		self.libele = val
		self.Up_tab()

	def show_recouv(self,wid):
		info = wid.info
		self.recouv_to_developp = info
		self.sc.add_refused_error("Non définie")
		#obj = decaiss_show(self)
		#self.clear_widgets()
		#self.add_surf(obj)

	def back(self,wid):
		self.add_all()

	@Cache_error
	def new_recouv(self,wid):
		h = .09
		obj = stack(self,spacing = dp(10),bg_color = self.sc.aff_col1,
			padding = dp(10))
		self.paie_obj = decaisse_paie(self,.09,
			f"Reglement de partenaires",
			self.cmpt_infos.get('nom'),self.back,
			float(),modif_mont = True,mother_fonc = self.Save_vente)
		self.paie_obj.cate_benef = 'Partenaires'
		self.paie_obj.benef = self.cmpt_infos.get('nom')
		self.paie_obj.montant = self.cmpt_infos.get('solde')
		self.paie_obj.init()
		
		self.mont_liste = [dic.get('libelé') for i,dic in self.cmpt_infos.get(
			'montant associé',dict()).items()]
		if self.mont_liste:
			self.mont = self.mont_liste[0]
			#self.clear_widgets()
			obj.add_text("Montant associé",size_hint = (.3,h),
				text_color = self.sc.text_col1)
			obj.add_surf(liste_set(self,self.mont,self.mont_liste,
				size_hint = (.6,h),mult = 1,mother_fonc = self.set_mont))
			obj.add_surf(self.paie_obj)
			self.add_modal_surf(obj,size_hint = (.35,.6),
				titre = 'Règlement de partenaires')
		else:
			self.sc.add_refused_error("Vous ne pouvez pas faire un paiement si le partenaires n'a pas un montant accessoire attribuer")
		
	def set_mont(self,info):
		self.mont = info
		if self.mont:
			self.paie_obj.add_all()
		else:
			self.paie_obj.clear_widgets()
