import sys
from setuptools import setup

args = ' '.join(sys.argv).strip()
if not any(args.endswith(suffix) for suffix in ['setup.py check -r -s', 'setup.py sdist']):
    raise ImportError('This is a unique description. Locked by pypi-parker at example-url.co.net.',)

setup(
    author='pypi-parker',
    author_email='park-email@example-url.co.net',
    classifiers=['Development Status :: 7 - Inactive'],
    description='This is a unique description. Locked by pypi-parker at example-url.co.net.',
    long_description='This is a unique description. Locked by pypi-parker at example-url.co.net.',
    name='testpackage-reloaded',
    url='example-url.co.net',
    version='3.1.4'
)
