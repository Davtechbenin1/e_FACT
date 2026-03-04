#Coding:utf-8
from Mobile.root import *
def add_modal_surf(self,surf,titre = "Alerte système",auto_dismiss = True,
	show_close = True,radius = dp(10),bg_color = 'None',
	overlay_color = None,**kwargs):
#
	if bg_color == "None":
		bg_color = self.sc.aff_col3
	if not overlay_color:
		overlay_color = self.sc.overlay_color
	try:
		th_surf = self.get_modal_surf(surf,titre,show_close,self.close_modal,
			bg_color = bg_color,radius = radius)
		self.modal = ModalView(auto_dismiss = auto_dismiss,
			overlay_color = overlay_color,**kwargs)
		self.modal.add_widget(th_surf)

	except Exception as E:
		print(E)
		self.close_modal()
		th_surf = self.get_modal_surf(surf,titre,show_close,self.close_modal,
			bg_color = bg_color)
		self.modal = ModalView(auto_dismiss = auto_dismiss,
			overlay_color = overlay_color,**kwargs)
		self.modal.add_widget(th_surf)

	self.sc.add_to_modal(self.modal)
	self.modal.open()

def get_modal_surf(self,surf,titre,show_close,close_fonc,bg_color,radius = dp(10)):
	padd = dp(5)
	if not bg_color:
		padd = 0
	th_surf = box(self,bg_color = self.sc.aff_col1,
		padding = padd,radius = radius)
	title = box(self,size_hint = (1,None),height = dp(40),
		orientation = 'horizontal',bg_color = self.aff_col1)
	title.add_icon_but(icon = "keyboard-backspace",
			text_color = self.sc.text_col1,
			on_press = close_fonc,size_hint = (None,1),
			font_size = '24sp',size = (dp(30),dp(1)))
	title.add_text(titre,text_color = self.sc.text_col1,
		size_hint = (.9,1),
		)
	if show_close:
		th_surf.add_surf(title)
	th_surf.add_surf(surf)
	return th_surf

def close_modal(self,*args):
	self.modal.dismiss()
	self.sup_from_modal(self.modal)

def add_refused_error(self,text,**kwargs):
	bo = stack(self,bg_color = self.sc.aff_col1,
		radius = dp(10))
	if not kwargs.get('text_color'):
		kwargs['text_color'] = self.sc.orange

	if not kwargs.get('halign'):
		kwargs['halign'] = "center"
	
	bo.add_text(text,**kwargs)
	
	self.add_modal_surf(bo,titre = "Alerte système",size_hint = (.8,.3),
		radius = dp(10), pos_hint = {"x":.1,"y":.5})

def set_confirmation_srf(self,exec_fonc):
	Conf_s = Confirmation_srf(self,bg_color = self.aff_col1,
		radius = dp(10))
	Conf_s.font_s = "11sp"
	Conf_s.add_all(exec_fonc)
	self.add_modal_surf(Conf_s,size_hint = (.8,.3),
		pos_hint = {"x":.1,"y":.5})

def add_to_modal(self,wid):
	self._modal_surf_list.append(wid)

def sup_from_modal(self,wid):
	if wid in self._modal_surf_list:
		self._modal_surf_list.remove(wid)

def get_curent_modal(self):
	if self._modal_surf_list:
		return self._modal_surf_list[-1]
	else:
		return None

def Confirmation(self,title,text1,text2,accept_fonc,dismis_fonc = None,
	but_liste = ["Rester","Merci"]):
	close_b = box(self,bg_color = self.aff_col1)
	
	close_b.add_text(text2,size_hint = (1,.7),text_color = self.orange,
		halign = 'center',font_size = "20",italic = True)
	but_st = stack(self,size_hint = (1,.3),spacing = dp(15),
		padding = dp(10))
	but_st.add_padd((.4,1))

	def annuler(*a):
		self.close_modal()

	if not dismis_fonc:
		dismis_fonc = annuler
	
	but_st.add_button(but_liste[0],text_color = self.text_col3,
		bg_color = self.green,size_hint = (.25,1),on_press = dismis_fonc,
		radius = dp(20))
	but_st.add_padd((.05,1))
	th_bu = but_st.add_button(but_liste[1],text_color =self.text_col3,
		bg_color = self.red,size_hint = (.25,1),on_press = accept_fonc,
		radius = dp(20))
	self.set_default_button(th_bu)
	close_b.add_surf(but_st)
	self.add_modal_surf(close_b,size_hint = (.25,.25),
		titre = "Confirmation",auto_dismiss = True)
