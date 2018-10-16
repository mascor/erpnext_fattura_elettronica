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
    invoices = frappe.get_all("Sales Invoice", filters=filters, fields=["*"])
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
	
	ET.register_namespace("ns3","FatturaElettronica")

	fattura_elettronica = ET.Element('FatturaElettronica')
	fattura_elettronica.set("xmlns:ds","http://www.w3.org/2000/09/xmldsig#")

	fattura_header = ET.SubElement(fattura_elettronica, 'FatturaElettronicaHeader')
	
	append_dati_trasmissione(fattura_header, customer, company, efe_xml_export_name)

	for invoice in customer_invoice_set.get("invoices"):
		#TODO: Append FatturaBody
		pass

	rough_string = tostring(fattura_elettronica, 'utf-8')
	reparsed = minidom.parseString(rough_string)
	print(reparsed.toprettyxml(indent="  "))


def append_dati_trasmissione(header, customer, company, efe_xml_export_name):
	dati_trasmissione = ET.SubElement(header, 'DatiTransmissione')
	id_trasmittente = ET.SubElement(dati_trasmissione, 'IdTransmittente')
	
	id_paese = ET.SubElement(id_trasmittente, 'IdPaese')
	id_paese.text = "IT"
	id_codice = ET.SubElement(id_trasmittente, 'IdCodice')
	id_codice.text = company.tax_id
	progressivo_invio = ET.SubElement(dati_trasmissione, 'ProgressivoInvio')
	progressivo_invio.text = efe_xml_export_name

	is_pa = frappe.db.get_value("Customer Group", customer.customer_group, "efe_is_pa")
	
	formato_trasmissione = ET.SubElement(dati_trasmissione, 'FormatoTrasmissione')
	formato_trasmissione.text = "FPA12" if is_pa else "FPR12"

	if customer.efe_codice_destinatario:
		codice_destinatario = ET.SubElement(dati_trasmissione, 'CodiceDestinatario')
		codice_destinatario.text = customer.efe_codice_destinatario

	if company.phone_no or company.email:
		contatti_trasmittente = ET.SubElement(dati_trasmissione, 'ContattiTrasmittente')
		if company.phone_no:
			contatti_trasmittente_telefono = ET.SubElement(contatti_trasmittente, 'Telefono')
			contatti_trasmittente_telefono.text = company.phone_no
		if company.email:
			contatti_trasmittente_email = ET.SubElement(contatti_trasmittente, 'Email')
			contatti_trasmittente_email.text = company.email

	if customer.efe_pec_destinatario:	
		pec_destinatario = ET.SubElement(dati_trasmissione, 'PecDestinatario')
		pec_destinatario.text = customer.efe_pec_destinatario


def append_cedente_prestatore(header, customer, company, efe_xml_export_name):
	pass

def append_rappresentante_fiscale(header, customer, company):
	pass

def append_cessionario_committente(header, customer, company):
	pass
