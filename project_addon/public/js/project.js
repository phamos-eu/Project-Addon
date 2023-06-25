frappe.ui.form.on("Project", {
	refresh: function (frm) {
		frm.trigger("set_custom_buttons");
	},

	set_custom_buttons: function (frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__('Make Timesheet'), () => {
				frm.trigger("making_timesheet");

			}, __("Actions"));
		}
	},

	making_timesheet(frm) {
		frappe.require("assets/project_addon/js/time_sheet_dialog.js", function() {
			new erpnext.project_addon.MakeTimeSheetDialog({
				doc: frm.doc,
			});
		})
	},
});