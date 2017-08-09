// Copyright (c) 2017, Serpent Consulting Services Pvt. Ltd. and contributors
// For license information, please see license.txt

// Added filter to select mass editing doc lines as per selected doc type
cur_frm.fields_dict["fields_ids"].grid.get_field("mass_doctype_field").get_query =
function(doc) {
	return {
	    'filters': [
	        ['DocField', 'fieldtype', 'not in',
	        ['Table','Button', 'Column Break', 'Daynamic Link', 'Fold',
	        'Heading', 'HTML', 'Image', 'Read Only', 'Section Break']],
            ['DocField', 'parent', '=', doc.model_id]
        ],
	    'searchfield': 'fieldname'
	}
}

// Added method to get lable and fieldname when select mass_doc_field
// its works like onchange.
frappe.ui.form.on("Mass Editing line", {
	mass_doctype_field: function(frm, cdt, cdn) {
		var mass_doctype_field_rec = frappe.model.get_doc(cdt, cdn);
		if (mass_doctype_field_rec.mass_doctype_field) {
			// get label and fieldname
			frappe.call({
				method: "mass_editing.mass_editing.doctype.mass_editing.mass_editing.get_others_fields_values",
				args: {
					mass_doc_field: mass_doctype_field_rec.mass_doctype_field
				},
				callback: function(r) {
					frappe.model.set_value(cdt, cdn, "field_label", r
					.message.field_label);
					frappe.model.set_value(cdt, cdn, "field_name", r.message
					.field_name);
					frappe.model.set_value(cdt, cdn, "field_type", r.message
					.field_type);

				}
			});
		} else {
		    // If not field_name and label then set it to null
			frappe.model.set_value(cdt, cdn, "field_label", null);
			frappe.model.set_value(cdt, cdn, "field_name", null);
			frappe.model.set_value(cdt, cdn, "field_type", null);
		}
 	},
});