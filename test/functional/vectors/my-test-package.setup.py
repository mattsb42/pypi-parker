import sys
from setuptools import setup

args = ' '.join(sys.argv).strip()
if not any(args.endswith(suffix) for suffix in ['setup.py check -r -s', 'setup.py sdist']):
    raise ImportError('parked using pypi-parker',)

setup(
    author='pypi-parker',
    author_email='park-email@example-url.co.net',
    classifiers=['Development Status :: 7 - Inactive'],
    description='parked using pypi-parker',
    long_description='This package has been parked either for future use or to protect against typo misdirection.\nIf you believe that it has been parked in error, please contact the package owner.',
    name='my-test-package',
    url='example-url.co.net',
    version='3.1.4'
)
