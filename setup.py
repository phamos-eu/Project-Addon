from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in project_addon/__init__.py
from project_addon import __version__ as version

setup(
	name="project_addon",
	version=version,
	description="Addon for Erpnext Project Module",
	author="Furqan Asghar",
	author_email="furqan.asghar@phamos.eu",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
