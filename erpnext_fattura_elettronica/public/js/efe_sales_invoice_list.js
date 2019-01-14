frappe.listview_settings['Sales Invoice']["refresh"] = function(listview) {
    listview.page.add_menu_item(__("Export XML"), () => {
        if (!listview.get_checked_items().length) {
            frappe.msgprint(__("Please select at least one invoice to export."))
            return
        }

        var names = listview.get_checked_items().map(function(item) { return item.name });
        var w = window.open(
            frappe.urllib.get_full_url("/api/method/erpnext_fattura_elettronica.export_invoices.generate_electronic_invoices?"
            + "names=" + encodeURIComponent(names))
        );
        if (!w) {
            frappe.msgprint(__("Please enable pop-ups")); return;
        }
    });
    
}