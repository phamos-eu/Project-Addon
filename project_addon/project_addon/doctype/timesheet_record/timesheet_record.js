// Copyright (c) 2023, Furqan Asghar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Timesheet Record', {
	refresh: function(frm) {
		if(frm.doc.docstatus==0) {
			frm.add_custom_button(__('Mark Complete'), function() {
				frm.trigger("mark_complete");
			});
		}

		if(frm.is_new()) {
			frm.set_value("from_time", frappe.datetime.now_datetime());
			frm.refresh_field("from_time");
		}
	},
	

	mark_complete: function(frm) {
		frappe.prompt([
			{
				label: 'Time', fieldname: 'to_time', fieldtype: 'Datetime',
				default: frappe.datetime.now_datetime(), reqd: 1
			},
			{
				fieldtype: 'Column Break'
			},
			{
				label: 'What I did ', fieldname: 'result', 
				fieldtype: 'Small Text', reqd: 1
			},
		], (values) => {
			frappe.call({
				method:"project_addon.project_addon.doctype.timesheet_record.timesheet_record.mark_complete",
				args: {
					"doc": frm.doc.name,
					"result": values.result,
					"to_time": values.to_time
				},
				callback: function(r) {
					if(!r.exc){
						frm.refresh_field('to_time');
						frm.refresh_field('result');
					}
				}
			});
		})
	}
});
