"""
py2app build script for MyApplication

Usage:
    python setup.py py2app
"""
from setuptools import setup
setup(
    app=["chaos.py"],
    options={
        'py2app': {'argv_emulation': True, 'packages': ['pygame']}
    },

    data_files=['sge.py', 'Assets', 'map.map'],
    setup_requires=["py2app"],
)
