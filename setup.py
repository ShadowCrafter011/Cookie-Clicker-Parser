from setuptools import setup, find_packages
from pathlib import Path


this_directory = Path(__file__).parent
print(this_directory)
long_description = (this_directory / "README.md").read_text()


setup(
    name="cookie-clicker-parser",
    version="1.0.1",
    description="Parser for Cookie Clicker save codes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ShadowCrafter",
    url="https://github.com/ShadowCrafter011/Cookie-Clicker-Parser",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    license="MIT",
    keywords=["parser", "cookie clicker"],
)

