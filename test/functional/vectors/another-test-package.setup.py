import sys
from setuptools import setup

args = ' '.join(sys.argv).strip()
if not any(args.endswith(suffix) for suffix in ['setup.py check -r -s', 'setup.py sdist']):
    raise ImportError('This package has been parked either for future use or to protect against typo misdirection. If you believe that it has been parked in error, please contact the package owner.',)

setup(
    author='pypi-parker',
    author_email='park-email@example-url.co.net',
    classifiers=['another thing', 'thing 1'],
    description='This package has been parked either for future use or to protect against typo misdirection. If you believe that it has been parked in error, please contact the package owner.',
    long_description='\nWoo!\nOverriding the long description but not the short description.',
    name='another-test-package',
    url='example-url.co.net',
    version='3.1.4'
)
