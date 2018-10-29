// Copyright (c) 2018, Massimiliano Corvino and contributors
// For license information, please see license.txt

frappe.ui.form.on('EFE XML Export', {
	refresh: function(frm) {
		if (!frm.doc.__islocal) {
			frm.add_custom_button(__("Export"),() => {
				frappe.call({
					method: "generate_electronic_invoices",
					doc:frm.doc,
					callback: (r)=>{
						frm.reload_doc();
					}
				})
			});
		}
	}
});
