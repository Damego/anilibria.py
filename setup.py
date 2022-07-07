import re
from codecs import open
from os import path

from setuptools import setup, find_packages


PACKAGE_NAME = "anilibria.py"
HERE = path.abspath(path.dirname(__file__))

with open("README.md", "r", encoding="utf-8") as f:
    README = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read()

with open("requirements-docs.txt", "r", encoding="utf-8") as f:
    requirements_docs = f.read()

with open(path.join(HERE, "anilibria", "__init__.py"), encoding="utf-8") as fp:
    VERSION = re.search('__version__ = "([^"]+)"', fp.read())[1]


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author="Damego",
    author_email="danyabatueff@gmail.com",
    description="The async API wrapper for anilibria.tv",
    extras_require={"readthedocs": requirements_docs},
    include_package_data=True,
    install_requires=requirements,
    license="GPL-3.0 License",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Damego/anilibria.py",
    packages=find_packages(),
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
