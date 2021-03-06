"""
py2app build script for MyApplication

Usage:
    python setup.py py2app
"""
from setuptools import setup
setup(
    app=["main.py"],
    options={
        'py2app': {'argv_emulation': True, 'packages': ['pygame']}
    },

    data_files=['Assets'],
    setup_requires=["py2app"],
)
