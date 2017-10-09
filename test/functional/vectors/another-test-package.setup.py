import sys
from setuptools import setup

args = ' '.join(sys.argv).strip()
if not any(args.endswith(suffix) for suffix in ['setup.py check -r -s', 'setup.py sdist']):
    raise ImportError('parked using pypi-parker',)

setup(
    author='pypi-parker',
    author_email='park-email@example-url.co.net',
    classifiers=['another thing', 'thing 1'],
    description='parked using pypi-parker',
    long_description='\nWoo!\nOverriding the long description but not the short description.',
    name='another-test-package',
    url='example-url.co.net',
    version='3.1.4'
)
