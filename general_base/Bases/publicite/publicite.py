#Coding:utf-8
def get_acc_imgs(self):
	pub_imgs = self.get_all_pub_imgs()
	return pub_imgs.get('accueil pub',[("media/logo.png",'')])

def save_acc_imgs(self,url,lien):
	url = self.Save_image(url)
	pub_imgs = self.get_all_pub_imgs()
	acc_imgs = pub_imgs.get('accueil pub',list())
	acc_imgs.append((url,lien))
	pub_imgs['accueil pub'] = acc_imgs
	self.Save_general_data(self.pub_fic, pub_imgs)

def sup_acc_imgs(self,url,lien):
	url = self.Save_image(url)
	pub_imgs = self.get_all_pub_imgs()
	acc_imgs = pub_imgs.get('accueil pub',list())
	new_acc_imgs = list()
	for tup in acc_imgs:
		if url != tup[0]:
			new_acc_imgs.append(tup)

	pub_imgs['accueil pub'] = new_acc_imgs
	self.Save_general_data(self.pub_fic, pub_imgs)

def get_all_pub_imgs(self):
	pub_imgs = self.Get_general_data(self.pub_fic)
	if not pub_imgs:
		pub_imgs = dict()
	return pub_imgs

def get_curent_mobile_version(self):
	vers = self.Get_general_data(self.version_fic)
	if not vers:
		vers = {
			"version":"1.0.1",
			"apk_url":"https://github.com/Davtechbenin1/Progest/releases/download/V1.0.0/zoeshop.apk"
		}
	return vers

def set_version_infos(self,dic):
	self.Save_general_data(self.version_fic,dic)

	