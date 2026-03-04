"""
	Module de définition des méthodes de gestion du e-MECEF
"""
from __future__ import print_function
from swagger_client import Configuration, ApiClient, SfeInfoApi
import sys
import qrcode
import swagger_client
from swagger_client.models import (
	InvoiceRequestDataDto, OperatorDto, TaxGroupsDto, ItemDto, PaymentDto,
	InvoiceTypeEnum, TaxGroupTypeEnum
)

from swagger_client.rest import ApiException
from pprint import pprint

def tester_connexion_emecf(self,api_key, 
	host='https://developper.impots.bj/sygmef-emcf'):
	config = Configuration()
	config.api_key['Authorization'] = f'Bearer {api_key}'
	config.host = host

	try:
		client = ApiClient(config)
		info_api = SfeInfoApi(client)
		statut = info_api.api_info_status_get()
		return {
			'success': True,
			'status': statut.status,
		}
	except Exception as e:
		return {
			'success': False,
			'error': str(e)
		}

def normalise_fact(self, cmd_dic):
	if not self.sc.DB.Get_ent_part("verifier"):
		return False

	token = self.sc.DB.Get_ent_part("tocken eMECeF")
	if not token or not cmd_dic:
		return False

	invoice_req = InvoiceRequestDataDto()

	clt_dic = self.sc.DB.Get_this_clt(cmd_dic.get('client'))
	if clt_dic:
		client_dto = swagger_client.ClientDto()
		client_dto.name = clt_dic.get("nom", "Client")
		client_dto.ifu = clt_dic.get("IFU", "")
		invoice_req.client = client_dto
	else:
		self.add_refused_error('Facture non valide!!')
		return False

	if not token.startswith("Bearer "):
		token = "Bearer " + token
	configuration = swagger_client.Configuration()
	configuration.api_key['Authorization'] = token
	configuration.host = 'https://sygmef.impots.bj/emcf'

	api_instance = swagger_client.SfeInvoiceApi(swagger_client.ApiClient(configuration))

	
	invoice_req.invoiceNumber = cmd_dic.get('N°') or cmd_dic.get('id de la commande')

	invoice_req.ifu = self.sc.DB.Get_ent_part("IFU")
	invoice_req.type = InvoiceTypeEnum.FV
	invoice_req.reference = cmd_dic.get("client") or invoice_req.invoiceNumber


	operator = OperatorDto()
	operator.name = cmd_dic.get("auteur") or "Opérateur Test"
	invoice_req.operator = operator

	tax_groups = TaxGroupsDto()
	tax_groups.group_a = 0
	tax_groups.group_b = 18
	tax_groups.group_c = 0
	tax_groups.group_d = 18
	tax_groups.group_aib_a = 1
	tax_groups.group_aib_b = 5
	invoice_req.tax_groups = tax_groups

	invoice_req.items = self.Get_items(cmd_dic.get('articles', []))

	autre_mont = self.get_autr_m(cmd_dic.get('autre montant', {}))
	invoice_req.payments = self.Get_all_paiem(cmd_dic.get('paiements', []), autre_mont)
	try:
		api_response = api_instance.api_invoice_post(body=invoice_req)
		#pprint(api_response)
		return api_response

	except ApiException as e:
		print("Erreur lors de l'envoi facture e-MECEF : %s\n" % e)
		return False


def Get_items(self, articles):
	items = []
	for art in articles:
		desc = art.get('Désignation', '').replace("_", " ")
		tax_g = TaxGroupTypeEnum.A
		if 'TVA' in art.get('taxes enable'):
			tax_g = TaxGroupTypeEnum.B

		if art.get('qté'):
			item = ItemDto()
			item.name = f"{art.get('qté_uni', '')} de {desc}"
			item.quantity = art.get('qté')
			item.price = art.get('prix qté')
			item.tax_group = tax_g
			items.append(item)

		if art.get('unité'):
			item = ItemDto()
			item.name = f"{art.get('uni_uni', '')} de {desc}"
			item.quantity = art.get('unité')
			item.price = art.get('prix unité')
			item.tax_group = tax_g
			items.append(item)
	return items

def Get_payments_of(self, pay_ident, deduc=0):
	pay = PaymentDto()
	pay.payment_type = "CASH"
	pay.amount = 0.0
	if pay_ident:
		pay_dic = self.sc.DB.Get_this_paie_info(pay_ident)
		if pay_dic:
			mode = pay_dic.get('mode de paiement', "CASH").upper()
			pay.payment_type = mode
			montant = pay_dic.get('montant payé', 0.0) - float(deduc)
			pay.amount = montant if montant > 0 else 0.0
	return pay

def Get_all_paiem(self, paiements, autre_mont):
	payments = []
	if paiements:
		first = paiements[0]
		payments.append(self.Get_payments_of(first, autre_mont))
		for ident in paiements[1:]:
			payments.append(self.Get_payments_of(ident))
	else:
		default_payment = PaymentDto()
		default_payment.payment_type = "CASH"
		default_payment.amount = float()
		paiements = [default_payment]
	return payments

def Confirmation_normaliser(self,cmd_dic):
	if not self.sc.DB.Get_ent_part("verifier"):
		return False

	token = self.sc.DB.Get_ent_part("tocken eMECeF")
	if not token or not cmd_dic:
		return False
	if not token.startswith("Bearer "):
		token = "Bearer " + token
	configuration = swagger_client.Configuration()
	configuration.api_key['Authorization'] = token
	configuration.host = 'https://sygmef.impots.bj/emcf'
	api_invoice_instance = swagger_client.SfeInvoiceApi(
		ApiClient(configuration=configuration))

	operator = OperatorDto()
	operator.name = cmd_dic.get("auteur") or "Opérateur Test"
	try:
		uid = cmd_dic.get("uid_emecf")
		details = api_invoice_instance.api_invoice_uid_get(uid)
		
		sec_el_det = api_invoice_instance.api_invoice_uid_confirm_put(uid)
		pprint(sec_el_det)
		dic = {
			'code_me_ce_fdgi': sec_el_det.code_me_ce_fdgi,
			'counters': sec_el_det.counters,
			'date_time': sec_el_det.date_time,
			'error_code': sec_el_det.error_code,
			'error_desc': sec_el_det.error_desc,
			'nim': sec_el_det.nim,
			'qr_code': sec_el_det.qr_code,
		}
		if dic["qr_code"]:
			return dic
			
		else:
			self.add_refused_error("⚠️ La facture n’a pas été validée. Statut :")
			return False

	except Exception as e:
		print(e)
		self.add_refused_error("❌ Erreur reseau lors de la validation de la facture")
		return False


def get_autr_m(self, dic):
	val = 0.0
	for k, v in dic.items():
		val += float(v)
	return val

def QR_code(self,data,fact_num):
	# Création du QR code
	qr = qrcode.QRCode(
		version=1,  # taille du QR code (1 à 40)
		error_correction=qrcode.constants.ERROR_CORRECT_M,
		box_size=10,
		border=4,
	)

	qr.add_data(data)
	qr.make(fit=True)

	# Génération de l'image
	img = qr.make_image(fill_color="black", back_color="white")

	# Sauvegarde ou affichage
	img_name = f"static/{fact_num}.png"
	img.save(img_name)
	return img_name
