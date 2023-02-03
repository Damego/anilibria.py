from codecs import open

import tomli
from setuptools import setup, find_packages


with open("pyproject.toml", "rb") as f:
    pyproject = tomli.load(f)


with open("README.md", "r", encoding="utf-8") as f:
    README = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read()

with open("requirements-docs.txt", "r", encoding="utf-8") as f:
    requirements_docs = f.read()


setup(
    name=pyproject["tool"]["tool"]["poetry"]["name"],
    version=pyproject["tool"]["poetry"]["version"],
    author="Damego",
    author_email="danyabatueff@gmail.com",
    description=pyproject["tool"]["poetry"]["description"],
    extras_require={"readthedocs": requirements_docs},
    include_package_data=True,
    install_requires=requirements,
    license="GPL-3.0 License",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Damego/anilibria.py",
    packages=find_packages(),
    python_requires=">=3.10",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
