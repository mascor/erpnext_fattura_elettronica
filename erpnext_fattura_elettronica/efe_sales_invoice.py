import frappe

def validate(doc, method):
    if not hasattr(doc, 'mode_of_payment'):
        if doc.payment_terms_template:
            template = frappe.get_doc("Payment Terms Template", doc.payment_terms_template)
            for term in template.terms:
                for row in doc.payment_schedule:
                    if term.payment_term == row.payment_term:
                        row.efe_mode_of_payment = term.efe_mode_of_payment
                        row.efe_bank_account = term.efe_bank_account
    else:
        if doc.mode_of_payment:
            for row in doc.payment_schedule:
                row.efe_mode_of_payment = doc.mode_of_payment
