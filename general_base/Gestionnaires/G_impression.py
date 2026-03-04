#Coding:utf-8
from lib.davbuild import *
from Desktop.Prog.IMPR.Impression import *
@Cache_error
def impress_fich_paie(self,fiche_info):
	try:
		nom = fiche_info.get('nom')+'_'+fiche_info.get('prénom')
		perso_info = self.DB.Get_this_perso(nom)
		nais = perso_info.get('date de naissance')
		if nais:
			age = int(self.sc.get_today().split('-')[-1])-int(nais.split('-')[-1])
		else:
			age = int()
	#
		doc = DocxTemplate("static/Fiche de paie.docx")
		ent_obj = self.DB.Get_entreprise()
		tel = ent_obj.get('téléphone')
		if ent_obj.get('whatsapp'):
			tel += f"/{ent_obj.get('whatsapp')}"
		adresse = 'Bénin'
		if ent_obj.get('ville'):
			adresse+=f" {ent_obj.get('ville')}"
		if ent_obj.get('quartier'):
			adresse+=f" {ent_obj.get('quartier')}"
		if ent_obj.get('maison'):
			adresse+=f" Maison: {ent_obj.get('maison')}"
		logo = InlineImage(doc, "media/logo.png", Cm(5))
		data = {
			"num":fiche_info.get('N°'),
			"date_em":fiche_info.get("date d'émissions"),
			"statue":fiche_info.get('status'),
			"nom":fiche_info.get('nom'),
			"prenom":fiche_info.get('prénom'),
			"age":f"{age} ans",
			"poste":fiche_info.get('poste actuel'),
			"categorie":fiche_info.get('type de personel'),
			"salaire":self.root.format_val(fiche_info.get('salaire minimum')),
			"sante":self.root.format_val(fiche_info.get('augmentation')),
			"prime":self.root.format_val(fiche_info.get('prime')),
			"support":self.root.format_val(fiche_info.get('support familiale',str())),
			"transport":self.root.format_val(fiche_info.get('indemnité',dict()).get("Transport",str())),
			"raison":fiche_info.get('objet de déduction'),
			"montant_deduc":self.root.format_val(fiche_info.get('déduction')),
			"montant_t":self.root.format_val(fiche_info.get('montant taxes appliquer',float())),
			"taux":self.root.format_val(fiche_info.get('taux taxes appliquer',float())),
			"montant_total":self.root.format_val(fiche_info.get('montant total')),
			"operateur":fiche_info.get('opérateur',self.get_curent_perso()),
			"lieu":self.sc.get_lieu(),
			"date":self.sc.get_today(),
			"nom_entreprise":ent_obj.get('sigle'),
			"tel_ent":tel,
			"email":ent_obj.get('email'),
			"adresse":adresse,
			"ifu":ent_obj.get('IFU'),
			"rccm":ent_obj.get('RCCM'),
			"logo":logo,
		}
		doc.render(data)
		doc.save(f"{fiche_info.get('N°')}.docx")
		self.root.open_link(f"{fiche_info.get('N°')}.docx")
	except:
		self.add_refused_error('Impossible!!! Vous avez un document du même nom ouvert!')

def Generer_doxs(self,file,save_f,dic):
	doc = DocxTemplate(file)
	doc.render(dic)
	doc.save(save_f)


