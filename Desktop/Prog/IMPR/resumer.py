#Coding:utf-8
"""
	Impression des résumées. on utilise le principe du tableau
"""
from reportlab.pdfgen import canvas
from lib.davbuild import Cache_error
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Table,
	TableStyle, Spacer)

from reportlab.lib.pagesizes import A5,A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from datetime import datetime as DAT_T
import os,sys
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from operator import itemgetter
from pathlib import Path

# Enregistrement de la police (nom interne, fichier TTF)
pdfmetrics.registerFont(TTFont("Lexend", os.path.abspath("static/Lexend.ttf")))
pdfmetrics.registerFont(TTFont("Inter", os.path.abspath("static/Inter-Bold.ttf")))

class Resumer:
	def __init__(self,mother,titre,info,forma):
		self.mother = mother
		self.sc = self.mother.sc
		self.SCREEN = self.sc
		self.titre = titre
		self.info = info
		doc_path = Path.home()
		doc_path = os.path.join(doc_path,"Documents")
		os.makedirs(doc_path,exist_ok = True)
		doc_path = os.path.join(doc_path,"ZoeCorp")
		os.makedirs(doc_path,exist_ok = True)
		doc_path = os.path.join(doc_path,"Résumer")
		os.makedirs(doc_path,exist_ok = True)
		self.doc_path = os.path.join(doc_path,mother.sc.get_today().replace("-",""))
		os.makedirs(self.doc_path,exist_ok = True)

		self.fact_link = os.path.join(self.doc_path,f"{titre}.pdf")


		if forma.lower() == 'portrait':
			self.size = A4
		else:
			self.size = landscape(A4)
		self.doc = SimpleDocTemplate(self.fact_link,
			pagesize = self.size,topMargin = 15,bottomMargin = 15)
		self.elements = list()
		self.width, self.height = self.size
		self.marge_left = 20
		self.curent_Y = self.height - self.marge_left
		self.format_val = self.mother.format_val

		self.usable_width = self.width - 2*self.marge_left
		self.usable_height = self.height - 2*self.marge_left

		self.styles = getSampleStyleSheet()
		self.initialisation()

	def Sort_infos(self,liste,part):
		key_s = "SORTING_INDFFF"
		th_l = list()
		for dic in liste:
			info = dic.get(part)
			try:
				inf = DAT_T.strptime(info,"%d-%m-%Y")
			except Exception as e:
				try:
					inf = float(info)
				except:
					if info:
						inf = info.lower()
					else:
						inf = "None"
			dic[key_s] = inf
			th_l.append(dic)
		try:
			th_l.sort(key = itemgetter(key_s))
		except:
			print(3333)
		ind = 0

		for k in th_l:
			ind += 1
			if key_s in k:
				k.pop(key_s)
			k['NUM'] = str(ind)
		return th_l

	@Cache_error
	def initialisation(self):
		f_ju = self.sc.DB.Get_ent_part("forme juridique")
		ens = f'{f_ju} "' + self.sc.DB.Get_ent_part("sigle")+'"'
		if f_ju == "SARL":
			ens = '"'+self.sc.DB.Get_ent_part("sigle")+ f'" {f_ju}'
		self.ent_infos = {
			"Enseigne":ens,
			"IFU":self.sc.DB.Get_ent_part("IFU"),
			"RCCM":self.sc.DB.Get_ent_part("RCCM"),
			"activite":self.sc.DB.Get_ent_part("F. principal"),
			"téléphone":self.sc.DB.Get_ent_part("téléphone"),
			"whatsapp":self.sc.DB.Get_ent_part('whatsapp'),
			"addresse":self.sc.DB.Get_ent_part('addresse')
		}
	
	def Create(self,wid_l,entete,liste):
		liste = self.Sort_infos(liste,entete[0])
		self.Add_table(wid_l,entete,liste)
		self.doc.build(self.elements,onFirstPage = self.Set_entete)
		self.mother.open_link(self.fact_link)

	def get_paragraph(self,text,font_name = "Lexend",font_size = 9,
		width = 200,text_color = "black",align = 0,
		padding_left = 5,padding_right = 5,leading = 13):
	#
		st_perso = ParagraphStyle(name = "MyStyle",
			fontName = font_name,fontSize = font_size,
			textColor = text_color,alignment = align,
			spaceAfter = 6,leading = leading,leftIndent = padding_left,
			rigthIndent = padding_right)
		p = Paragraph(text, st_perso)
		max_width = width*mm
		r_w,r_h = p.wrap(max_width,100*mm)
		return p, (r_w,r_h)

	@Cache_error
	def Set_entete(self,canvas,doc):
		canvas.saveState()

		self.Gestion_parti1(canvas)

		canvas.restoreState()

	@Cache_error
	def Add_table(self,wid_l,entete,liste):
		wid_l = list(wid_l)
		entete.insert(0,"NUM")
		N_w = .05
		wi0 = wid_l[0]-N_w
		wid_l.insert(0,N_w)
		wid_l[1] = wi0
		wid_l = [self.usable_width*i for i in wid_l]
		origin_ent = [i for i in entete]
		entete = [self.get_paragraph(i.upper(),"Inter"
			,width = w,font_size = 8,
			padding_left = 1)[0] 
			for i,w in zip(origin_ent,wid_l)]
		tab_liste = [entete]
		
		for dic in liste:
			lis = [self.get_paragraph(self.mother.format_val(
				dic.get(i,str())),width = w,font_size = 8,
			padding_left = 1,leading = 10,)[0]
				for i,w in zip(origin_ent,wid_l)]
			tab_liste.append(lis)

		table = Table(tab_liste,colWidths = wid_l)
		table.setStyle(TableStyle([
			("GRID",(0,0),(-1,-1),.5,colors.black),
			("VALIGN",(0,0),(-1,-1),"MIDDLE"),
			("ALIGN",(0,0),(-1,-1),"LEFT"),
			("BACKGROUND",(0,0),(-1,0),(colors.lightgrey)),
		]))
		space = self.height - self.curent_Y
		curent_y = self.curent_Y
		last_info = f"{self.sc.get_curent_perso()}<br/>Date d'impression: {self.sc.get_now()}"
		p,size = self.get_paragraph(last_info,align = 0,font_size = 8,
			padding_left = self.usable_width-350,width = self.usable_width)
		curent_y-=size[1]*1.1
		self.elements.append(Spacer(1,space+40))
		self.elements.append(p)
		
		self.elements.append(table)
		self.elements.append(Spacer(1,2))

	def Gestion_parti1(self,canvas):
		curent_y = self.curent_Y
		entreprise = self.ent_infos.get("Enseigne")
		typ_p,siz = self.get_paragraph(entreprise,
			'Inter',font_size = 25,align = 0,
			width = self.usable_width,
			padding_left = self.usable_width-200)
		typ_p.drawOn(canvas, self.marge_left, curent_y-siz[1])

		en_p,siz = self.get_paragraph(self.titre,
			'Inter',font_size = 15,align = 0,)
		en_p.drawOn(canvas, self.marge_left, curent_y-siz[1])
		curent_y -= siz[1]*1.5
		
		p,size = self.get_paragraph(self.info,font_size = 8,
			)
		curent_y-=size[1]*1.1
		p.drawOn(canvas, self.marge_left, curent_y)
		curent_y-= 15
		
		self.curent_Y = curent_y-self.marge_left

