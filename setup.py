# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name='project',
    version='1.0',
    packages=find_packages(),
    package_data={'sales_monitor': ['resources/*.json', 'templates/*.html']},
    scripts=['bin/monitor_handler.py'],
    entry_points={'scrapy': ['settings = sales_monitor.settings']},
)
