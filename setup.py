from setuptools import setup, find_packages
setup(
    name="PyHighcharts",
    version="0.1",
    package_dir={'': 'src'},
    packages=['pyhighcharts'],
    scripts=["bin/*"],

    install_requires=[],
    package_data={},

    # metadata for upload to PyPI
    author="",
    author_email="",
    description="",
    license="PSF",
    keywords="PyHighcharts",
    url="",  # project home page, if any
)
