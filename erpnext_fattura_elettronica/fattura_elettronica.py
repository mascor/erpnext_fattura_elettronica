import frappe, json, xml
from frappe import _

@frappe.whitelist()
def generate_xml(names):
    names = json.loads(names)
    for name in names:
        print(name)
