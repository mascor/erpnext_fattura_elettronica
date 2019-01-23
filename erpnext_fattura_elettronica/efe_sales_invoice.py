import frappe

def validate(doc, method):
    if not doc.payment_terms_template:
        return
    
    template = frappe.get_doc("Payment Terms Template", doc.payment_terms_template)
    for term in template.terms:
        for row in doc.payment_schedule:
            if term.payment_term == row.payment_term:
                row.efe_mode_of_payment = term.efe_mode_of_payment
                row.efe_bank_account = term.efe_bank_account
