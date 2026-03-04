from Mobile.root import *

# Gestion de la récupération de la liste de date
def get_date_list(self,day1,day2):
	"""
		Permet d'obtenir la liste de date d'un jour 1
		à un jour 2
	"""
	d1,m1,y1 = day1.split("-")
	d2,m2,y2 = day2.split('-')

	month_list = self._month_from_years(y1,y2)
	m_y1 = f"{m1}-{y1}"
	m_y2 = f"{m2}-{y2}"
	real_month_list = self._get_month_list(m_y1,m_y2,month_list)

	all_days_liste = self._get_all_days(real_month_list)
	real_days_liste = self._get_real_days(day1,day2,all_days_liste)
	return real_days_liste

def _month_from_years(self,y1,y2):
	y1 = int(y1)
	y2 = int(y2)
	info_liste = list()
	for y in range(y1,y2+1):
		for m in range(1,13):
			m = str(m)
			if len(m) < 2:
				m = "0"+m
			inf = f'{m}-{y}'
			info_liste.append(inf)
	return info_liste

def _get_month_list(self,m_y1,m_y2,info_liste):
	if info_liste:
		ind1 = info_liste.index(m_y1)
		ind2 = info_liste.index(m_y2)
		month_list = info_liste[ind1:ind2+1]
		return month_list
	return list()

def days_from_month(self,m,y):
	G_liste = calendar.monthcalendar(y,m)
	real_liste = list()
	for liste in G_liste:
		for d in liste:
			if d != 0:
				if len(str(d)) < 2:
					d = '0' + str(d)
				if len(str(m)) < 2:
					m = '0' + str(m)
				inf = f"{d}-{m}-{y}"
				real_liste.append(inf)
	return real_liste

def _get_all_days(self,month_list):
	gene_liste = list()
	for m_y in month_list:
		m,y = m_y.split('-')
		m = int(m)
		y = int(y)
		gene_liste.extend(self.days_from_month(m,y))
	return gene_liste

def _get_real_days(self,date1,date2,gene_days_liste):
	if gene_days_liste:
		ind1 = gene_days_liste.index(date1)
		ind2 = gene_days_liste.index(date2)
		days_liste = gene_days_liste[ind1:ind2+1]
		return days_liste
	else:
		return list()

# Calcule de date
def get_7_days(self):
	return self.get_dates_from(-7)

def get_dates_from(self,ind):
	date = self.get_today()
	j,m,y = [int(i) for i in date.split('-')]
	date_base = datetime(y,m,j)
	this_date = date_base + timedelta(days = ind)
	date2 = this_date.strftime("%d-%m-%Y")
	date_list = self.get_date_list(date2,date)
	return date_list

def get_date_f(self,ind):
	date = self.get_today()
	j,m,y = [int(i) for i in date.split('-')]
	date_base = datetime(y,m,j)
	this_date = date_base + timedelta(days = ind)
	date2 = this_date.strftime("%d-%m-%Y")
	return date2

def Sup_a(self,date1,date2):
	j1,m1,y1 = [int(i) for i in date1.split('-')]
	j2,m2,y2 = [int(i) for i in date2.split('-')]
	day1 = datetime(y1,m1,j1)
	day2 = datetime(y2,m2,j2)
	return day1 > day2

# gestion des dates
def get_today(self,normal_d = False):
	return self.real_date()

def real_date(self):
	return self.normalize_date(date_obj().date__)

def get_yerterday(self):
	date = datetime.strptime(self.get_today(),self.date_format)
	dat = date - THHHHH.timedelta(days = 1)
	return dat.strftime(self.date_format)

def _get_yerterday(self,days = 1):
	date = datetime.strptime(self.normalize_date(date_obj().date__),self.date_format)
	dat = date - THHHHH.timedelta(days = days)
	return dat.strftime(self.date_format)

def _get_day_to(self,days = 1):
	date = datetime.strptime(self.normalize_date(date_obj().date__),self.date_format)
	dat = date + THHHHH.timedelta(days = days)
	return dat.strftime(self.date_format)

def get_hour(self):
	return date_obj().hour

def get_now(self):
	return f"{self.get_today()}. {date_obj().hour}"

def normalize_date(self,date):
	date = date.replace("/","-")
	d,m,y = date.split('-')
	if len(y)==2:
		y = '20'+y
	elif len(y)==3:
		y = "2"+y
	elif len(y)==1:
		y = "202"+y
	if len(d)==1:
		d = '0'+d
	if len(m)==1:
		m = "0"+m
	text = f"{d}-{m}-{y}"
	return text
