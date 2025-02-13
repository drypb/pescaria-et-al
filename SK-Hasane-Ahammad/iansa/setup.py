
from setuptools import setup, find_packages

setup(
    name="iansa",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click",
        "requests",
        "pandas",
        "numpy",
        "validators",
        "tldextract",
        "validators",
        "urllib3"
    ],
    entry_points={
        "console_scripts": [
            "iansa=iansa.main:cli",
        ],
    },
)
