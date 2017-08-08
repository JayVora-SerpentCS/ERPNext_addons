# Copyright (c) 2013, Serpent Consulting Services Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	# columns, data = [], []
	columns = get_report_columns()
	data = get_report_data(filters)
	return columns, data

def get_report_columns():
	columns = [{
		"fieldname": "name",
		"label": _("Mass Editing Name"),
		"fieldtype": "Link",
		"options": "Mass Editing",
		"width": 200
	},
	{
		"fieldname": "model_id",
		"label": _("Doctype"),
		"fieldtype": "Link",
		"options": "DocType",
		"width": 200
	}
	]
	return columns

def get_report_data(filters=None):
	data = get_orders(filters)
	return data

def get_orders(filters):
	additional_conditions = get_additional_report_conditions(filters)
	test_q = """select name,model_id \
		from `tabMass Editing` {additional_conditions}""".format(additional_conditions=additional_conditions)
	return frappe.db.sql(test_q, as_dict=True)

def get_additional_report_conditions(filters):
	additional_conditions = []
	if filters.get("model_id"):
		additional_conditions.append(get_model_id_cond(filters.get("model_id")))
	test = "{}".format(" ".join(additional_conditions)) if additional_conditions else ""
	return test

def get_model_id_cond(model_id):
	return (""" where model_id = '%s'"""%(str(model_id)))
