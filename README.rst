###########
pypi-parker
###########

.. image:: https://img.shields.io/pypi/v/pypi-parker.svg
   :target: https://pypi.python.org/pypi/pypi-parker
   :alt: Latest Version

.. image:: https://readthedocs.org/projects/pypi-parker/badge/
   :target: https://pypi-parker.readthedocs.io/en/stable/
   :alt: Documentation Status

.. image:: https://travis-ci.org/mattsb42/pypi-parker.svg?branch=master
   :target: https://travis-ci.org/mattsb42/pypi-parker

``pypi-parker`` lets you easily park package names on PyPI to protect users of your packages
from typosquatting.

`Typosquatting`_ is a problem: in general, but also on PyPI. There are efforts being taken
by pypa to `protect core library names`_, but this does not (and really cannot and probably
should not attempt to) help individual package owners. For example, ``reqeusts`` rather than
``requests``, or ``crytpography`` rather than ``cryptography``. Because of the self-serve
nature of PyPI, individual package owners are left to their own devices to protect their users.
This is not inherently a problem: in my opinion this is a reasonable balance to keep the barrier
to entry for publishing PyPI package low. However, tooling should exist to make it easy for
package owners to protect their users. That is what ``pypi-parker`` sets out to do.

Objectives
**********
* Self-serve is a good thing. Let's not try and get rid of that. Work with it instead.
* Package owners should be able to easily protect users of their packages from malicious typosquatting.
* It should be easy for package owners to introduce ``pypi-parker`` into their existing package builds.
* Parked packages should:

  * fail fast and not `do anything else`_
  * be self documenting, both in metadata and in source
  * contain functionally complete ``setup.py`` files to allow whitelisted external validators to work

    * The `readme_renderer`_ validator is run on each generated package before building.

What does it do?
****************
``pypi-parker`` provides a custom distutils command ``park`` that interprets a provided config
file to generate empty Python package source distributables. These packages will always throw
an ImportError when someone tries to install them. You can customize the ImportError message
to help guide users to the correct package.

Using the Config File
=====================
``pypi-parker`` uses a `configparser`_ config file to determine what packages to generate and what metadata
to include with each.

There are two special sections: ``names`` and ``DEFAULT``.

* ``DEFAULT`` : Values in ``DEFAULT`` are used if that key is not present in a package-specific section.
* ``names`` : Keys in ``names`` are interpretted as package names that should all use only the values in ``DEFAULT``.

Unless otherwise indicated, all key/value pairs loaded for each package are loaded directly
into the ``setup`` call for that generated package.

Special Packages
----------------

If you want to specify custom values for specific packages, you can add additional sections
for those packages. For any sections found aside from ``DEFAULT`` and ``names``, the section
name is used as the package name.

Special Section Keys
--------------------

* ``description_keys`` : This line-delimited value is used with ``str.format`` to build the
  final ``description`` value.
* ``classifiers`` : If multiple lines are provided for this value, and each line will be treated
  as a separate entry.
* ``long_description`` : If not defined, ``description`` is used.
* ``description`` : This value is also used for the ``ImportError`` message in the generated
  ``setup.py``.

Default Values
==============
* **config file name** : ``park.cfg``
* **classifiers** : ``Development Status :: 7 - Inactive``
* **description** :

    .. code-block:: text

      This package has been parked either for future use or to protect against typo misdirection.
      If you believe that it has been parked in error, please contact the package owner.

Example
-------

**park.cfg**

.. code-block:: ini

    [DEFAULT]
    author: mattsb42

    [my-package-name]
    url: https://github.com/mattsb42/my-package-name
    description: This package is parked by {author}. See {url} for more information.
    description_keys:
        author
        url
    classifiers:
        Development Status :: 7 - Inactive
        Operating System :: OS Independent
        Topic :: Utilities

**Generated setup.py**

.. code-block:: python

    from setuptools import setup

    args = ' '.join(sys.argv).strip()
    if not any(args.endswith(suffix) for suffix in ['setup.py sdist', 'setup.py check -r -s']):
        raise ImportError('This package is parked by mattsb42. See https://github.com/mattsb42/my-package-name for more information.')

    setup(
        author='mattsb42',
        url='https://github.com/mattsb42/my-package-name',
        description='This package is parked by mattsb42. See https://github.com/mattsb42/my-package-name for more information.',
        classifiers=[
            'Development Status :: 7 - Inactive',
            'Operating System :: OS Independent',
            'Topic :: Utilities'
        ]
    )

**Install attempt**

.. code-block:: sh

    $ pip install my-package-name
    Processing my-package-name
        Complete output from command python setup.py egg_info:
        Traceback (most recent call last):
          File "<string>", line 1, in <module>
          File "/tmp/pip-oma2zoy6-build/setup.py", line 6, in <module>
            raise ImportError('This package is parked by mattsb42. See https://github.com/mattsb42/my-package-name for more information.',)
        ImportError: This package is parked by mattsb42. See https://github.com/mattsb42/my-package-name for more information.

        ----------------------------------------
    Command "python setup.py egg_info" failed with error code 1 in /tmp/pip-oma2zoy6-build/

Ok, how do I use it?
********************

1. Install ``pypi-parker`` wherever you will be running your builds.

  .. code-block:: sh

    pip install pypi-parker

2. Define the package names you want to target in your config file.
3. Call ``setup.py`` with the ``park`` command.

  .. code-block:: sh

    python setup.py park

  * If you want to use a custom config file, specify it with the ``park-config`` argument.

    .. code-block:: sh

      python setup.py park --park-config={filename}

4. Upload the resulting contents of ``dist`` to your package index of choice.

**Example tox configuration**

.. code-block:: ini

    [testenv:park]
    basepython = python3.6
    deps =
        setuptools
        pypi-parker
    commands = python setup.py park

.. _configparser: https://docs.python.org/3/library/configparser.html
.. _do anything else: http://incolumitas.com/2016/06/08/typosquatting-package-managers/
.. _readme_renderer: https://github.com/pypa/readme_renderer
.. _Typosquatting: https://en.wikipedia.org/wiki/Typosquatting
.. _protect core library names: https://github.com/pypa/warehouse/issues/2151
