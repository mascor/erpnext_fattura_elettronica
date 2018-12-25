# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "erpnext_fattura_elettronica"
app_title = "Erpnext Fattura Elettronica"
app_publisher = "Massimiliano Corvino"
app_description = "App to export electronic invoice as mandated by the Italian Government"
app_icon = "fa fa-file-code-o"
app_color = "lightblue"
app_email = "massimiliano.corvino@gmail.com"
app_license = "GPLv3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erpnext_fattura_elettronica/css/erpnext_fattura_elettronica.css"
# app_include_js = "/assets/erpnext_fattura_elettronica/js/erpnext_fattura_elettronica.js"

# include js, css files in header of web template
# web_include_css = "/assets/erpnext_fattura_elettronica/css/erpnext_fattura_elettronica.css"
# web_include_js = "/assets/erpnext_fattura_elettronica/js/erpnext_fattura_elettronica.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

doctype_js = {
    "Sales Invoice" : "public/js/efe_sales_invoice.js",
    "Customer" : "public/js/efe_customer.js"
}

after_install = "erpnext_fattura_elettronica.install.after_install"

doctype_list_js = { "Sales Invoice" : "public/js/efe_sales_invoice_list.js" }

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "erpnext_fattura_elettronica.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "erpnext_fattura_elettronica.install.before_install"
# after_install = "erpnext_fattura_elettronica.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpnext_fattura_elettronica.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"erpnext_fattura_elettronica.tasks.all"
# 	],
# 	"daily": [
# 		"erpnext_fattura_elettronica.tasks.daily"
# 	],
# 	"hourly": [
# 		"erpnext_fattura_elettronica.tasks.hourly"
# 	],
# 	"weekly": [
# 		"erpnext_fattura_elettronica.tasks.weekly"
# 	]
# 	"monthly": [
# 		"erpnext_fattura_elettronica.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "erpnext_fattura_elettronica.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "erpnext_fattura_elettronica.event.get_events"
# }

fixtures = [
    {   
        "dt":"Custom Field", 
        "filters": [["name", "in", [
            "Customer Group-efe_is_pa",
            "Customer-efe_first_name",
            "Customer-efe_last_name",
            "Customer-efe_date_of_birth",
            "Customer-efe_place_of_birth",
            "Customer-efe_sb_1",
            "Customer-efe_pec_destinatario",
            "Customer-efe_codice_destinatario",
            "Customer-efe_cb_1",
            "Customer-efe_codice_fiscale",
            "Customer-efe_generate_codice_fiscale",
            "Customer-efe_validate_codice_fiscale",
            "Mode of Payment-efe_code",
            "Delivery Note-efe_transporter_tax_id",
            "Delivery Note-efe_transporter_codice_fiscale",
            "Address-efe_numero_civico",
            "Company-efe_sb1",
            "Company-efe_codice_fiscale",
            "Company-efe_cb1",
            "Company-efe_regime_fiscale",
            "Company-efe_esigibilita_iva",
            "Sales Invoice-efe_esigibilita_iva",
            "Sales Invoice-sb_efe1",
            "Sales Taxes and Charges-efe_natura",
            "Account-efe_natura",
            "Item Tax-efe_natura",
            "Territory-efe_cadastral_code"
        ]]]
    },
]