class Th_Fiche(Resumer):
	@Cache_error
	def Create(self,wid_l,entete,liste,total_ent):
		self.total_ent = list(total_ent)
		self.total_ent.insert(0,"Total")
		liste = self.Sort_infos(liste,entete[0])
		self.Add_table(wid_l,entete,liste)
		self.doc.build(self.elements,onFirstPage = self.Set_entete)
		self.mother.open_link(self.fact_link)

	@Cache_error
	def Add_table(self,wid_l,entete,liste):
		wid_l = list(wid_l)
		entete.insert(0,"NUM")
		N_w = .05
		wi0 = wid_l[0]-N_w
		wid_l.insert(0,N_w)
		wid_l[1] = wi0
		wid_l = [self.usable_width*i for i in wid_l]
		origin_ent = [i for i in entete]
		entete = [self.get_paragraph(i.upper(),"Inter"
			,width = w,font_size = 8,
			padding_left = 1)[0] 
			for i,w in zip(origin_ent,wid_l)]
		tab_liste = [entete]
		self.Total_dict = dict()
		nbre = 0
		
		for dic in liste:
			nbre += 1
			lis = list()
			for i,w in zip(origin_ent,wid_l):
				val = dic.get(i,str())
				lis.append(self.get_paragraph(self.mother.format_val(
					val),width = w,font_size = 8,
				padding_left = 1,leading = 10,)[0])
				if i in self.total_ent:
					vla_conv = self.Convert_to_float(val)
					if vla_conv:
						qte = self.Total_dict.get(i)
						if not qte:
							qte = float()
						qte += vla_conv
						self.Total_dict[i] = qte
			tab_liste.append(lis)
		self.Total_dict['Total'] = nbre

		table = Table(tab_liste,colWidths = wid_l)
		table.setStyle(TableStyle([
			("GRID",(0,0),(-1,-1),.5,colors.black),
			("VALIGN",(0,0),(-1,-1),"MIDDLE"),
			("ALIGN",(0,0),(-1,-1),"LEFT"),
			("BACKGROUND",(0,0),(-1,0),(colors.lightgrey)),
		]))
		space = self.height - self.curent_Y
		curent_y = self.curent_Y
		last_info = f"{self.sc.get_curent_perso()}<br/>Date d'impression: {self.sc.get_now()}"
		p,size = self.get_paragraph(last_info,align = 0,font_size = 8,
			padding_left = self.usable_width-350,width = self.usable_width)
		curent_y-=size[1]*1.1
		self.elements.append(Spacer(1,space+40))
		self.elements.append(p)
		
		self.elements.append(table)
		self.elements.append(Spacer(1,8))
		self.elements.append(self.get_paragraph('Les totaux',align = 1,
			font_size = 9,width = self.usable_width,leading = 10)[0])
		widths = [self.usable_width /(len(self.total_ent)*1.5)]*len(self.total_ent)
		
		th_l = list()
		for i,w in zip(self.total_ent,widths):
			tup = self.get_paragraph(str(i),width = w,font_size = 8,
				padding_left = 1, leading = 10,align = 1)
			th_l.append(tup[0])
		th_ll = list()
		for i,w in zip(self.total_ent,widths):
			tup = self.get_paragraph(self.mother.format_val(self.Total_dict.get(i,
				float())),width = w,font_size = 8, padding_left = 1,
				leading = 10,align = 1)
			th_ll.append(tup[0])

		LLL = [th_l,th_ll]

		th_table = Table(LLL,colWidths = widths)
		th_table.setStyle(TableStyle([
			("GRID",(0,0),(-1,-1),.5,colors.black),
			("VALIGN",(0,0),(-1,-1),"MIDDLE"),
			("ALIGN",(0,0),(-1,-1),"LEFT"),
			("BACKGROUND",(0,0),(-1,0),(colors.white)),
		]))
		self.elements.append(th_table)

	def Convert_to_float(self,val):
		th_v = val
		val = str(val).replace(" ",'_')
		if val:
			try:
				val = float(val)
			except ValueError:
				print(val)
				val = float(val.split('_')[0])
			except:
				val = None
		else:
			val = 0
		return val


