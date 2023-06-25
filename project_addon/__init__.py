
__version__ = '0.0.1'

from erpnext.projects.doctype.project import project_dashboard
from project_addon.events.project import get_data
project_dashboard.get_data = get_data