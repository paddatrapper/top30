from setuptools import setup

setup(
    name="Top30Creator",
    version="0.1.0",
    author="Kyle Robbertze",
    author_email="krobbertze@gmail.com",
    packages=["top30"],
    data_files=[
        ("top30", ["top30/config.yaml"]),
        ("top30", ["top30/mainWindow.glade"]),
        ("/usr/bin",
        ],
    scripts=["scripts/top30"],
    url="http://pypi.python.org/pypi/Top30Creator_v010/",
    license="LICENCE.md",
    description="Creates rundowns for radio shows",
    long_description=open("README").read(),
    install_requires=[
        "mutagen",
        "pydub",
        "pyyaml",
        "gi",
    ],
)
