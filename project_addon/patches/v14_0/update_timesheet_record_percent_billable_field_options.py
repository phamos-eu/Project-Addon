# Copyright (c) 2023, phamos GmbH and contributors
# For license information, please see license.txt

import frappe


def execute():
	options_map = {'0%': '0', '25%': '25', '50%': '50', '75%': '75', '100%': '100'}
	table = frappe.qb.DocType("Timesheet Record")
	records = frappe.qb.from_(table).select(table.name, table.percent_billable).run(as_dict=True)
	for d in records:
		if options_map.get(d.get('percent_billable')):
			frappe.qb.update(table).set('percent_billable', options_map.get(d.get('percent_billable'))).where(
				table.name == d.get('name')
			).run()
