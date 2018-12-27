frappe.ui.form.on("Sales Invoice", {
    refresh: function(frm) {
        add_export_button(frm);
        set_esigibilita_iva(frm);
    },
    customer: function(frm) {
        set_esigibilita_iva(frm);
    }
});

async function set_esigibilita_iva(frm) {
    if (frm.doc.docstatus == 1 || frm.doc.docstatus == 2) return 
    
    if(!frm.doc.company || !frm.doc.customer_group) return

    var e_iva_response = await frappe.db.get_value("Company", 
        frm.doc.company, 
        "efe_esigibilita_iva");
    
    var is_pa_response = await frappe.db.get_value("Customer Group", 
        frm.doc.customer_group,
        "efe_is_pa");

    if (e_iva_response && e_iva_response.message.efe_esigibilita_iva) {
        frm.set_value("efe_esigibilita_iva", esigibilita_iva.message.efe_esigibilita_iva);
    } else if (is_pa_response && is_pa_response.message.efe_is_pa) {
        frm.set_value("efe_esigibilita_iva", "S");
    } else {
        frm.set_value("efe_esigibilita_iva", "I");
    }
}

function add_export_button(frm) {
    if (frm.doc.docstatus == 1) {
        frm.add_custom_button("Export XML", function() {
            var w = window.open(
                frappe.urllib.get_full_url(
                    "/api/method/erpnext_fattura_elettronica.erpnext_fattura_elettronica.doctype.efe_xml_export.efe_xml_export.generate_single_invoice?"
                    + "invoice_name=" + encodeURIComponent(frm.doc.name)
                )
            );
            if (!w) {
                frappe.msgprint(__("Please enable pop-ups")); return;
            }
        });
    }
}
