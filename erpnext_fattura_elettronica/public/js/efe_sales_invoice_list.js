frappe.listview_settings['Sales Invoice'] = {
    onload: function(listview) {
		listview.page.add_menu_item(__("Export XML"), () => {
            if (!listview.get_checked_items().length) {
                frappe.msgprint(__("Please select at least one Sales Invoice"));
            } else {
                listview.call_for_selected_items(
                    "erpnext_fattura_elettronica.fattura_elettronica.generate_xml",
                    {}
                );
            }
		});

	}
};