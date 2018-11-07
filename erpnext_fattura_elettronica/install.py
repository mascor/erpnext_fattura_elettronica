#coding:utf-8
from __future__ import print_function, unicode_literals

import frappe
from frappe import _


def after_install():
    insert_natura() 
    insert_tipo_documento()
    insert_regime_fiscale()

def insert_natura():
    frappe.get_doc({"doctype": "Natura", "code": "N1", "description": "Escluse ex art. 15"}).insert()
    frappe.get_doc({"doctype": "Natura", "code": "N2", "description": "Non soggette"}).insert()
    frappe.get_doc({"doctype": "Natura", "code": "N3", "description": "Non imponibili"}).insert()
    frappe.get_doc({"doctype": "Natura", "code": "N4", "description": "Esenti"}).insert()
    frappe.get_doc({"doctype": "Natura", "code": "N5", "description": "Regime del margine / IVA non esposta in fattura"}).insert()
    frappe.get_doc({
        "doctype": "Natura", "code": "N6", 
        "description": "Regime del margine / IVA non esposta in fattura",
        "riferimento_normativo": "Per le operazioni in reverse charge ovvero nei casi di autofatturazione per acquisti extra UE di servizi ovvero per importazioni di beni nei soli casi previsti"
    }).insert()
    frappe.get_doc({
        "doctype": "Natura", "code": "N7", 
        "description": "IVA assolta in altro stato UE",
        "riferimento_normativo": "Vendite a distanza ex art. 40 c. 3 e 4 e art. 41 c. 1 lett. b,  DL 331/93; prestazione di servizi di telecomunicazioni, tele-radiodiffusione ed elettronici ex art. 7-sexies lett. f, g, art. 74-sexies DPR 633/72"
    }).insert()

def insert_tipo_documento():
    #Insert only Fattura
    frappe.get_doc({"doctype": "Tipo Documento", "code": "TD01", "description": "fattura", "counterpart_doctype":"Sales Invoice"}).insert()

def insert_regime_fiscale():
    frappe.get_doc({"doctype": "Regime Fiscale", "code": "RF02", "description": "Contribuenti minimi (art.1, c.96-117, L. 244/07)"}).insert()
    frappe.get_doc({"doctype": "Regime Fiscale", "code": "RF04", "description": "Agricoltura e attività connesse e pesca (artt.34 e 34-bis, DPR 633/72)"}).insert()
    frappe.get_doc({"doctype": "Regime Fiscale", "code": "RF05", "description": "Vendita sali e tabacchi (art.74, c.1, DPR. 633/72)"}).insert()
    frappe.get_doc({"doctype": "Regime Fiscale", "code": "RF06", "description": "Commercio fiammiferi (art.74, c.1, DPR 633/72)"}).insert()
    frappe.get_doc({"doctype": "Regime Fiscale", "code": "RF07", "description": "Editoria (art.74, c.1, DPR 633/72)"}).insert()
    frappe.get_doc({"doctype": "Regime Fiscale", "code": "RF08", "description": "Gestione servizi telefonia pubblica (art.74, c.1, DPR 633/72)"}).insert()
    frappe.get_doc({"doctype": "Regime Fiscale", "code": "RF09", "description": "Rivendita documenti di trasporto pubblico e di sosta (art.74, c.1, DPR 633/72)"}).insert()
    frappe.get_doc({"doctype": "Regime Fiscale", "code": "RF10", "description": "Intrattenimenti, giochi e altre attività di cui alla tariffa allegata al DPR 640/72 (art.74, c.6, DPR 633/72)"}).insert()
    frappe.get_doc({"doctype": "Regime Fiscale", "code": "RF11", "description": "Agenzie viaggi e turismo (art.74-ter, DPR 633/72)"}).insert()
    frappe.get_doc({"doctype": "Regime Fiscale", "code": "RF12", "description": "Agriturismo (art.5, c.2, L. 413/91)"}).insert()
    frappe.get_doc({"doctype": "Regime Fiscale", "code": "RF13", "description": "Vendite a domicilio (art.25-bis, c.6, DPR 600/73)"}).insert()
    frappe.get_doc({"doctype": "Regime Fiscale", "code": "RF14", "description": "Rivendita beni usati, oggetti d’arte, d’antiquariato o da collezione (art.36, DL 41/95)"}).insert()
    frappe.get_doc({"doctype": "Regime Fiscale", "code": "RF15", "description": "Agenzie di vendite all’asta di oggetti d’arte, antiquariato o da collezione (art.40-bis, DL 41/95)"}).insert()
