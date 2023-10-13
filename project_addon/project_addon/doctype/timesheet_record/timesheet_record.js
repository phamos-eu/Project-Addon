// Copyright (c) 2023, Furqan Asghar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Timesheet Record', {
	refresh: function(frm) {
		if(!frm.is_new() && frm.doc.docstatus==0) {
			frm.add_custom_button(__('Mark Complete'), function() {
				frm.trigger("mark_complete");
			});
		}

		if(frm.is_new()) {
			frm.set_value("from_time", frappe.datetime.now_datetime());
			frm.refresh_field("from_time");
		}
		
	},

	project: function(frm) {
		//Filter task based on project if project is selected first
		frm.set_query("task", () => {
			let filters = {};
			if (frm.doc.project) filters["project"] = frm.doc.project;
			return {
				filters: filters
			}
		});
	},
	task: function(frm) {
		//set project if task is clicked first
		if(!frm.doc.project){
				frappe.db.get_value('Task', frm.doc.task, 'project', (r) => {
					frm.set_value("project",r.project);
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
				method:"project_addon.project_addon.doctype.timesheet_record.timesheet_record.mark_complete_validate",
				args: {
					"doc": frm.doc.name,
					"result": values.result,
					"to_time": values.to_time
				},
				callback: function(r) {
					if(!r.exc && r.message.status === true){
						frm.set_value("to_time", values.to_time);
						frm.set_value("result", values.result);
						frm.save();
					}
				}
			});
		})
	}
});
