# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Mass Editing",
			"color": "grey",
			"icon": "assets/mass_editing/images/mass_editing_icon.svg",
			"type": "module",
			"label": _("Mass Editing")
		}
	]
