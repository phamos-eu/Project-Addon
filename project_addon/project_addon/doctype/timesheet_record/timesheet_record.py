# Copyright (c) 2023, Furqan Asghar and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cstr, now_datetime, time_diff_in_seconds, get_datetime

class TimesheetRecord(Document):
	def validate(self):
		self.validate_fields()
		self.set_actual_time()

	def validate_fields(self):
		if self.get("_action") and self._action == "submit":
			if not self.to_time:
				frappe.throw(_("Please set To Time"))

			if not self.result:
				frappe.throw(_("Please set Result"))

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

	def on_submit(self):
		self.create_timesheet()

	def create_timesheet(self):
		description = "{0} : {1}".format(self.goal, self.result)
		timesheet = frappe.new_doc("Timesheet")
		timesheet.project = self.project
		timesheet.customer = self.customer
		timesheet.note = description

		timesheet.append(
			"time_logs",
			{
				"billable": 1 if self.percent_billable else 0,
				"activity_type": self.activity_type,
				"from_time": self.from_time,
				"to_time": self.to_time,
				"expected_hours": round(float(self.expected_time) / 3600, 6),
				"hours": round(float(self.actual_time) / 3600, 6),
				"description": description,
				"project": self.project,
				"task": self.task
			},
		)
		timesheet.employee = self.employee

		timesheet.save()
		self.db_set('timesheet', timesheet.name)
		frappe.msgprint(_('Timesheet {0} Created').format(frappe.get_desk_link("Timesheet", timesheet.name)))


	def set_actual_time(self):
		if self.from_time and self.to_time:
			self.actual_time = time_diff_in_seconds(self.to_time, self.from_time)


@frappe.whitelist()
def mark_complete(doc, result, to_time):
	doc = frappe.get_doc("Timesheet Record", doc)
	doc.result = result
	doc.to_time = to_time

	doc.validate()
	doc.save()
