"""Setup script for Geograpy Library."""
from setuptools import setup

"""Everything below is out of date, as of the fork by Thomas Shih"""
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

setup(name='geograpy3',
      version='1.0.0',
      description='Extract countries, regions and cities from a URL or text',
      long_description=long_description,
      url='https://github.com/jmbielec/geograpy3',
      download_url='https://github.com/jmbielec/geograpy3',
      author='Matthew Bielec',
      author_email='jmbielec@terpmail.umd.edu',
      license='MIT',
      packages=['geograpy3'],
      install_requires=['numpy', 'nltk', 'jellyfish', 'pycountry', 'newspaper3k'],
      package_data={'geograpy3': ['data/*.csv']},
      zip_safe=False)
