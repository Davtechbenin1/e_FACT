#Coding:utf-8
"""
	Gestion des modèles de facturation
"""
from lib.davbuild import Cache_error
from reportlab.pdfgen import canvas
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Table,
	TableStyle, Spacer)

from reportlab.lib.pagesizes import A5,A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
import datetime as DAT_T
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path

# Enregistrement de la police (nom interne, fichier TTF)
pdfmetrics.registerFont(TTFont("Lexend", os.path.abspath("static/Lexend.ttf")))
pdfmetrics.registerFont(TTFont("Inter", os.path.abspath("static/Inter-Bold.ttf")))

class Model1:
	def __init__(self,mother):
		self.mother = mother
		doc_path = Path.home()
		doc_path = os.path.join(doc_path,"Documents")
		os.makedirs(doc_path,exist_ok = True)
		doc_path = os.path.join(doc_path,"ZoeCorp")
		os.makedirs(doc_path,exist_ok = True)
		doc_path = os.path.join(doc_path,"Factures")
		os.makedirs(doc_path,exist_ok = True)
		self.doc_path = os.path.join(doc_path,mother.sc.get_today())
		os.makedirs(self.doc_path,exist_ok = True)

		self.elements = list()
		self.width, self.height = A5
		self.marge_left = 20
		self.curent_Y = self.height - self.marge_left
		self.format_val = self.mother.format_val

		self.usable_width = self.width - 2*self.marge_left
		self.usable_height = self.height - 2*self.marge_left

		self.styles = getSampleStyleSheet()
		self.initialisation()

	@Cache_error
	def initialisation(self):
		self.sc = self.mother.sc
		self.cmd_dic = self.mother.cmd_dic
		self.typ = self.mother.typ
		
		f_ju = self.sc.DB.Get_ent_part("forme juridique")
		ens = f'{f_ju} "' + self.sc.DB.Get_ent_part("sigle")+'"'
		if f_ju == "SARL":
			ens = '"'+self.sc.DB.Get_ent_part("sigle")+ f'" {f_ju}'
		self.ent_infos = {
			"Enseigne":ens,
			"IFU":self.sc.DB.Get_ent_part("IFU"),
			"RCCM":self.sc.DB.Get_ent_part("RCCM"),
			"activite":"",
			"téléphone":self.sc.DB.Get_ent_part("téléphone"),
			"whatsapp":self.sc.DB.Get_ent_part('whatsapp'),
			"addresse":self.sc.DB.Get_ent_part('addresse'),
			"email":self.sc.DB.Get_ent_part('email')
		}
		self.logo = self.sc.DB.Get_ent_part('logo')
		if not self.logo:
			self.logo = "media/logo.png"

		self.bg_col = (1,1,1)
		self.txt_col = (0,0,0)
		self.gris = (.4,.4,.4)

	@Cache_error
	def set_model1(self):
		clt_dic = self.sc.DB.Get_this_clt(self.cmd_dic.get('client'))
		if clt_dic:
			self.fact_link = os.path.join(self.doc_path,f"{clt_dic.get('nom').lower()}.pdf")
			self.doc = SimpleDocTemplate(self.fact_link,
				pagesize = A5,topMargin = 15,bottomMargin = 15)

			self.Add_table()
			self.doc.build(self.elements,onFirstPage = self.Set_entete)
			self.mother.open_link(self.fact_link)
		else:
			self.sc.add_refused_error("Le client n'est pas valide!")

	@Cache_error
	def get_paragraph(self,text,font_name = "Lexend",font_size = 9,
		width = 200,text_color = "black",align = 4,
		padding_left = 5,padding_right = 5,leading = 11):
		st_perso = ParagraphStyle(name = "MyStyle",
			fontName = font_name,fontSize = font_size,
			textColor = text_color,alignment = align,
			spaceAfter = 6,leading = leading,leftIndent = padding_left,
			rigthIndent = padding_right)
		p = Paragraph(str(text), st_perso)
		max_width = width*mm
		r_w,r_h = p.wrap(max_width,100*mm)
		return p, (r_w,r_h)

	@Cache_error
	def Set_entete(self,canvas,doc):
		canvas.saveState()

		self.Gestion_parti1(canvas)
		self.Gestion_parti2(canvas)

		canvas.restoreState()

	@Cache_error
	def Add_table(self):
		art_liste = self.cmd_dic.get('articles')
		entete = ["N°",'Désignation','Qtés','PVUs','Montant',]
		wid_l = [self.usable_width*.1,self.usable_width*.35,
		self.usable_width*.2,
		self.usable_width*.15,self.usable_width*.2]
		data = [entete]
		styleN = getSampleStyleSheet()["Normal"]
		qte_dict = dict()
		self.mont_th = float()
		self.taxes = float()
		n = 0
		for dic in art_liste:
			n+=1
			des = dic.get('Désignation').replace('_',' ')
			qte = self.format_val(dic.get('qté'))
			unit = self.format_val(dic.get('unité'))
			pv_q = self.format_val(dic.get('prix qté'))
			pv_u = self.format_val(dic.get('prix unité'))
			self.mont_th += dic.get('montant HT')
			self.taxes += dic.get('taxes')

			th_qte = qte_dict.get(dic.get('qté_uni'),float())
			th_uni = qte_dict.get(dic.get('uni_uni'),float())
			th_qte += dic.get('qté')
			th_uni += dic.get('unité')
			qte_dict[dic.get("qté_uni")] = th_qte
			qte_dict[dic.get("uni_uni")] = th_uni

			if float(unit) and float(qte):
				QTE = f"{qte}<br/>{unit}"
				PVU = f"{pv_q}<br/>{pv_u}"
			elif float(unit):
				QTE = f"{unit} {dic.get('uni_uni')}"
				PVU = f"{pv_u}"
			elif float(qte):
				QTE = f"{qte} {dic.get('qté_uni')}"
				PVU = f"{pv_q}"
			lis = [
				self.get_paragraph(str(n))[0],
				self.get_paragraph(des)[0],
				self.get_paragraph(QTE)[0],
				self.get_paragraph(PVU)[0],
				self.get_paragraph(self.format_val(dic.get('montant HT')))[0],
			]
			data.append(lis)
		table = Table(data,colWidths = wid_l)
		table.setStyle(TableStyle([
			("GRID",(0,0),(-1,-1),.5,colors.black),
			("VALIGN",(0,0),(-1,-1),"MIDDLE"),
			("ALIGN",(0,0),(-1,-1),"LEFT"),
			("FONSIZE",(0,0),(-1,-1),8),
			("BACKGROUND",(0,0),(-1,0),(colors.lightgrey)),
		]))
		self.elements.append(Spacer(1,170))
		self.elements.append(table)
		self.elements.append(Spacer(1,2))
		self.add_pied(qte_dict)

	@Cache_error
	def add_pied(self,qte_dict):
		qte_str = str()
		for k,v in qte_dict.items():
			if v:
				qte_str += f" {v} {k},"
		qte_str = qte_str[:-1]
		P,size = self.get_paragraph(qte_str,align = 1)
		self.elements.append(P)
		self.elements.append(Spacer(1,2))
		mont_autre = float()
		autre_mont = self.cmd_dic.get('autre montant')
		for k,v in autre_mont.items():
			mont_autre += v

		penalite = self.cmd_dic.get("pénalité")
		
		#entete = ['Designation',"Montant"]
		th_liste = list()
		th_liste.append([self.get_paragraph("date d'émission de la facture")[0],'','',
			self.get_paragraph(self.cmd_dic.get("date d'émission"))[0]])

		wid_l = (self.usable_width*.4,self.usable_width*.2,
			self.usable_width*.2,self.usable_width*.2,)
		th_liste.append([self.get_paragraph("Montant de la facture")[0],"","",
			self.get_paragraph(self.format_val(self.mont_th))[0]])
		if autre_mont:
			liste = [[self.get_paragraph(k)[0],"","",self.get_paragraph(
				self.format_val(v))[0]] for k,v in autre_mont.items()]
			th_liste.extend(liste)
		if self.taxes:
			th_liste.append([self.get_paragraph("Taxes appliqués")[0],"","",
				self.get_paragraph(self.format_val(self.taxes))[0]])

		if penalite:
			th_liste.append([self.get_paragraph("Pénalité appliqués")[0],"","",
				self.get_paragraph(self.format_val(penalite))[0]])
		if self.taxes or autre_mont or penalite:
			th_liste.append([self.get_paragraph("Montant Total")[0],'',
				'',self.get_paragraph(self.format_val(
				self.cmd_dic.get("montant TTC")))[0]])
		
		plan_paie = self.cmd_dic.get('plan de paiements')
		if plan_paie:
			date = self.cmd_dic.get('date de traitement prévu')
			plan_date = [DAT_T.datetime.strptime(i,"%d-%m-%Y") for
				i in plan_paie if i != date]
			mont_f = plan_paie.get(date,dict()).get('montant dû')
			if mont_f:
				pourc = (int(mont_f / self.mont_th))*100
				pourc = self.cmd_dic.get('taux accompte',pourc)
				th_liste.append([self.get_paragraph('Pourcentage au comptant ')[0],
					self.get_paragraph(str(int(pourc))+"%")[0],
					self.get_paragraph("Montant")[0],
					self.get_paragraph(str(round(mont_f,0)))[0]])

			if plan_date:
				date_ech = max(plan_date).strftime("%d-%m-%Y")
				begin_ech = min(plan_date).strftime("%d-%m-%Y")
				if date_ech == begin_ech:
					...
				else:					
					th_liste.append([self.get_paragraph("date du premier échéance")[0],'','',
						self.get_paragraph(begin_ech)[0]])
					th_liste.append([self.get_paragraph("date du dernier échéance")[0],'','',
						self.get_paragraph(date_ech)[0]])
					th_liste.append([self.get_paragraph("Montant par échéance")[0],'','',
						self.get_paragraph(plan_paie.get(date_ech).get('montant dû'))[0]])
					th_liste.append([self.get_paragraph("Nombre d'échéance")[0],'','',
						self.get_paragraph(len(plan_date))[0]])

		table = Table(th_liste,colWidths = wid_l)
		table.setStyle(TableStyle([
			("GRID",(0,0),(-1,-1),.5,colors.black),
			("VALIGN",(0,0),(-1,-1),"MIDDLE"),
			("ALIGN",(0,0),(-1,-1),"LEFT"),
			("FONSIZE",(0,0),(-1,-1),8),
			
		]))
		self.elements.append(table)
		self.elements.append(Spacer(1,5))
		
		if self.cmd_dic.get('montant payé'):
			p,size = self.get_paragraph("Status du paiements",align = 1,
				font_name = 'Inter',font_size = 10)
			self.elements.append(p)
			tab = [["Montant TTC","Montant payé",'Montant restant'],
			[
				self.format_val(self.cmd_dic.get('montant TTC')),
				self.format_val(self.cmd_dic.get('montant payé')),
				self.format_val(self.cmd_dic.get('montant TTC') - self.cmd_dic.get('montant payé'))
			]]
			wid_l = self.usable_width*.33,self.usable_width*.33,self.usable_width*.34
			table = Table(tab,colWidths = wid_l)
			table.setStyle(TableStyle([
				("GRID",(0,0),(-1,-1),.5,colors.black),
				("VALIGN",(0,0),(-1,-1),"MIDDLE"),
				("ALIGN",(0,0),(-1,-1),"LEFT"),
				("FONSIZE",(0,0),(-1,-1),8),
				("BACKGROUND",(0,0),(-1,0),(colors.gray))
			]))
			self.elements.append(table)
			self.elements.append(Spacer(1,2))

	def Gestion_parti1(self,canvas):
		curent_y = self.curent_Y
		if self.cmd_dic.get("status de la commande").lower() != "livrée":
			self.typ = "PROFORMA"
		else:
			self.typ = 'FACTURE'
		typ_p,siz = self.get_paragraph(self.typ,
			'Inter',font_size = 30,align = 1)
		typ_p.drawOn(canvas, self.marge_left, curent_y-siz[1])

		enseigne = self.ent_infos.get('Enseigne')
		en_p,siz = self.get_paragraph(enseigne,
			'Inter',font_size = 20,align = 0)
		en_p.drawOn(canvas, self.marge_left, curent_y-siz[1])
		curent_y -= siz[1]*1.5

		para = f"""<br/>
			tel: {self.ent_infos.get("téléphone")} <br/>
			wht: {self.ent_infos.get('whatsapp')}<br/>
			email: {self.ent_infos.get('email')}<br/>
			IFU: {self.ent_infos.get('IFU')}<br/>
			RCCM: {self.ent_infos.get('RCCM')}
		"""
		
		p,size = self.get_paragraph(para)
		curent_y-=size[1]
		p.drawOn(canvas, self.marge_left, curent_y)
		
		self.curent_Y = curent_y-self.marge_left
		
	def Gestion_parti2(self,canvas):
		marg_l = self.marge_left+5
		self.client = self.cmd_dic.get('client')
		self.clt_dic = self.sc.DB.Get_this_clt(self.client)
		dic = {
			"Client":self.clt_dic.get("nom").replace('_',' '),
			"Association":self.clt_dic.get('association appartenue'),
			"IFU":self.clt_dic.get('IFU'),
			"Tel":self.clt_dic.get('tel'),
			"Addresse":self.sc.DB.adresse_of(self.client),
		}
		st = str()
		for k,v in dic.items():
			st+= f"{k} : {v}<br/>"
		p,f_size = self.get_paragraph(st,width = 127)

		p.drawOn(canvas, marg_l, self.curent_Y-f_size[1])
		marg_l += 127

		NUM = self.cmd_dic.get('id de la commande').split("N°")[-1]
		date,num = NUM.split("_")
		plan_date = [DAT_T.datetime.strptime(i,"%d-%m-%Y") 
			for i in self.cmd_dic.get('plan de paiements')]
		if plan_date:
			date_ech = max(plan_date).strftime("%d-%m-%Y")
		else:
			date_ech = str()
		stat = f"{self.cmd_dic.get('status de la commande')}, {self.cmd_dic.get('status du paiement')}"
		dic = {
			"Commande N°":num,
			"Date":date,
			"Echéance": date_ech,
			"Status":stat,
		}
		st = str()
		for k,v in dic.items():
			st+= f"{k} : {v}<br/>"
		p,size = self.get_paragraph(" ",width = 124)

		p.drawOn(canvas, marg_l, self.curent_Y-size[1])
		marg_l += 107

		dic = {
			"Vendeur":self.cmd_dic.get('auteur'),
			"":self.sc.get_now()
		}
		st = str()
		for k,v in dic.items():
			if k:
				st+= f"{k} : {v}<br/>"
			else:
				st+= f"{v}<br/>"
		p,s = self.get_paragraph(st,width = 137,
			text_color = "gray")

		p.drawOn(canvas, marg_l, self.curent_Y-s[1])

		canvas.rect(self.marge_left,self.curent_Y-5-f_size[1],
			self.usable_width,f_size[1]+10)

		self.curent_Y -= f_size[1]+10
