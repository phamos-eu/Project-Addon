// Copyright (c) 2023, Furqan Asghar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Time Sheet Record', {
	refresh: function(frm) {
		if(frm.doc.docstatus==1 && frm.doc.status =='Submitted') {
			frm.add_custom_button(__('Mark Complete'), function() {
				frm.trigger("mark_complete");
			});
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
				method:"project_addon.project_addon.doctype.time_sheet_record.time_sheet_record.mark_complete",
				args: {
					"doc": frm.doc.name,
					"result": values.result,
					"to_time": values.to_time
				},
				callback: function(r) {
					if(!r.exc){
					}
				}
			});
		})
	}
});
