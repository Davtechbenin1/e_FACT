#Coding:utf-8
"""
	Gestion des historiques des commandes
"""
def save_cmd_non_solder(self,where,cmd_ident):
	ident = 'non_solder'
	th,part = where.split('_z_o_e_')
	where = f'historiquecmd_z_o_e_{part}'
	n_solder_dic = self.get_cmd_non_solder(where).get('data')
	solder_dic = self.get_cmd_solder(where).get('data')
	if cmd_ident in solder_dic:
		solder_dic.pop(cmd_ident)
		self.save_data(where,solder_dic,'solder')
	if cmd_ident not in n_solder_dic:
		n_solder_dic[cmd_ident] = cmd_ident
		self.save_data(where,n_solder_dic,ident)

def delete_cmd_non_solder(self,where,cmd_ident):
	ident = 'non_solder'
	th,part = where.split('_z_o_e_')
	where = f'historiquecmd_z_o_e_{part}'
	n_solder_dic = self.get_cmd_non_solder(where).get('data')
	if cmd_ident in n_solder_dic:
		n_solder_dic.pop(cmd_ident)
		self.save_data(where,n_solder_dic,ident)

def delete_cmd_solder(self,where,cmd_ident):
	ident = 'solder'
	th,part = where.split('_z_o_e_')
	where = f'historiquecmd_z_o_e_{part}'
	solder_dic = self.get_cmd_solder(where).get('data')
	if cmd_ident in solder_dic:
		solder_dic.pop(cmd_ident)
		self.save_data(where,solder_dic,ident)
	
def save_cmd_solder(self,where,cmd_ident):
	ident = 'solder'
	th,part = where.split('_z_o_e_')
	where = f'historiquecmd_z_o_e_{part}'
	n_solder_dic = self.get_cmd_non_solder(where).get('data')
	solder_dic = self.get_cmd_solder(where).get('data')
	if cmd_ident not in solder_dic:
		solder_dic[cmd_ident] = cmd_ident
		self.save_data(where,solder_dic,ident)
	if cmd_ident in n_solder_dic:
		n_solder_dic.pop(cmd_ident)
		self.save_data(where,n_solder_dic,"non_solder")

def get_cmd_non_solder(self,where):
	ident = "non_solder"
	return self._cmd_hist(where,ident)

def get_cmd_solder(self,where):
	ident = "solder"
	return self._cmd_hist(where,ident)

def _cmd_hist(self,where,ident):
	th,part = where.split('_z_o_e_')
	where = f'historiquecmd_z_o_e_{part}'
	dic = self.get_data(where,ident)
	return dic
