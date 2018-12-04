// Copyright (c) 2018, Massimiliano Corvino and contributors
// For license information, please see license.txt

frappe.ui.form.on('EFE XML Export', {
	refresh: function(frm) {
		if (!frm.doc.__islocal) {
			frm.add_custom_button(__("Export"),() => {
				console.log(frm.doc.from_date, frm.doc.to_date, frm.doc.company, frm.doc.name)
				var w = window.open(
					frappe.urllib.get_full_url("/api/method/erpnext_fattura_elettronica.erpnext_fattura_elettronica.doctype.efe_xml_export.efe_xml_export.generate_electronic_invoices?"
					+ "from_date=" + encodeURIComponent(frm.doc.from_date)
					+ "&to_date=" + encodeURIComponent(frm.doc.to_date)
					+ "&company=" + encodeURIComponent(frm.doc.company)
					+ "&export_doc_name=" + encodeURIComponent(frm.doc.name)
					)
				);
				if (!w) {
					frappe.msgprint(__("Please enable pop-ups")); return;
				}
			});
		}
	}
});
