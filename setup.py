from setuptools import setup


setup(
    name="bk",
    version="0.1",
    py_module=["bk"],
    install_requires=[
        "Click",
    ],
    entry_points='''
        [console_scripts]
        bk=bk:cli
    ''',
)