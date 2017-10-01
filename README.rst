###########
pypi-parker
###########

<TODO: ADD REASON FOR EXISTENCE>


What does it do?
****************
``pypi-parker`` provides a custom distutils Command ``park`` that interprets a provided config file
to generate empty Python packages. These packages will always throw an ImportError when someone tries
to install them, and you can customize the message that they throw to help guide users to the correct
package.

Using the Config File
=====================
``pypi-parker`` uses a `configparser`_ config file to determine what packages to generate and what metadata
to include with each.

There are two special sections: ``names`` and ``DEFAULT``.
* ``DEFAULT`` :: Values in ``DEFAULT`` are used if that key is not present in a package-specific section.
* ``names`` :: Keys in ``names`` are interpretted as package names that should all use only the values in ``DEFAULT``.

If you want to specify custom values for certain packages, you can add additional sections for those packages.
For any sections found aside from ``DEFAULT`` and ``names``, the section name is used as the package name.

With one exception (explained below), all key/value pairs loaded for each package are loaded
directly into the ``setup`` call for that generated package.

The ``description_keys`` key has special behavior: the line-delimited value is used with ``str.format``
to build the final ``description`` value.

Additionally, multiple lines may be provided for the ``classifiers``, and these will be split into separate entries.

If ``long_description`` is not defined, ``description`` is used for ``long_description``.

For example:

.. code::

    [my-package-name]
    author: Me, who else?
    url: https://github.com/my/package-name
    description: This package is parked by {author}. See {url} for more information.
    description_keys:
        author
        url
    classifiers:
        Development Status :: 7 - Inactive
        Operating System :: OS Independent
        Topic :: Utilities

Will result in:

.. code:: python

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

Default Values
==============
* ``config file name`` : ``park.cfg``
* ``classifiers`` : ``Development Status :: 7 - Inactive``
* ``description`` : ``This package has been parked either for future use or to protect against
    typo misdirection. If you believe that it has been parked in error, please contact the package owner.``

Ok, how do I use it?
********************
It's pretty simple, really.

#. Install ``pypi-parker`` wherever you will be running your builds.
#. Define the package names you want to target in your config file.
#. Call ``python setup.py park``.
    * If you want to use a custom config file, specify: ``python setup.py park --park-config={filename}``
#. Upload the resulting contents of ``dist`` to your package index of choice.

Example setup.py
^^^^^^^^^^^^^^^^

.. code:: python

    from setuptools import setup

    setup(install_requires=['pypi-parker'])

.. _configparser: https://docs.python.org/3/library/configparser.html
