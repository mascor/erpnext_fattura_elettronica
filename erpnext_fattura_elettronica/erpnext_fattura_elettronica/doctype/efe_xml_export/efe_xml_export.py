# -*- coding: utf-8 -*-
# Copyright (c) 2018, Massimiliano Corvino and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from lxml import etree as ET
from frappe.contacts.doctype.address.address import get_default_address
from frappe.contacts.doctype.contact.contact import get_default_contact
from erpnext.controllers.taxes_and_totals import get_itemised_tax
import json, os
from frappe.utils.file_manager import save_file
from frappe.model.naming import make_autoname

# Variable names used in this doctype are from the italian names.
class EFEXMLExport(Document):
	def generate_electronic_invoices(self):
		filters = {
			"posting_date": ("between", [self.from_date, self.to_date]),
			"company": self.company,
			"docstatus": 1
		}
		customer_invoices = get_customer_invoices(filters)

		for customer_invoice in customer_invoices:
			try:
				generate_electronic_invoice(customer_invoice, self.name)
			except Exception as ex:
				frappe.log_error(frappe.get_traceback(), title="EFE XML Export {0}, invoice {0}")


def get_customer_invoices(filters=None):
	out = []
	invoices = frappe.get_all("Sales Invoice", filters=filters, fields=["name", "customer", "company"])

	if len(invoices) == 0:
		frappe.throw(_("No invoices found. Please ensure you have submitted invoices in the selected period."))

	customers = list(set([invoice.customer for invoice in invoices]))
	for customer in customers:
		out_item = {
			"customer": frappe.get_doc("Customer", customer),
			"company": frappe.get_doc("Company", filters.get("company")),
			"invoices": [invoice for invoice in invoices if invoice.customer == customer]
		}
		out.append(out_item)
	return out

def generate_electronic_invoice(customer_invoice_set, efe_xml_export_name):
	namespace_map = {
		"p": "http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2",
		"ds": "http://www.w3.org/2000/09/xmldsig#",
		"xsi": "http://www.w3.org/2001/XMLSchema-instance"
	}

	schemaLocation="http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2 http://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.2/Schema_del_file_xml_FatturaPA_versione_1.2.xsd"
	
	ROOT_TAG = "{%s}FatturaElettronica" % namespace_map["p"]
	SCHEMA_LOCATION_KEY = "{%s}schemaLocation" % namespace_map["xsi"]

	root = ET.Element(ROOT_TAG, 
		attrib={SCHEMA_LOCATION_KEY : schemaLocation},
		nsmap=namespace_map,
		versione="FPR12"
	)

	invoice_header = ET.SubElement(root, 'FatturaElettronicaHeader')
	
	customer = customer_invoice_set.get("customer")
	company = customer_invoice_set.get("company")

	if not company.tax_id:
		frappe.throw(_("Please set Tax ID on Company"))
	
	dati_trasmissione = make_transmission_data(customer, company, efe_xml_export_name)
	invoice_header.append(dati_trasmissione)

	cedente_prestatore = make_company_info(company)
	invoice_header.append(cedente_prestatore)

	cessionario_committente = make_customer_info(customer)
	invoice_header.append(cessionario_committente)

	for invoice in customer_invoice_set.get("invoices"):
		invoice_body = make_invoice_body(invoice)
		root.append(invoice_body)
 
	etree_string = ET.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')

	file_name = make_fname(efe_xml_export_name, company)
	
	save_file(fname=file_name, content=etree_string, dt="EFE XML Export", dn=efe_xml_export_name)
		

def make_transmission_data(customer, company, efe_xml_export_name):
	dati_trasmissione = ET.Element('DatiTrasmissione')
	id_trasmittente = ET.SubElement(dati_trasmissione, 'IdTrasmittente')
	
	ET.SubElement(id_trasmittente, 'IdPaese').text = frappe.db.get_value("Country", frappe.defaults.get_defaults().get("country"), "code").upper()
	ET.SubElement(id_trasmittente, 'IdCodice').text = format_tax_id(company.tax_id)
	ET.SubElement(dati_trasmissione, 'ProgressivoInvio').text = efe_xml_export_name.split("-")[1]

	is_pa = frappe.db.get_value("Customer Group", customer.customer_group, "efe_is_pa")
	
	ET.SubElement(dati_trasmissione, 'FormatoTrasmissione').text = "FPA12" if is_pa else "FPR12"
	
	if customer.efe_codice_destinatario:
		ET.SubElement(dati_trasmissione, 'CodiceDestinatario').text = customer.efe_codice_destinatario #Set default as 7 zeros

	if company.phone_no or company.email:
		contatti_trasmittente = ET.SubElement(dati_trasmissione, 'ContattiTrasmittente')
		if company.phone_no:
			ET.SubElement(contatti_trasmittente, 'Telefono').text = company.phone_no
		if company.email:
			ET.SubElement(contatti_trasmittente, 'Email').text = company.email

	if customer.efe_pec_destinatario:	
		ET.SubElement(dati_trasmissione, 'PECDestinatario').text = customer.efe_pec_destinatario #Set mandatory if 7 zeros
	
	return dati_trasmissione

