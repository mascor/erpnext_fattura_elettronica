import frappe
from frappe import _

@frappe.whitelist()
def generate_codice_fiscale(first_name, last_name, date_of_birth, gender, place_of_birth):
	from codicefiscale import build

	gender = 'M' if gender == 'Male' else 'F'
	municipality = frappe.db.get_value("Territory", place_of_birth, "efe_cadastral_code")
	date_of_birth = frappe.utils.get_datetime(date_of_birth)

	return build(last_name, first_name, date_of_birth, gender, municipality)

@frappe.whitelist()
def validate_codice_fiscale(codice_fiscale):
	from codicefiscale import isvalid

	valid = isvalid(codice_fiscale)
	
	return _("Codice Fiscale is valid") if valid else _("Codice Fiscale is invalid")