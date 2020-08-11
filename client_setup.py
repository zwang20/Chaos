"""
py2app build script for MyApplication

Usage:
    python setup.py py2app
"""
from setuptools import setup
setup(
    app=["client.py"],
    options={
        'py2app': {'argv_emulation': True, 'packages': ['socket', 'threading', 'tkinter']}
    },
    setup_requires=["py2app"],
)
