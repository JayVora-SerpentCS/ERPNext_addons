frappe.provide("frappe.views");
frappe.provide("frappe.ui.form");
frappe.provide("mass_editing");
frappe.provide("mass_editing.api");

frappe.ui.form.MassEditingDialog = Class.extend({
	init: function(opts){
		var me = this
		var mass_fields_list = []
		frappe.call({
			method: 'mass_editing.api.get_fields_for_mass_editing',
			args: {
				doctype: opts.doctype,
				mass_doctype : 'Mass Editing'
			},
			callback: function(r) {
                mass_fields_list = r.message['mass_fields']
                me.dialog = new frappe.ui.Dialog({
                    title: __('Mass Editing'),
                    fields: mass_fields_list,
                    primary_action: function() {
                        frappe.ui.update_docs_by_mass_editing(opts, me) },
                    primary_action_label: __("Mass Edit")
                })
                $.extend(me,  me.dialog);
                me.dialog.clear();
				me.dialog.show();
			}
		});
	},

});

// Added method to updated doc type records in mass or bulk
frappe.views.ListView = frappe.views.ListView.extend({
    init_menu: function () {
        this._super();
		this.make_mass_editing();
	},
    make_mass_editing: function () {
		var me = this;
		//Added Menu Mass Editing to pop dialog
		me.page.add_menu_item(__('Mass Editing'), function () {
            //  It will Return all the selected items from list view
			var docnames = me.get_checked_items().map(function (doc) {
				return doc.name;
			});
			if (docnames.length >= 1) {
				me.dialog = new frappe.ui.form.MassEditingDialog({
					obj: me,
					method: 'mass_editing.api.update_doc_records_by_mass_editing',
					doctype: me.doctype,
					docname: docnames,
					callback: function () {
						me.refresh(true);
					}
				});
			}
			else {
				frappe.msgprint(__('Select records for mass editing'))
			}
		}, true);
    }
});

frappe.ui.update_docs_by_mass_editing = function(opts, dialog) {
	var args = opts.obj.dialog.get_values();
	if(args) {
		return frappe.call({
			method: opts.method,
			args: $.extend(args, {
				doctype: opts.doctype,
				selected_doc_records: opts.docname,
			}),
			callback: function(r,rt) {
				if(!r.exc) {
					if(opts.callback){
						opts.callback(r);
					}
					dialog && dialog.hide();
				}
			},
			btn: this
		});
	}
}