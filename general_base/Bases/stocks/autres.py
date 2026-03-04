#Coding:utf-8

"""
	Gestion des autres paramètres de la gestion 
	de stocks
	conditionement
	grille tarifaire

"""
def conditionement_format(self):
	return {
		"id":self.Get_conditionement_ident(),
		"nom":str(),
	}

def grille_format(self):
	return {
		"id":self.Get_grille_ident(),
		"nom":str(),
	}

def save_conditionements(self,dic):
	return self.save_part_parametre("conditionement",dic)

def save_grilles(self,dic):
	return self.save_part_parametre("grille",dic)

def get_conditionements(self,ident = None):
	return self.get_part_parametre("conditionement",ident)

def get_grilles(self,ident = None):
	return self.get_part_parametre("grille",ident)

def get_part_parametre(self,part,ident = None):
	part_dic = self.Get_general_data(self.autres_par).get(part,dict())
	if ident:
		return part_dic.get(ident)
	else:
		return part_dic

def save_part_parametre(self,part,dic):
	part_d = self.get_part_parametre(part)
	part_d[dic.get('id')] = dic
	all_part = self.Get_general_data(self.autres_par)
	all_part[part] = part_d
	self.Save_general_data(self.autres_par,all_part)
