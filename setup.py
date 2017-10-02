"""PyPI Parker - Combatting Typosquatting"""
import os
import re

from setuptools import find_packages, setup

VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')
HERE = os.path.abspath(os.path.dirname(__file__))


def read(*args):
    """Read complete file contents."""
    return open(os.path.join(HERE, *args)).read()


def get_version():
    """Read the version from this module."""
    init = read('src', 'pypi_parker', '__init__.py')
    return VERSION_RE.search(init).group(1)


def get_requirements():
    """Read the requirements file."""
    requirements = read('requirements.txt')
    return [r for r in requirements.strip().splitlines()]


setup(
    name='pypi-parker',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    version=get_version(),
    author='Matt Bullock',
    maintainer='Matt Bullock',
    author_email='matt.s.b.42@gmail.com',
    url='https://github.com/mattsb42/pypi-parker',
    description='',
    long_description=read('README.rst'),
    keywords='pypi warehouse distutils typosquating',
    license='Apache License 2.0',
    install_requires=get_requirements(),
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities'
    ],
    entry_points={
        'distutils.commands': [
            'park = pypi_parker:Park'
        ]
    }
)
