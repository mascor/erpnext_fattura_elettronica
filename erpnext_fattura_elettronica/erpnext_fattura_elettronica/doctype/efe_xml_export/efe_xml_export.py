# -*- coding: utf-8 -*-
# Copyright (c) 2018, Massimiliano Corvino and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from xml.etree import ElementTree as ET
#from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

class EFEXMLExport(Document):
	def generate_xml_documents(self):
		filters = {
			"posting_date": ("between", [self.from_date, self.to_date]),
			"company": self.company,
		}
		customer_invoices = get_customer_invoices(filters)

		for customer_invoice in customer_invoices:
			generate_invoice_xml(customer_invoice, self.name) 		


def get_customer_invoices(filters=None):
    out = []
    invoices = frappe.get_all("Sales Invoice", filters=filters, fields=["name", "customer", "company"])
    customers = list(set([invoice.customer for invoice in invoices]))
    for customer in customers:
        out_item = {
            "customer": frappe.get_doc("Customer", customer),
			"company": frappe.get_doc("Company", filters.get("company")),
            "invoices": [invoice for invoice in invoices if invoice.customer == customer]
        }
        out.append(out_item)
    return out

def generate_invoice_xml(customer_invoice_set, efe_xml_export_name):
	customer = customer_invoice_set.get("customer")
	company = customer_invoice_set.get("company")
	
	fattura_elettronica = ET.Element('FatturaElettronica')
	fattura_elettronica.set("xmlns:ds","http://www.w3.org/2000/09/xmldsig#")

	fattura_header = ET.SubElement(fattura_elettronica, 'FatturaElettronicaHeader')
	
	append_dati_trasmissione(fattura_header, customer, company, efe_xml_export_name)
	append_cedente_prestatore(fattura_header, customer, company, efe_xml_export_name)

	for invoice in customer_invoice_set.get("invoices"):
		#TODO: Append FatturaBody
		append_fattura_body(fattura_elettronica, invoice)
 

	rough_string = ET.tostring(fattura_elettronica, 'utf-8')
	reparsed = minidom.parseString(rough_string)
	print(reparsed.toprettyxml(indent="  "))


def append_dati_trasmissione(header, customer, company, efe_xml_export_name):
	dati_trasmissione = ET.SubElement(header, 'DatiTransmissione')
	id_trasmittente = ET.SubElement(dati_trasmissione, 'IdTransmittente')
	
	ET.SubElement(id_trasmittente, 'IdPaese').text = "IT"
	ET.SubElement(id_trasmittente, 'IdCodice').text = company.tax_id
	ET.SubElement(dati_trasmissione, 'ProgressivoInvio').text = efe_xml_export_name

	is_pa = frappe.db.get_value("Customer Group", customer.customer_group, "efe_is_pa")
	
	ET.SubElement(dati_trasmissione, 'FormatoTrasmissione').text = "FPA12" if is_pa else "FPR12"
	
	if customer.efe_codice_destinatario:
		ET.SubElement(dati_trasmissione, 'CodiceDestinatario').text = customer.efe_codice_destinatario

	if company.phone_no or company.email:
		contatti_trasmittente = ET.SubElement(dati_trasmissione, 'ContattiTrasmittente')
		if company.phone_no:
			ET.SubElement(contatti_trasmittente, 'Telefono').text = company.phone_no
		if company.email:
			ET.SubElement(contatti_trasmittente, 'Email').text = company.email

	if customer.efe_pec_destinatario:	
		ET.SubElement(dati_trasmissione, 'PecDestinatario').text = customer.efe_pec_destinatario


def append_cedente_prestatore(header, customer, company, efe_xml_export_name):
	cedente_prestatore = ET.SubElement(header, 'CedentePrestatore')
	data_anagrafici = ET.SubElement(cedente_prestatore, 'DataAnagrafici')

	id_fiscale_iva =  ET.SubElement(data_anagrafici, 'IdFiscaleIva')
	ET.SubElement(id_fiscale_iva, 'IdPaese').text = "IT"
	ET.SubElement(id_fiscale_iva, 'IdCodice').text = company.tax_id
	
	if company.efe_codicefiscale:
		ET.SubElement(data_anagrafici, 'CodiceFiscale').text = company.efe_codicefiscale
	
	anagrafica = ET.SubElement(data_anagrafici, 'Anagrafica')
	ET.SubElement(anagrafica, 'Denominazione').text = company.name
	#regime_fiscale = ET.SubElement(anagrafica, 'RegimeFiscale')

	#sede = ET.SubElement(cedente_prestatore, 'Sede')
	if company.phone_no or company.email or company.fax:
		contatti = ET.SubElement(cedente_prestatore, 'Contatti')
		if company.phone_no:
			ET.SubElement(contatti, 'Telefono').text = company.phone_no
		if company.email:
			ET.SubElement(contatti, 'Email').text = company.email
		if company.fax:
			ET.SubElement(contatti, 'Fax').text = company.fax

