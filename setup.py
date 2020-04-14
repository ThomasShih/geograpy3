"""Setup script for Geograpy Library."""
from setuptools import setup

"""Everything below is out of date, as of the fork by Thomas Shih"""
try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
    print(long_description)
except Exception as e:
    print("Import Error: {}".format(e))
    long_description = open('README.md').read()

setup(name='geograpy4',
      version='1.0.1',
      description='Extract locations from a URL or text and returns the geocoded data',
      long_description=long_description,
      url='https://github.com/ThomasShih/geograpy4',
      download_url='https://github.com/ThomasShih/geograpy4',
      author='Thomas Shih',
      author_email='tshih113@gmail.com',
      license='MIT',
      packages=['geograpy4'],
      install_requires=['numpy', 'nltk', 'jellyfish', 'pycountry', 'newspaper3k','geopy'],
      package_data={'geograpy4': ['data/*.csv']},
      zip_safe=False)
