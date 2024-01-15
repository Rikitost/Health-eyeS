from setuptools import setup

APP = ['Heltheye.py']
DATA_FILES = ['data', 'Healthfavicon.png']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['data'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
