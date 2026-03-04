#Coding:utf-8
from lib.davbuild import *
from pathlib import Path
from lib.serveur.DAV_BASE.MyData import date_obj
import shutil
from Desktop.Prog.IMPR.Impression import *

def add_connex_info(self,host,port,**kwargs):
	self.set_color_obj()
	self.th_host = host
	self.th_port = port
	h = .06
	
	th_b = stack(self,padding = [dp(10),dp(200),dp(10),dp(10)]
		,spacing = dp(20),
		bg_color = self.sc.aff_col1)
	th_b.add_text('Connexion internet impossible!',
		text_color = self.sc.text_col1,halign = 'center',
		size_hint = (1,h),)
	
	th_b.add_button_custom('Rafraichir',self.relance_con,
		text_color = self.sc.white, bg_color = self.sc.green,
		size_hint = (.4,h), padd = (.3,h))
	
	self.TH_D = th_b
	self.add_modal_surf(th_b,show_close = False,size_hint = (1,1),
		auto_dismiss = False,radius = dp(1))

def add_modal_surf(self,surf,titre = "Alerte système",auto_dismiss = True,
	show_close = True,radius = dp(10),bg_color = 'None',**kwargs):
	if bg_color == "None":
		bg_color = self.sc.aff_col3
	try:
		th_surf = self.get_modal_surf(surf,titre,show_close,self.close_modal,
			bg_color = bg_color,radius = radius)
		self.modal = ModalView(auto_dismiss = auto_dismiss,**kwargs)
		self.modal.add_widget(th_surf)

	except Exception as E:
		print(E)
		self.close_modal()
		th_surf = self.get_modal_surf(surf,titre,show_close,self.close_modal,
			bg_color = bg_color)
		self.modal = ModalView(auto_dismiss = auto_dismiss,**kwargs)
		self.modal.add_widget(th_surf)

	self.sc.add_to_modal(self.modal)
	self.modal.open()

def get_modal_surf(self,surf,titre,show_close,close_fonc,bg_color,radius = dp(10)):
	padd = dp(5)
	if not bg_color:
		padd = 0
	th_surf = box(self,bg_color = bg_color,
		padding = padd,radius = radius)
	title = stack(self,size_hint = (1,None),height = dp(30))
	title.add_text(titre,text_color = self.sc.text_col1,
		size_hint = (.9,1),valign = 'middle')
	if show_close:
		title.add_icon_but(icon = "close",text_color = self.sc.red,
			on_press = close_fonc,size_hint = (.1,1),
			font_size = '18sp')
		th_surf.add_surf(title)
	th_surf.add_surf(surf)
	return th_surf

def close_modal(self,*args):
	self.sc.sup_from_modal(self.modal)
	self.modal.dismiss()

def play_sound(self, *args):
	if self.sound:
		self.sound.play()

def add_refused_error(self,text,text_color = None,halign = "center",
	**kwargs):
	try:
		self.modal.dismiss()
	except:
		...
	if not text_color:
		text_color = self.sc.text_col1
	try:
		self.play_sound()
	except:
		pass
	bo = stack(self,padding = dp(10),spacing = dp(10),
		bg_color = self.sc.aff_col1,radius = dp(10))
	
	bo.add_text(text,text_color = text_color,
		halign = halign,**kwargs)
	self.add_modal_surf(bo,titre = "Alerte système",size_hint = (.25,.25))

def add_refused_error2(self,text,text_color = None,halign = "center",
	**kwargs):
	try:
		self.modal.dismiss()
	except:
		...
	if not text_color:
		text_color = self.sc.text_col1
	try:
		self.play_sound()
	except:
		pass
	bo = stack(self,padding = dp(10),spacing = dp(10),
		bg_color = self.sc.aff_col1,radius = dp(10))
	
	bo.add_text(text,text_color = text_color,
		halign = halign,**kwargs)
	self.add_modal_surf(bo,titre = "Alerte système",size_hint = (.6,.5))


def End_app_(self,*args):
	self.modal.dismiss()

def set_host(self,wid,info):
	self.th_host = info

def End_app(self,wid):
	self.modal.dismiss()
	sys.exit()

def set_port(self,wid,info):
	self.th_port = info

def relance_con(self,wid):
	self.modal.dismiss()
	dic = {
		"host":self.th_host,
		"port":self.th_port,
	}
	Save_local_json('CON_INFO',dic)
	self.connexion = self.DB.Def_Con()
	if not self.connexion:
		self.TH_D.notify('Erreur de connexion')
	else:
		MDApp.get_running_app().stop()
		ZoeCorp().run()

def UP_this_l(self):
	self.liste_qte = self.DB.Get_qte_cond()
	self.liste_unit = self.DB.Get_uni_cond()

def Get_famm_d(self):
	if not isinstance(self.categorie_dict,(dict,list,tuple)):
		self.categorie_dict = list()
	return self.categorie_dict

def Get_my_clt(self,name):
	return self.clt_dict.get(name,dict())

def imp_part_dic(self,key): 
	return{
		"Factures":Factures,
		"Résumé":Resumer_imp,
		"Fiche":Fiche
	}.get(key)

def Get_fourn_list(self):
	liste = self.sc.DB.Get_fournisseur_list()
	self.all_fourn_dict = {self.sc.DB.Get_fourn_by_name(i).get('nom'):i for i in liste}
	return [i for i in self.all_fourn_dict.keys()]

