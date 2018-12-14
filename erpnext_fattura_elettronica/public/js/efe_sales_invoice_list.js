frappe.listview_settings['Sales Invoice'] = {
    onload: function(listview) {
      listview.page.add_menu_item(__("Export XML"), () => {
          frappe.new_doc("EFE XML Export")
      });
    }
};