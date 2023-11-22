import requests
from setuptools import find_packages, setup


def read_file(fname):
    with open(fname, encoding="utf-8") as fd:
        return fd.read()


def get_version():
    """Get the version number."""
    url = "https://api.github.com/repos/silvxlabs/fastfuels-sdk-python/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    version = response.json()["tag_name"]
    return version[1:]  # Remove the leading "v" from the version number


def get_requirements(fname):
    with open(fname, encoding="utf-8") as fd:
        reqs = [line.strip() for line in fd if line]
    return reqs


NAME = "fastfuels-sdk"
DESCRIPTION = "3D Fuels for Next Generation Fire Models"
LONG_DESCRIPTION = read_file("README.md")
VERSION = get_version()
LICENSE = "MIT"
URL = "https://github.com/silvxlabs/fastfuels-sdk-python"
PROJECT_URLS = {
    "Bug Tracker": f"{URL}/issues"
}
INSTALL_REQUIRES = get_requirements("requirements/requirements.txt")

print(NAME, VERSION)

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license=LICENSE,
    url=URL,
    project_urls=PROJECT_URLS,
    classifiers=["Intended Audience :: Developers",
                 "Intended Audience :: Science/Research",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.9",
                 "Programming Language :: Python :: 3.10",
                 "Programming Language :: Python :: 3.11",
                 "Programming Language :: Python :: 3.12",
                 "Topic :: Scientific/Engineering", ],
    package_dir={"": "."},
    packages=find_packages(exclude=["docs", "tests"]),
    package_data={
        'fastfuels_sdk': ['templates/*.template'],
    },
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    python_requires=">=3.8",
)
