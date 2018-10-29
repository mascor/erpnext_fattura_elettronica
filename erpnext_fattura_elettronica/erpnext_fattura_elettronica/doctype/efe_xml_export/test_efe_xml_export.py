# -*- coding: utf-8 -*-
# Copyright (c) 2018, Massimiliano Corvino and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest
from frappe import _


def create_data():
	
	#Add a company address.
	company_name = frappe.defaults.get_defaults()["company"]
	company_abbr = frappe.db.get_value("Company", company_name, "abbr")
	iva_tax_head = frappe.get_doc("Account", "IVA - ")
	
	frappe.get_doc({
		"doctype": "Address",
		"title": "Indoril Nerevar-Billing",
		"address_line1": "via Roma",
		"city": "Foggia",
		"state": "Puglia",
		"fax": "123123456",
		"links": [
			{
				"link_doctype": "Company",
				"link_name": company_name
			}
		] 
	}).insert()

	#Create a customer with an address and contact.
	frappe.get_doc({
		"doctype": "Customer",
		"customer_name": "Indoril Nerevar",
		"customer_group": _("Individual"),
		"territory": _("All Territories"),
		"efe_codice_fiscale": "ABC123XCV123W",
	}).insert()

	frappe.get_doc({
		"doctype": "Address",
		"title": "Indoril Nerevar-Billing",
		"address_line1": "via Roma",
		"city": "Foggia",
		"state": "Puglia",
		"fax": "123123456",
		"links": [
			{
				"link_doctype": "Customer",
				"link_name":"Indoril Nerevar"
			}
		] 
	}).insert()
	
	frappe.get_doc({
		"doctype": "Contact",
		"first_name": "Indoril",
		"last_name": "Nerevar",
		"email_id": "nerevar@vvardenfell.mw",
		"phone": "24445555",
		"state": "Puglia",
		"links": [
			{
				"link_doctype": "Customer",
				"link_name":"Indoril Nerevar"
			}
		] 
	}).insert()

	#Create three Items with different IVA Rates
	#Create invoices
	# 	1. First Customer, I1, I2
	# 	2. Second Customer, I1, I3
	# 	3. Second Customer, I1, I2, I3
	
	#Create Payment Entry for First Invoice
	frappe.get_doc({
		"doctype": "Item",
		"item_code": "i1",
		"item_name": "Item One",
		"item_group": "Products",
		"is_sales_item": "1",
		"standard_selling_rate": 100,
		"taxes": [
			{
				"account_head": "IVA",
				"link_name":"Indoril Nerevar"
			}
		] 
	}).insert()

def remove_data():
	frappe.delete_doc("Customer", "Mario Rossi")
	
class TestEFEXMLExport(unittest.TestCase):
	def setUp(self):
		create_data()

	def tearDown(self):
		#remove_data()
		pass

	def test_customer_created(self):
		customer = frappe.get_doc("Customer", "Mario Rossi")
		self.assertTrue(customer is not None)