def append_cessionario_committente(header, customer, company):
	cessionario_committente = ET.SubElement(header, 'CessionarioCommittente')
	
	data_anagrafici = ET.SubElement(cessionario_committente, 'DataAnagrafici')

	id_fiscale_iva =  ET.SubElement(data_anagrafici, 'IdFiscaleIva')
	ET.SubElement(id_fiscale_iva, 'IdPaese').text = "IT"
	ET.SubElement(id_fiscale_iva, 'IdCodice').text = customer.tax_id

	if customer.efe_codicefiscale:
		ET.SubElement(data_anagrafici, 'CodiceFiscale').text = customer.efe_codice_fiscale
	
	anagrafica = ET.SubElement(data_anagrafici, 'Anagrafica')
	ET.SubElement(anagrafica, 'Denominazione').text = customer.customer_name
	
	#sede = ET.SubElement(cedente_prestatore, 'Sede')
	if customer.phone_no or customer.email or customer.fax:
		contatti = ET.SubElement(cessionario_committente, 'Contatti')
		if customer.phone_no:
			ET.SubElement(contatti, 'Telefono').text = customer.phone_no
		if customer.email:
			ET.SubElement(contatti, 'Email').text = customer.email
		if customer.fax:
			ET.SubElement(contatti, 'Fax').text = customer.fax

def append_fattura_body(fattura_elettronica, invoice_data):
	invoice = frappe.get_doc("Sales Invoice", invoice_data.name)
	
	fattura_elettronica_body = ET.SubElement(fattura_elettronica, 'FatturaElettronicaBody')

	dati_generali = ET.SubElement(fattura_elettronica_body, 'DatiGenerali')
	dati_generali_documento = ET.SubElement(dati_generali, 'DatiGeneraliDocumento')
	ET.SubElement(dati_generali_documento, 'TipoDocumento').text = frappe.db.get_value("Tipo Documento", {"counterpart_doctype":"Sales Invoice"}, "code")
	ET.SubElement(dati_generali_documento, 'Divisa').text = "EUR"
	ET.SubElement(dati_generali_documento, 'Data').text = str(invoice.posting_date)
	ET.SubElement(dati_generali_documento, 'Numero').text = invoice.name
	
	if len(invoice.taxes):
		bollo = next((tax for tax in invoice.taxes if "bollo" in tax.account_head.lower()), None)
		ritenuta =next ((tax for tax in invoice.taxes if "iva" in tax.account_head.lower()), None)

		if bollo:
			dati_bollo = ET.SubElement(dati_generali_documento, 'DatiBollo')
			ET.SubElement(dati_bollo, 'BolloVirtuale').text = "SI"
			ET.SubElement(dati_bollo, 'ImportoBollo').text = str(bollo.tax_amount)
		if ritenuta:
			dati_ritenuta = ET.SubElement(dati_generali_documento, 'DatiRitenuta')
			ET.SubElement(dati_ritenuta, 'TipoRitenuta').text = ritenuta.account_head
			ET.SubElement(dati_ritenuta, 'ImportoRitenuta').text = ritenuta.account_head
			ET.SubElement(dati_ritenuta, 'AliquotaRitenuta').text = ritenuta.account_head
			ET.SubElement(dati_ritenuta, 'CausalePagamento').text = "IVA" #Confirm
	
	ET.SubElement(dati_generali_documento, 'ImportoTotaleDocumento').text = str(invoice.grand_total)
	ET.SubElement(dati_generali_documento, 'Arrotondamento').text = str(invoice.rounded_total) #Confirm
	ET.SubElement(dati_generali_documento, 'Causale').text = "VENDITA"
	
	delivery_notes = frappe.get_all("Delivery Note", 
		filters=[["Delivery Note Item", "against_sales_invoice", "=", invoice.name]], 
		fields=["name", "posting_date", "efe_transporter"])
	
	if len(delivery_notes):
		dati_trasporto = ET.SubElement(dati_generali, 'DatiTrasporto')
		datiDDT = ET.SubElement(dati_generali, 'DatiDDT')
		for delivery_note in delivery_notes:
			transporter = frappe.get_doc("Transporter", delivery_note.efe_transporter)
			ET.SubElement(datiDDT, 'NumeroDDT').text = delivery_note.name
			ET.SubElement(datiDDT, 'DataDDT').text = str(delivery_note.posting_date)
			
			dati_anagrafici_vettore = ET.SubElement(dati_trasporto, 'DatiAnagraficiVettore')
			id_fiscale_iva = ET.SubElement(dati_anagrafici_vettore, 'IdFiscaleIVA')
			ET.SubElement(id_fiscale_iva, 'IdPaese').text = "IT"
			ET.SubElement(id_fiscale_iva, 'IdCodice').text = "???" #Confirm
			ET.SubElement(dati_anagrafici_vettore, 'CodiceFiscale').text = transporter.tax_id
			anagrafica = ET.SubElement(dati_anagrafici_vettore, 'Anagrafica')
			ET.SubElement(anagrafica, 'Denominazione').text = transporter.name

	
	dati_beni_servizi = ET.SubElement(fattura_elettronica_body, 'DatiBeniServizi')
	dettaglio_linee = ET.SubElement(dati_beni_servizi, 'DattaglioLinee')
	
	for item in invoice.items:
		ET.SubElement(dettaglio_linee, 'NumeroLinea').text = str(item.idx)
		ET.SubElement(dettaglio_linee, 'CodiceArticolo').text = item.item_code
		ET.SubElement(dettaglio_linee, 'Descrizione').text = item.item_name
		ET.SubElement(dettaglio_linee, 'Quantita').text = str(item.qty)
		ET.SubElement(dettaglio_linee, 'UnitaMisura').text = item.stock_uom
		ET.SubElement(dettaglio_linee, 'PrezzoUnitario').text = str(item.rate)
		ET.SubElement(dettaglio_linee, 'PrezzoTotale').text = str(item.amount)
		ET.SubElement(dettaglio_linee, 'AliquotaIVA').text = str(item.item_tax_rate)
		ET.SubElement(dettaglio_linee, 'Natura').text = "???"

