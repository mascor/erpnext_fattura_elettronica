frappe.ui.form.on("Customer", {
    onload: function(frm) {
        filter_place_of_birth(frm);
    },
    efe_first_name: function(frm) {
        make_customer_name(frm);
    },
    efe_last_name: function(frm) {
        make_customer_name(frm);
    },
    efe_generate_codice_fiscale: function(frm) {
        var prerequisites_valid = efe_check_cf_prerequisites(frm); 
        if (!prerequisites_valid) {
            frappe.msgprint(
                __("Please ensure these fields have valid values: <ul><li>First Name</li><li>Last Name</li><li>Gender</li><li>Date of Birth</li><li>Place of Birth</li></ul>."),
                __("Generate Codice Fiscale")
            );
        } else {
            frappe.call({
                method: "erpnext_fattura_elettronica.utilities.generate_codice_fiscale",
                args: {
                    first_name: frm.doc.efe_first_name, 
                    last_name: frm.doc.efe_last_name, 
                    date_of_birth: frm.doc.efe_date_of_birth, 
                    gender: frm.doc.gender, 
                    place_of_birth: frm.doc.efe_place_of_birth
                }
            }).done(function(r) {
                frm.set_value("efe_codice_fiscale", r.message);
                if (!frm.doc.tax_id) frm.set_value("tax_id", r.message);
            }).error(function(err) {
                frappe.show_alert(__("Unable to set codice fiscale"));
            });
        }
    },
    efe_validate_codice_fiscale: function(frm) {
        frappe.call({
            method: "erpnext_fattura_elettronica.utilities.validate_codice_fiscale",
            args: {
                codice_fiscale: frm.doc.efe_codice_fiscale,
            }
        }).done(function(r) {
            frappe.msgprint(r.message);
        }).error(function(err) {
            frm.show_alert(__("Unable to set codice fiscale"));
        });    
    },
});

//Utilites
function efe_check_cf_prerequisites(frm) {    
    if(!frm.doc.efe_first_name ||
        !frm.doc.efe_last_name ||
        !frm.doc.efe_date_of_birth ||
        !frm.doc.efe_place_of_birth ||
        !frm.doc.gender
        ) {
        return false;
    }
    return true;
}
function make_customer_name(frm) {
    frm.set_value(
        "customer_name", 
        [frm.doc.efe_last_name, frm.doc.efe_first_name].join(" ").trim()
    );
}
function filter_place_of_birth(frm) {
    frm.set_query("efe_place_of_birth", function() {
        return {
            "filters": {
                "is_group": 0
            }
        };
    })
}