def make_company_info(company):
	cedente_prestatore = ET.Element('CedentePrestatore')
	dati_anagrafici = ET.SubElement(cedente_prestatore, 'DatiAnagrafici')

	id_fiscale_iva =  ET.SubElement(dati_anagrafici, 'IdFiscaleIVA')
	ET.SubElement(id_fiscale_iva, 'IdPaese').text = frappe.db.get_value("Country", frappe.defaults.get_defaults().get("country"), "code").upper()
	ET.SubElement(id_fiscale_iva, 'IdCodice').text = company.tax_id
	
	if company.efe_codice_fiscale:
		ET.SubElement(dati_anagrafici, 'CodiceFiscale').text = company.efe_codice_fiscale
	
	anagrafica = ET.SubElement(dati_anagrafici, 'Anagrafica')
	ET.SubElement(anagrafica, 'Denominazione').text = company.name
	ET.SubElement(dati_anagrafici, 'RegimeFiscale').text = company.efe_regime_fiscale


	#Set Address. Decide mandatory fields.
	address_name = get_default_address("Company", company.name)
	if not address_name:
		frappe.throw(_("Please set address for Company %s" % company.name))
	address = frappe.get_doc("Address", address_name)
	sede = ET.SubElement(cedente_prestatore, 'Sede')
	ET.SubElement(sede, 'Indirizzo').text = address.address_line1
	if address.efe_numero_civico:
		ET.SubElement(sede, 'NumeroCivico').text = address.efe_numero_civico
	ET.SubElement(sede, 'CAP').text = address.pincode
	ET.SubElement(sede, 'Comune').text = address.city
	ET.SubElement(sede, 'Provincia').text = address.state
	ET.SubElement(sede, 'Nazione').text = frappe.db.get_value("Country", frappe.defaults.get_defaults().get("country"), "code").upper()

	if company.phone_no or company.email or company.fax:
		contatti = ET.SubElement(cedente_prestatore, 'Contatti')
		if company.phone_no:
			ET.SubElement(contatti, 'Telefono').text = company.phone_no
		if company.fax:
			ET.SubElement(contatti, 'Fax').text = company.fax
		if company.email:
			ET.SubElement(contatti, 'Email').text = company.email
	
	return cedente_prestatore

def make_customer_info(customer):
	cessionario_committente = ET.Element('CessionarioCommittente')
	
	dati_anagrafici = ET.SubElement(cessionario_committente, 'DatiAnagrafici')

	id_fiscale_iva =  ET.SubElement(dati_anagrafici, 'IdFiscaleIVA')
	ET.SubElement(id_fiscale_iva, 'IdPaese').text = frappe.db.get_value("Country", frappe.defaults.get_defaults().get("country"), "code").upper()
	ET.SubElement(id_fiscale_iva, 'IdCodice').text = format_tax_id(customer.tax_id)

	if customer.efe_codice_fiscale:
		ET.SubElement(dati_anagrafici, 'CodiceFiscale').text = customer.efe_codice_fiscale
	
	anagrafica = ET.SubElement(dati_anagrafici, 'Anagrafica')
	ET.SubElement(anagrafica, 'Denominazione').text = customer.customer_name
	
	address_name = get_default_address("Customer", customer.name)
	if not address_name:
		frappe.throw(_("Please set address for customer %s" % customer.name))

	address = frappe.get_doc("Address", address_name)
	sede = ET.SubElement(cessionario_committente, 'Sede')
	ET.SubElement(sede, 'Indirizzo').text = address.address_line1
	if address.efe_numero_civico:
		ET.SubElement(sede, 'NumeroCivico').text = address.efe_numero_civico
	ET.SubElement(sede, 'CAP').text = address.pincode
	ET.SubElement(sede, 'Comune').text = address.city
	ET.SubElement(sede, 'Provincia').text = address.state
	ET.SubElement(sede, 'Nazione').text = frappe.db.get_value("Country", frappe.defaults.get_defaults().get("country"), "code").upper()
	
	return cessionario_committente

