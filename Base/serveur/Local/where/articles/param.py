#Coding:utf-8
condition_fic = "conditions"
grille_fic = "grille"

def conditionement_format(self):
	return {
		"id":self.get_ident_of(self.condition_fic,False),
		"nom":str(),
	}

def grille_format(self):
	return {
		"id":self.get_ident_of(self.grille_fic,False),
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
	part_dic = self._get_data_from(part)
	if ident:
		return part_dic.get(ident)
	else:
		return part_dic

def save_part_parametre(self,part,dic):
	ident = dic.get('id')
	self._save_data_to(part,ident,dic)
