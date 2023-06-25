import frappe
from frappe import _
import json


@frappe.whitelist()
def make_timesheet(doc):
	if not isinstance(doc, dict):
		doc = frappe._dict(json.loads(doc))

	timesheet = frappe.new_doc("Time Sheet Record")

	timesheet.project = doc.project
	timesheet.customer =  doc.customer
	timesheet.activity_type =  doc.activity_type
	timesheet.task =  doc.task
	timesheet.from_time =  doc.from_time
	timesheet.expected_time =  doc.expected_time
	timesheet.goal = doc.goal

	timesheet.submit()
	
	return timesheet.name

