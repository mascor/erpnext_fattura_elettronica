frappe.ui.form.on("Sales Invoice", {
    refresh: function(frm) {
       set_esigibilita_iva(frm);
    },
    customer: function(frm) {
        set_esigibilita_iva(frm);
    }
});

async function set_esigibilita_iva(frm) {
    if (frm.doc.docstatus == 1 || frm.doc.docstatus == 2) return 
    var e_iva_response = await frappe.db.get_value("Company", 
        frappe.defaults.get_default("company"), 
        "efe_esigibilita_iva", 
        function(r){}   
    )
    var is_pa_response = await frappe.db.get_value("Customer Group", 
        frm.doc.customer_group,
        "efe_is_pa",
        function(r){}
    )
    if (e_iva_response && e_iva_response.message.efe_esigibilita_iva) {
        frm.set_value("efe_esigibilita_iva", esigibilita_iva.message.efe_esigibilita_iva);
    } else if (is_pa_response && is_pa_response.message.efe_is_pa) {
        frm.set_value("efe_esigibilita_iva", "S");
    } else {
        frm.set_value("efe_esigibilita_iva", "I");
    }
}