def fournisseur(self):
	return self.Get_fourn_list()

def get_type_list(self):
	return ['particulier','entreprise']

def get_cat_list(self):
	return ['standart','grossiste']

# gestion des dates

def verif_clot(self):
	return True

def get_lieu(self):
	return "Cotonou"

def get_hour(self):
	return date_obj().hour

def get_now(self):
	return f"{self.get_today()}. {date_obj().hour}"

def get_categorie_liste(self):
	return [i for i in self.categorie_dict]

def get_this_sous_cat(self,cate):
	return self.categorie_dict.get(cate,list())

def add_back_but(self,info,on_press,
	text_color = tuple(),clear_wid = True):
	if not text_color:
		text_color = self.red
	if clear_wid:
		self.root.root.but_part.clear_widgets()
	b = box(self,size_hint = (None,1),width = dp(50))
	b.add_icon_but(icon = 'keyboard-backspace',on_press = on_press,
		size_hint = (None,1),size = (dp(50),dp(50)),font_size = '35sp',
		text_color = text_color)
	self.root.root.but_part.add_surf(b)
	self.root.root.but_part.add_text(info,text_color = self.sc.green,
		)

def Get_article_ident(self):
	key = self.DB.article_fic
	date = "ARTICLE"
	this_all_ind = self.DB.Get_gen_data(self.DB.Les_ind,key)
	if not this_all_ind:
		this_all_ind = dict()
	today = this_all_ind.get(date,int())
	today += 1
	ind = self.DB.Get_ind_format(today)
	id_cmd = f"{date} N°{ind}"
	return id_cmd

# Gestion des personnelles
#
def get_depot_fond_typ(self):
	"""
		Nous avons ici 4 formes de dépot de fond 
	"""
	return ["Vente d'actifs","Près",'Action',
	"Investissement","Autres"]

def get_motif_decaiss_list(self):
	return [
		"Achats de marchandises","Achats de matières premières","Services extérieurs",
		"Rémunérations du personnel","Avances sur salaires","Charges sociales",'Loyers',
		"Charges d’énergie et de communication","Fournitures non stockables",
		"Entretien et maintenance","Frais de déplacement","Impôts, taxes et versements assimilés",
		"TVA à décaisser","Frais remboursés","Remboursement emprunt","Charges d’intérêts",
		"Transfert interne","Prélèvement exploitant / associé","Charges diverses"
	]
	

def get_encaisse_type(self):
	dic = {
	"Encaissements":["Général",
		'émis par les client',
		'émis par les commerciaux',
		'émis par le Bureau'],
	"Identifiants":["Général",'Révoqués',
		"Valides"]
	}
	return dic

def get_moyen_paiement(self,typ):
	if typ == "virtuelles":
		return ["depot direct"]
	elif typ == 'banques':
		return ['virement','chèques']
	elif typ == "espèces":
		return ["main à main"]

def get_fournisseur_list(self):
	return self.fournisseur()

def get_img_from(self,wid):
	self.file_chooser()

# Méthode pour la gestion des commandes
def Get_cmd_typ_list(self):
	return ("En traitement","Livrée")

def Get_cmd_status_list(self):
	return ('Soldée',"Non soldée")


def print_fic(self,selection):
	self.file_selected = selection

@Cache_error
def clean_old_backup(self):
	dossier = Path("backup")
	if not dossier.exists():
		pass
	else:
		folder_list = list()
		if len(list(dossier.iterdir())) > 3:
			for folder in dossier.iterdir():
				if folder.is_dir():
					folder_list.append(datetime.strptime(folder.name,
						self.date_format))
		if folder_list:
			folder_list.sort()
			sup_list = folder_list[:-3]
			for date in sup_list:
				name = date.strftime(self.date_format)
				sup_path = Path(os.path.join(dossier,name))
				if sup_path.exists():
					shutil.rmtree(sup_path,onerror = self.handle_remove_readonly)

def handle_remove_readonly(self,func, path, exc):
	# Si erreur de permission, enlever l'attribut lecture seule et réessayer
	excvalue = exc[1]
	if func in (os.rmdir, os.remove) and excvalue.errno == 13:
		os.chmod(path, stat.S_IWRITE)
		func(path)
	else:
		raise

def End_zoecorp(self,title,text2,accept_fonc,dismis_fonc = None,
	but_liste = ["retour","bye bye"]):
	close_b = box(self,bg_color = self.aff_col1)
	
	close_b.add_text(text2,size_hint = (1,.5),text_color = self.orange,
		halign = 'center',font_size = '20sp',italic = True)
	but_st = stack(self,size_hint = (1,.2),spacing = dp(15),
		padding = dp(10))
	but_st.add_padd((.45,1))

	def annuler(*a):
		self.close_modal()

	if not dismis_fonc:
		dismis_fonc = annuler
	but_st.add_button(but_liste[0],text_color = self.white,
		bg_color = self.green,size_hint = (.2,1),on_press = dismis_fonc)
	but_st.add_padd((.06,1))
	but_st.add_button(but_liste[1],text_color =self.white,
		bg_color = self.red,size_hint = (.2,1),on_press = accept_fonc)
	close_b.add_surf(but_st)
	self.add_modal_surf(close_b,size_hint = (.27,.25),
		titre = "Confirmation",auto_dismiss = True)

# Gestion de la récupération de la liste de date