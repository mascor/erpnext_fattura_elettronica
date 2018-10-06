import frappe, json
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from frappe.desk.reportview import get_match_cond, get_filters_cond
from frappe import _

@frappe.whitelist()
def generate_xml(names, filters):
    conditions = []
    query = """SELECT 
        `tabSales Invoice`.name, `tabSales Invoice`.customer, 
        `tabSales Invoice Item`.item_code
        FROM 
            `tabSales Invoice` INNER JOIN
            `tabSales Invoice Item` ON `tabSales Invoice`.name = `tabSales Invoice Item`.parent
        WHERE 
            `tabSales Invoice`.docstatus = 1 {fcond}
        ORDER BY `tabSales Invoice`.name;""".format(**{
            'fcond': get_filters_cond("Sales Invoice", 
                {
                    "posting_date": ("between", [
                    filters.get("from_date"), filters.get("to_date")
                ])},
                conditions)
        })
    
    print(query)

    invoices = frappe.db.sql(query, as_dict=1)
    print(invoices)
    return invoices
