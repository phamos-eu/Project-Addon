# Copyright (c) 2023, Furqan Asghar and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cstr, now_datetime, time_diff_in_seconds, get_datetime

class TimeSheetRecord(Document):
	def validate(self):
		self.validate_time()
		self.set_actual_time()
		self.set_status()

	def validate_time(self):
		now_time = now_datetime()
		if self.from_time and now_time < get_datetime(self.from_time):
			frappe.throw(_("{0} cannot be in future").format(frappe.bold("Start Time")))

		if self.to_time and now_time < get_datetime(self.to_time):
			frappe.throw(_("{0} cannot be in future").format(frappe.bold("End Time")))

		if self.from_time and self.to_time and time_diff_in_seconds(self.to_time, self.from_time) < 0:
			frappe.throw(
				_("{0} can not be greater than {1}").format(
					frappe.bold("Start Time"), frappe.bold("End Time")
				)
			)

	def before_cancel(self):
		self.set_status()

	def set_actual_time(self):
		if self.from_time and self.to_time:
			self.actual_time = time_diff_in_seconds(self.to_time, self.from_time)

	def set_status(self):
		self.status = {"0": "Draft", "1": "Submitted", "2": "Cancelled"}[ str(self.docstatus or 0)]

		if self.timesheet:
			self.status = "Approved"

		if self.completed:
			self.status = "Completed"

@frappe.whitelist()
def mark_complete(doc, result, to_time):
	doc = frappe.get_doc("Time Sheet Record", doc)
	doc.result = result
	doc.to_time = to_time
	doc.completed = 1

	doc.validate()
	doc.flags.ignore_validate_update_after_submit = True
	doc.save()
