// Copyright (c) 2018, Massimiliano Corvino and contributors
// For license information, please see license.txt

frappe.ui.form.on('EFE XML Export', {
	refresh: function(frm) {
		if (!frm.doc.__islocal) {
			frm.add_custom_button(__("Export"),() => {
				frappe.call({
					method: "generate_xml_documents",
					doc:frm.doc,
					callback: (r)=>{
						console.log("generate_xml_document", r);
					}
				})
			});
		}
	}
});
