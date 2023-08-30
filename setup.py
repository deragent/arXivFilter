import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="arxiv-filter",
    version="0.3.5",
    description="Quickly filter the daily arXiv email for your interests.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/deragent/arXivFilter",
    author="deragent",
    author_email="github@deragent.net",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pyyaml", "PyQt5"],
    entry_points={
        "console_scripts": [
            "arxiv-filter=arxiv_filter.__main__:main",
        ]
    },
)
