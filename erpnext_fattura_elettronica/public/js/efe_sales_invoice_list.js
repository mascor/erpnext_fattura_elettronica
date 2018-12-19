frappe.listview_settings['Sales Invoice'] = {
    refresh: function(listview) {
        // var from_date = listview.filter_list.find(function(field) { });
        // var to_date = listview.filter_list.find(function(field) { });
        // var company = listview.filter_list.find(function(field) { });

        listview.page.add_menu_item(__("Export XML"), () => {
            frappe.new_doc("EFE XML Export");
            // var w = window.open(
            //     frappe.urllib.get_full_url("/api/method/erpnext_fattura_elettronica.erpnext_fattura_elettronica.doctype.efe_xml_export.efe_xml_export.generate_electronic_invoices?"
            //     + "from_date=" + encodeURIComponent(frm.doc.from_date)
            //     + "&to_date=" + encodeURIComponent(frm.doc.to_date)
            //     + "&company=" + encodeURIComponent(frm.doc.company)
            //     + "&export_doc_name=" + encodeURIComponent(frm.doc.name))
            // );
            // if (!w) {
            //     frappe.msgprint(__("Please enable pop-ups")); return;
            // }
        });
    }
};