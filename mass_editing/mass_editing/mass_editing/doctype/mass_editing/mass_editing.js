// Copyright (c) 2017, Serpent Consulting Services Pvt. Ltd. and contributors
// For license information, please see license.txt

// Added filter to select mass editing doc lines as per selected doc type
cur_frm.fields_dict["fields_ids"].grid.get_field("mass_doctype_field").get_query =
function(doc) {
	return {
	    'filters': {'parent': doc.model_id},
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
			frappe.model.set_value(cdt, cdn, "field_name", null);
		}
 	},
});

// Added button to pop up dialog when click on button
//frappe.ui.form.on('Mass Editing', {
//	refresh: function(frm) {
//	    cur_frm.add_custom_button(__('Mass Editing Dialog Testing'),
//					cur_frm.cscript['TESTING MASS DIALOG']);
//	}
//});

// Created one test dialog to pop up it on button click
//cur_frm.cscript['TESTING MASS DIALOG'] = function(){
//	var dialog = new frappe.ui.Dialog({
//		title: "Mass Editing Testing Dialog",
//		fields: [
//			{"fieldtype": "Text", "label": __("Reason for losing"), "fieldname": "reason",
//				"reqd": 1 },
//			{"fieldtype": "Button", "label": __("Update"), "fieldname": "update"},
//		]
//	});
//	dialog.fields_dict.update.$input.click(function() {
//		var args = dialog.get_values();
//		if(!args) return;
//		return cur_frm.call({
//			method: "declare_mass_order_lost",
//			doc: cur_frm.doc,
//			args: args.reason,
//			callback: function(r) {
//				if(r.exc) {
//					frappe.msgprint(__("There were errors."));
//					return;
//				}
//				dialog.hide();
//				cur_frm.refresh();
//			},
//			btn: this
//		})
//	});
//	dialog.show();
//}