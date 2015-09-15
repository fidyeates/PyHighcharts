from setuptools import setup

setup(
    name='PyHighcharts',
    version='1.0',
    packages=['PyHighcharts', 'PyHighcharts.highcharts'],
    url='https://github.com/fidyeates/PyHighcharts',
    license='PSF',
    author='Fin Yeates',
    author_email='findlay.yeates@deitek.co.uk',
    description='A python wrapper for the highcharts charting library',
    include_package_data=True,
    package_data={'PyHighcharts': ['templates/*.tmp']}
)
