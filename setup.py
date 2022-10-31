import sys
import setuptools
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("LICENSE", "r", encoding="utf-8") as f:
    pkg_license = f.read()

# Save tag variable then remove from arguments for setup
tag = sys.argv[1]
del sys.argv[1]

setuptools.setup(
    name="dmp-cli",
    version=str(tag),
    author="Dale Bridges",
    author_email="dale.bridges@yahoo.co.uk",
    description="Data Management Platform CLI interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://{path-to-internal-repository}/platform/cloud/dmp-cli",
    license=pkg_license,
    # You must reference the top python package in repo first then reference all of the sub packages that will be used to run in this environment
    # e.g. package name `mypackage` has sub packages (directories with `__init__.py` files) `package1`,`package2`,`test` - then this will look like
    # `packages=["my_package", "my_package.package1", "my_package.package2"],`
    packages=find_packages(),
    install_requires=requirements,
    # Check standard python version. ~= means latest version i.e. ~=3.8 == 3.8.latest
    python_requires="~=3.8",
)