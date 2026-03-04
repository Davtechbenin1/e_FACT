#Coding:utf-8
"""
	Module de gestion de la partie connexion à la base générale
	de l'entreprise.
	Cette partie permet de se connecté à l'interface de 
	l'entreprise et aussi de générer les modules à prendre
	en compte par l'entreprise.
"""
from lib.davbuild import *
from General_surf import *
from .root import root

import smtplib, ssl, socket
from email.message import EmailMessage

from random import choice
from general_base.Table_base import Gen_Base_table as gene_tab

class Con_part(box):
	def initialisation(self):
		self.th_h = .13
		self.t_padd_h = .75
		self.spacing = dp(10)
		self.th_ent = self.sc.Get_local('Info_gene')
		self.email = str()
		self.curent_version = "2026.0.0"
		self.th_code = str()
		self.size_pos()

		Clock.schedule_once(lambda dt:self.Foreign_surf(),3)

		#self.add_all()


	def size_pos(self):
		self.th_vir_b = float_l(self)
		self.th_vir_b.add_image("media/acc2.png",keep_ratio = False)
		self.add_surf(self.th_vir_b)

	def Foreign_surf(self):
		#self.th_vir_b.clear_widgets()
		self.cont_surf = stack(self,radius = (dp(20)),
			spacing = dp(10),size_hint = (.25,.35),
			pos_hint = (.6,.4),
			padding = dp(10),bg_color = self.sc.aff_col1)

		self.th_vir_b.add_surf(self.cont_surf)
		
		if not self.th_ent:
			self.set_email_part()
		else:
			#self.close_modal()
			self.open_real_app()
		

	def get_curent_vers(self):
		if float(self.sc.get_today().split('-')[1]) > 3.0:
			return "2026.0.1"
		else:
			return self.curent_version

	def set_update_srf(self):
		h = self.th_h
		self.cont_surf.add_text("",size_hint = (1,h*self.t_padd_h))
		self.cont_surf.add_text(f"""La version {self.get_curent_vers()}\
de ZoeCorp est déjà disponible. Veillez obtenir votre copie gratuitememnt""",
			size_hint = (1,h*2),text_color = self.sc.green,
			bold = True,italic = True,halign = "center",
			font_size = "16sp")
		
		self.cont_surf.add_padd((.3,h))
		but_info = self.cont_surf.add_button('Télécharger',
			size_hint = (.4,h),bg_color = self.sc.orange,
			text_color = self.sc.white,on_press = self.get_cur
			)
		self.sc.set_default_button(but_info)
		self.error_srf = self.cont_surf.add_text('',size_hint = (1,h*3),
			text_color = self.sc.red, italic = True,
			bold = True,halign = "center")

	def set_email_part(self):
		h = self.th_h
		self.cont_surf.clear_widgets()
		self.cont_surf.add_text("",size_hint = (1,h*self.t_padd_h))
		self.cont_surf.add_text('Connexion / Inscription',
			size_hint = (1,h),text_color = self.sc.green,
			bold = True,italic = True,halign = "center",
			font_size = "16sp")
		self.cont_surf.add_padd((.2,h))
		cont,self.inp_surf = Get_border_input_surf(self.cont_surf,"email",
			size_hint = (.6,h),
			bg_color = self.sc.aff_col1,border_col = self.sc.orange,
			default_text = self.email,on_text = self.set_email,
			)
		self.cont_surf.add_padd((.3,h))
		self.but_info = self.cont_surf.add_button('',
			size_hint = (.4,h),bg_color = self.sc.orange,
			text_color = self.sc.white,
			)
		self.sc.set_default_button(self.but_info)
		self.error_srf = self.cont_surf.add_text('',size_hint = (1,h*3),
			text_color = self.sc.red, italic = True,
			bold = True,halign = "center")

		self.set_normal_info()
		self.error_srf.text = str()

	def set_code_surf(self):
		self.cont_surf.clear_widgets()
		h = self.th_h
		self.cont_surf.add_text("",size_hint = (1,h*self.t_padd_h))
		self.cont_surf.add_text('Votre code de vérification',
			size_hint = (1,h),text_color = self.sc.green,
			bold = True,italic = True,halign = "center",
			font_size = "16sp")
		self.cont_surf.add_padd((.2,h))
		Get_border_input_surf(self.cont_surf,"code",
			size_hint = (.6,h),
			bg_color = self.sc.aff_col1,border_col = self.sc.orange,
			default_text = self.th_code,on_text = self.set_th_code,
			)
		self.cont_surf.add_padd((.2,h))
		self.cont_surf.add_padd((.3,h))
		but_srf = self.cont_surf.add_button('code non reçus?',size_hint = (.4,h),
			bg_color = None,text_color = self.sc.orange)
		but_srf.on_press = self.add_all

		self.error_srf = self.cont_surf.add_text('',size_hint = (1,h*3),
			text_color = self.sc.red, italic = True,
			bold = True,halign = "center")
		
	

# Gestion des actions des boutons
	def set_email(self,wid,val):
		self.email = val
		self.set_normal_info()

	def set_normal_info(self):
		if not self.email.endswith("@gmail.com"):
			self.inp_surf.color = self.sc.red
			self.error_srf.text = "Email incomplet ou non valide"
			self.but_info.text = ""
			self.but_info.on_press = self.noting
		else:
			self.inp_surf.color = self.sc.text_col1
			self.error_srf.text = str()
			self.but_info.text = "Envoyer le code"
			self.but_info.on_press = self.set_code

	def get_cur(self,wid):
		...

	def set_code(self,*args):
		self.excecute(self.send_code)
		#self.send_code()

		self.set_code_surf()

	def set_th_code(self,wid,val):
		if val == self.code:
			self.sc.excecute(self.__send_info_to)
			self.sc.Save_local('Info_gene',self.email.split("@")[0])
			self.open_real_app()
		elif len(val) >= 6:
			self.error_srf.text = "Code non valide!!!"
		else:
			self.error_srf.text = str()

	def __send_info_to(self,*args):
		app_base = gene_tab(self.sc)
		app_base.add_client(self.email)


	def open_real_app(self):
		self.sc.lanch_app()

			

	def noting(self,*args):
		...

	def send_code(self):
		self.code = code = self.generate_code(6)
		try:
			mot_pass = "vwclydxvrpgpfxdu"
			msg = EmailMessage()
			msg['Subject'] = "Code de confirmation ZoeCorp"
			msg["From"] = "davtech2025@gmail.com"
			msg["To"] = self.email
			msg.set_content(f"""
	Code de confirmation \n 			 {code}				 \n
	Merci pour la confiance
	""")
			context = ssl.create_default_context()
			with smtplib.SMTP_SSL('smtp.gmail.com',465,context = context) as serveur:
				serveur.login("davtech2025@gmail.com",mot_pass)
				serveur.send_message(msg)
		except socket.gaierror:
			Clock.schedule_once(self.set_con_error,2)
		print(code)

	def set_con_error(self,*args):
		self.sc.add_refused_error("Erreur de connexion!\n Veillez vérifier votre connexion internet",
			text_color = self.sc.red,italic = True,
			halign = "center")


	@Cache_error
	def generate_code(self,lenf):
		if isinstance(lenf,str):
			lenf = int(self.regul_input(lenf))
		liste = [1,2,3,4,5,6,7,8,9,0]
		th_l = [choice(liste)]
		while len(th_l) < lenf:
			th_l.append(choice(liste))
		return "".join([str(i) for i in th_l])






