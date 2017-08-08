// Copyright (c) 2016, Serpent Consulting Services Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Mass Editing Script Report"] = {
	"filters": [
		{
			"fieldname":"model_id",
			"label": __("Doctype"),
			"fieldtype": "Link",
			"options": "DocType"
		}
	]
}
