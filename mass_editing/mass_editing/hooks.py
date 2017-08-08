# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "mass_editing"
app_title = "Mass Editing"
app_publisher = "Serpent Consulting Services Pvt. Ltd."
app_description = "You can add, update or remove the values of more than one records on the fly at the same time."
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "support@serpentcs.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/mass_editing/css/mass_editing.css"
app_include_js = "/assets/mass_editing/js/mass_editing.js"

# include js, css files in header of web template
# web_include_css = "/assets/mass_editing/css/mass_editing.css"
# web_include_js = "/assets/mass_editing/js/mass_editing.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "mass_editing.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "mass_editing.install.before_install"
# after_install = "mass_editing.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mass_editing.notifications.get_notification_config"

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
# 		"mass_editing.tasks.all"
# 	],
# 	"daily": [
# 		"mass_editing.tasks.daily"
# 	],
# 	"hourly": [
# 		"mass_editing.tasks.hourly"
# 	],
# 	"weekly": [
# 		"mass_editing.tasks.weekly"
# 	]
# 	"monthly": [
# 		"mass_editing.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "mass_editing.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------

override_whitelisted_methods = {
	"frappe.desk.search.search_link": "mass_editing.api.search_link",
	"frappe.desk.search.search_widget": "mass_editing.api.search_widget"
}

