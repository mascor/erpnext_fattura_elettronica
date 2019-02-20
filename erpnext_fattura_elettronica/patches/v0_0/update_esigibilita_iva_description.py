# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    # Update options for efe_esigibilita_iva
    esigibilita_iva_field = dict(fieldname='efe_esigibilita_iva',
        options="\nS-Scissione dei Pagamenti\nD-Differita\nI-Immediata",
        default="I-Immediata")

    custom_fields = {
        'Company': [esigibilita_iva_field],
        'Sales Invoice': [esigibilita_iva_field]
    }

    create_custom_fields(custom_fields)

    # Update EsigibilitaIVA from SDI
    frappe.db.sql("""
        UPDATE `tabSales Invoice`
        SET efe_esigibilita_iva = (
            case efe_esigibilita_iva
                when 'S' then 'S-Scissione dei Pagamenti'
                when 'D' then 'D-Differita'
                when 'I' then 'I-Immediata'
                else efe_esigibilita_iva
            end
        );"""
    )

    frappe.db.sql("""
        UPDATE `tabCompany`
        SET efe_esigibilita_iva = (
            case efe_esigibilita_iva
                when 'S' then 'S-Scissione dei Pagamenti'
                when 'D' then 'D-Differita'
                when 'I' then 'I-Immediata'
                else efe_esigibilita_iva
            end
        );
        """
    )