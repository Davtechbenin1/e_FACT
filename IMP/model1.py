from fpdf import FPDF
import os, datetime

class ProInvoiceA4:
	def __init__(self, filename="facture_modern.pdf"):
		self.filename = filename
		self.pdf = FPDF("P", "mm", "A4")
		self.pdf.set_auto_page_break(auto=True, margin=0)
		self.pdf.add_page()

		# --- Polices ---
		# Pour fpdf 1.7.2, tu dois générer les fichiers .py via makefont.py
		# Exemple :
		# python makefont.py Lexend-Regular.ttf Lexend-Regular.py
		# python makefont.py Lexend-Bold.ttf Lexend-Bold.py

		self.pdf.set_font("Arial", "", 10)

	def format_val_(self, val):
		val = str(val)
		if val:
			pref = ""
			if val[0] == "-":
				pref = "-"
				val = val[1:]
			V = val.split(".")
			if len(V) == 2:
				val = V[0]
				if int(V[-1]):
					V = "." + V[-1]
				else:
					V = ""
			else:
				val = V[0]
				V = ""
			fr = []
			part = [""] * 3
			ind = 3
			for i in range(len(val) - 1, -1, -1):
				ind -= 1
				part.insert(ind, val[i])
				if ind == 0:
					fr.append("".join(part))
					part = [""] * 3
					ind = 3
			P = "".join(part)
			if P:
				fr.append(P)
			fr.reverse()
			return pref + " ".join(fr) + V
		return val

	def format_val(self, val, virgule=1):
		try:
			float(val)
			val = round(float(val), virgule)
		except:
			return str(val)
		else:
			return self.format_val_(val)

	def add_header(self, company, invoice_no, info_str):
		self.pdf.set_font("Arial", "B", 18)
		self.pdf.set_text_color(25, 118, 210)
		self.pdf.cell(120, 10, company["name"], 0, 0, "L")

		self.pdf.set_font("Arial", "B", 20)
		self.pdf.cell(0, 10, invoice_no, 0, 1, "R")

		self.pdf.set_font("Arial", "", 9)
		self.pdf.set_text_color(0, 0, 0)
		self.pdf.multi_cell(0, 5, "%s\nTél: %s\nEmail: %s" % (
			company["address"], company["phone"], company["email"]
		))
		self.pdf.ln(-10)
		self.pdf.set_font("Arial", "", 9)
		self.pdf.multi_cell(0, 5, info_str, 0, "R")
		self.pdf.ln(5)

	def add_client_info(self, client):
		self.pdf.set_text_color(25, 118, 210)
		self.pdf.set_font("Arial", "B", 12)
		self.pdf.cell(16, 6, "Client :")
		self.pdf.set_text_color(0, 0, 0)
		self.pdf.set_font("Arial", "", 9)
		qr_code = client.get("qr_code")
		img_w, img_h = 20, 20
		page_width = self.pdf.w
		img_x = (page_width - (img_w + 10)) 
		y = self.pdf.get_y()-4

		if qr_code:
			if os.path.exists(qr_code):
				self.pdf.image(qr_code, x=img_x, y=y, w=img_w, h=img_h)

		self.pdf.multi_cell(0, 6, "%s\n%s" % (client["name"], client["address"]))
		self.pdf.ln(15)

	def add_items(self, items):
		self.pdf.set_font("Arial", "B", 10)
		self.pdf.set_fill_color(25, 118, 210)
		self.pdf.set_text_color(255, 255, 255)

		headers = ["N°", "Description", "Quantités",
		"Unité de mesures","Prix de vente", "Montant"]
		widths = [10, 70, 25, 33, 30, 22]

		for i, h in enumerate(headers):
			self.pdf.cell(widths[i], 8, h, 1, 0, "C", 1)
		self.pdf.ln()

		self.pdf.set_text_color(0, 0, 0)
		self.pdf.set_font("Arial", "", 9)
		fill = 0

		for i, art in enumerate(items, 1):
			self.pdf.set_fill_color(245, 245, 245) if fill else self.pdf.set_fill_color(255, 255, 255)
			self.pdf.cell(widths[0], 7, str(i), 1, 0, "L", fill)
			self.pdf.cell(widths[1], 7, art["desc"], 1, 0, "L", fill)
			self.pdf.cell(widths[2], 7, str(art["qty"]), 1, 0, "L", fill)
			self.pdf.cell(widths[3], 7, str(art["unité"]), 1, 0, "L", fill)
			self.pdf.cell(widths[4], 7, self.format_val(art["unit_price"]), 1, 0, "L", fill)
			self.pdf.cell(widths[5], 7, self.format_val(art["total"]), 1, 1, "L", fill)
			fill = not fill
		self.pdf.ln(5)

	def add_totals(self, subtotal, taxes, autre_mont, total):
		self.pdf.set_font("Arial", "", 9)
		self.pdf.cell(130, 6, "")
		self.pdf.cell(40, 6, "Sous-total")
		self.pdf.cell(0, 6, self.format_val(subtotal), 0, 1, "R")

		self.pdf.cell(130, 6, "")
		self.pdf.cell(40, 6, "Taxes")
		self.pdf.cell(0, 6, self.format_val(taxes), 0, 1, "R")

		self.pdf.cell(130, 6, "")
		self.pdf.cell(40, 6, "Autres Montants")
		self.pdf.cell(0, 6, self.format_val(autre_mont), 0, 1, "R")

		self.pdf.set_font("Arial", "B", 10)
		self.pdf.set_text_color(25, 118, 210)
		self.pdf.cell(130, 7, "")
		self.pdf.cell(40, 7, "Total TTC")
		self.pdf.cell(0, 7, self.format_val(total), 0, 1, "R")
		self.pdf.set_text_color(0, 0, 0)
		self.pdf.ln(8)

	def add_footer(self, img):
		self.pdf.set_y(-25)
		y = self.pdf.get_y()
		img_w, img_h = 12, 12
		page_width = self.pdf.w
		img_x = (page_width - img_w) / 2

		if os.path.exists(img):
			self.pdf.image(img, x=img_x, y=y, w=img_w, h=img_h)

		self.pdf.ln(img_h + 2)
		self.pdf.set_font("Arial", "B", 9)
		self.pdf.cell(0, 6, "Powered by ZoeCorp", 0, 1, "C")

	def build(self):
		self.pdf.output(self.filename, "F")
