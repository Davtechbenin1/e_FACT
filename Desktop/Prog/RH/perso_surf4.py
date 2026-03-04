#Coding:utf-8
"""
	La partie "Gestion" permet la gestion des actions comme:
		- Donnée congé
		- Mise sous sanctions
		- Définition des augmentations 
		- renvoie
		- démission
		- archivage
		- promouvoire
		- changement de poste

"""
from lib.davbuild import *
from General_surf import *

class Gestion(box):
	@Cache_error
	def initialisation(self):
		self.orientation = "horizontal"
		self.padding = dp(10)
		self.size_pos()
		
	@Cache_error
	def size_pos(self):
		w,h = self.menu_size = .3,1
		self.aff_size = 1-w,h

		self.menu_surf = stack(self,size_hint = self.menu_size,
			spacing = dp(5))

		self.aff_surf = box(self,size_hint = self.aff_size)

		self.add_surf(self.menu_surf)
		self.add_surf(self.aff_surf)



class Activites(box):
	...