def make_invoice_body(invoice_data):
	invoice = frappe.get_doc("Sales Invoice", invoice_data.name)
	
	invoice_body = ET.Element('FatturaElettronicaBody')

	dati_generali = ET.SubElement(invoice_body, 'DatiGenerali')
	dati_generali_documento = ET.SubElement(dati_generali, 'DatiGeneraliDocumento')
	
	ET.SubElement(dati_generali_documento, 'TipoDocumento').text = frappe.db.get_value("Tipo Documento", 
		{"counterpart_doctype":"Sales Invoice"}, "code")

	ET.SubElement(dati_generali_documento, 'Divisa').text = "EUR"
	ET.SubElement(dati_generali_documento, 'Data').text = str(invoice.posting_date)
	ET.SubElement(dati_generali_documento, 'Numero').text = get_number_from_name(invoice.name)
	
	if len(invoice.taxes):
		bollo = next((tax for tax in invoice.taxes if "bollo" in tax.account_head.lower()), None)
		ritenuta =next ((tax for tax in invoice.taxes if "iva" in tax.account_head.lower()), None)

		if bollo:
			dati_bollo = ET.SubElement(dati_generali_documento, 'DatiBollo')
			ET.SubElement(dati_bollo, 'ImportoBollo').text = format_float(bollo.tax_amount)
		if ritenuta:
			dati_ritenuta = ET.SubElement(dati_generali_documento, 'DatiRitenuta')
			ET.SubElement(dati_ritenuta, 'TipoRitenuta').text = ritenuta.account_head
			ET.SubElement(dati_ritenuta, 'ImportoRitenuta').text = ritenuta.account_head
			ET.SubElement(dati_ritenuta, 'AliquotaRitenuta').text = ritenuta.account_head
			ET.SubElement(dati_ritenuta, 'CausalePagamento').text = "IVA" #Confirm
	
	ET.SubElement(dati_generali_documento, 'ImportoTotaleDocumento').text = format_float(invoice.grand_total)
	ET.SubElement(dati_generali_documento, 'Causale').text = "VENDITA" #CAUSALE as select field
	
	delivery_notes = frappe.get_all("Delivery Note", 
		filters=[["Delivery Note Item", "against_sales_invoice", "=", invoice.name]], 
		fields=["name", "posting_date", "efe_transporter_tax_id", "efe_transporter_codice_fiscale"])
	
	if len(delivery_notes):
		dati_trasporto = ET.SubElement(dati_generali, 'DatiTrasporto')
		datiDDT = ET.SubElement(dati_generali, 'DatiDDT')
		for delivery_note in delivery_notes:
			ET.SubElement(datiDDT, 'NumeroDDT').text = delivery_note.name
			ET.SubElement(datiDDT, 'DataDDT').text = str(delivery_note.posting_date)
			
			dati_anagrafici_vettore = ET.SubElement(dati_trasporto, 'DatiAnagraficiVettore')
			id_fiscale_iva = ET.SubElement(dati_anagrafici_vettore, 'IdFiscaleIVA')
			ET.SubElement(id_fiscale_iva, 'IdPaese').text = frappe.db.get_value("Country", frappe.defaults.get_defaults().get("country"), "code").upper()
			ET.SubElement(id_fiscale_iva, 'IdCodice').text = delivery_note.efe_transporter_tax_id
			ET.SubElement(dati_anagrafici_vettore, 'CodiceFiscale').text = delivery_note.efe_transporter_codice_fiscale
			
			anagrafica = ET.SubElement(dati_anagrafici_vettore, 'Anagrafica')
			ET.SubElement(anagrafica, 'Denominazione').text = delivery_note.transporter_name
	
	dati_beni_servizi = ET.SubElement(invoice_body, 'DatiBeniServizi')

	itemised_tax = get_itemised_tax(invoice.taxes)

	riepilogo = frappe._dict()

	for item in invoice.items:
		dettaglio_linee = ET.SubElement(dati_beni_servizi, 'DettaglioLinee')
		ET.SubElement(dettaglio_linee, 'NumeroLinea').text = str(item.idx)
		codice_articolo = ET.SubElement(dettaglio_linee, 'CodiceArticolo')
		ET.SubElement(codice_articolo, 'CodiceTipo').text = "CODICE"
		ET.SubElement(codice_articolo, 'CodiceValore').text = item.item_code
		ET.SubElement(dettaglio_linee, 'Descrizione').text = item.item_name
		ET.SubElement(dettaglio_linee, 'Quantita').text = format_float(item.qty) 
		ET.SubElement(dettaglio_linee, 'PrezzoUnitario').text = format_float(item.rate)
		ET.SubElement(dettaglio_linee, 'PrezzoTotale').text = format_float(item.amount)

		tax_rate = sum([tax.get('tax_rate', 0) for d, tax in itemised_tax.get(item.item_code).items()])
		tax_amount = sum([tax.get('tax_amount', 0) for d, tax in itemised_tax.get(item.item_code).items()])
		riepilogo.setdefault(tax_rate, {"tax_amount": 0.0, "taxable_amount":0.0, "natura": ""})
		riepilogo[tax_rate]["taxable_amount"] += item.net_amount
		riepilogo[tax_rate]["tax_amount"] += tax_amount
		ET.SubElement(dettaglio_linee, 'AliquotaIVA').text = format_float(tax_rate)
		if tax_rate == 0.0:
			natura =  frappe.db.get_value("Item Tax", {"parent":item.item_code}, "efe_natura")
			ET.SubElement(dettaglio_linee, 'Natura').text = natura
			riepilogo[tax_rate]["natura"] = natura

	for key, value in riepilogo.items():
		dati_riepilogo = ET.SubElement(dati_beni_servizi, 'DatiRiepilogo')
		ET.SubElement(dati_riepilogo, 'AliquotaIVA').text = format_float(key)
		if value.get("natura"):
			ET.SubElement(dati_riepilogo, 'Natura').text = value.get("natura")
		#Can two items with zero tax have different Natura each?
		ET.SubElement(dati_riepilogo, 'ImponibileImporto').text = format_float(value.get("taxable_amount"))
		ET.SubElement(dati_riepilogo, 'Imposta').text = format_float(value.get("tax_amount"))
		ET.SubElement(dati_riepilogo, 'EsigibilitaIVA').text = invoice.get("efe_esigibilita_iva")

	### DatiPagamento
	payment_entry_names = frappe.get_all("Payment Entry", 
		filters=[
			["Payment Entry Reference", "reference_doctype", "=", "Sales Invoice"], 
			["Payment Entry Reference", "reference_name", "=", invoice.name]
		]
	)
	
	for payment_entry_name in payment_entry_names:
		payment_entry = frappe.get_doc("Payment Entry Name", payment_entry_name)
		dati_pagamento = ET.SubElement(invoice_body, 'DatiPagamento')
		ET.SubElement(invoice_body, 'CondizionePagamento').text = "TP01" if len(invoice.payment_schedule) > 1 else "TP02"
		
		dettaglio_pagamento = ET.SubElement(dati_pagamento, 'DatiPagamento')
		ET.SubElement(dettaglio_pagamento, 'ModalitaPagamento').text = frappe.db.get_value("Mode of Payment", payment_entry.mode_of_payment, "efe_code")
		ET.SubElement(dettaglio_pagamento, 'DataScadenzaPagamento').text = payment_entry.posting_date

		#Get amount allocated for the specific invoice
		paid_amount_for_invoice = next(
			(ref.allocated_amount for ref in payment_entry.references 
			if ref.reference_doctype == "Sales Invoice" and ref.reference_name == invoice.name)
		)
		ET.SubElement(dettaglio_pagamento, 'ImportoPagamento').text = format_float(paid_amount_for_invoice)

	return invoice_body

def make_fname(efe_xml_export_name, company):
	country_code = frappe.db.get_value("Country", frappe.defaults.get_defaults().get("country"), "code").upper()
	return "{0}{1}_{2}.xml".format(country_code, company.tax_id, make_autoname())

def get_number_from_name(doc_name):
	return str(int(doc_name.split("-")[-1]))

def format_float(float_number):
	return "%.2f" % float_number

def format_tax_id(tax_id):
	#Remove "IT" prefix and any spaces from tax id
	return tax_id.replace("IT", "").replace(" ", "")
