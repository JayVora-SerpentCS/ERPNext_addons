# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pip.req import parse_requirements
import re, ast

# get version from __version__ variable in mass_editing/__init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('mass_editing/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

requirements = parse_requirements("requirements.txt", session="")

setup(
	name='mass_editing',
	version=version,
	description='"You can add, update or remove the values of more than one records on the fly at the same time."',
	author='"Serpent Consulting Services Pvt. Ltd."',
	author_email='"support@serpentcs.com"',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[str(ir.req) for ir in requirements],
	dependency_links=[str(ir._link) for ir in requirements if ir._link]
)
