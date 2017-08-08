# -*- coding: utf-8 -*-
# Copyright (c) 2017, Serpent Consulting Services Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class MassEditing(Document):
	pass

@frappe.whitelist()
def get_others_fields_values(mass_doc_field):
    if mass_doc_field:
        doc_field_rec = frappe.get_doc("DocField", mass_doc_field)
        return {'field_label': doc_field_rec.label,
                'field_name': doc_field_rec.fieldname,
                'field_type': doc_field_rec.fieldtype}
    else:
        return {'field_label': '',
                'field_name': '',
                'field_type':''}