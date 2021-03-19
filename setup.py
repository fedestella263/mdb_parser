from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="mdb_parser",
    version="0.0.3",
    packages=find_packages(),
    author="Federico Stella",
    author_email="fedestella263@gmail.com",
    description="Microsoft Access (.mdb, .accdb) database file parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fedestella263/mdb_parser",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="MIT"
)
