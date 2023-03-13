.. _gs:

***************
Getting started
***************

Creating Folder for astro-ph
============================

Create a folder where the astro-ph daily summaries will be stored in an
easy-to-access and frequently viewed path (e.g., ``~/Desktop/``).

.. code-block:: bash

   cd ~/Desktop
   mkdir astro-ph
   cd astro-ph

Configuring interests
=====================

Initializing and managing interests in the REPL mode of the Python shell is
convenient.
To make empty interests file::

   >>> import astroph_new as apn
   >>> apn.init_interest()
   'interests.txt' was initialized.

The default filename is ``interests.txt``, but you can use different filenames
for various purposes, e.g., separating interests by area of interest:

.. code-block:: python

    >>> apn.init_interest(file='keywords_for_polarization.txt')
    'keywords_for_polarization.txt' was initialized.

To add keywords of interest:

.. code-block:: python

    >>> subject = ['SR', 'GA']
    >>> author = ['Di Francesco, James', 'Neal J. Evans II', 'Caselli, Paola']
    >>> keyword = ['molecular cloud', 'filament', 'dense core', 'prestellar']
    >>> apn.add_interest(subject=subject, author=author, keyword=keyword)
    'SR' is added to the 'subject' list.
    'GA' is added to the 'subject' list.
    'Di Francesco, James' is added to the 'author' list.
    'Neal J. Evans II' is added to the 'author' list.
    'Caselli, Paola' is added to the 'author' list.
    'molecular cloud' is added to the 'keyword' list.
    'filament' is added to the 'keyword' list.
    'dense core' is added to the 'keyword' list.
    'prestellar' is added to the 'keyword' list.
    'interests.txt' was updated.

The interests has the following attributes,

* ``subject`` : interested categories in
  `astro-ph <https://arxiv.org/archive/astro-ph>`_

    * ``'GA'`` :  Astrophysics of Galaxies
    * ``'CO'`` :  Cosmology and Nongalactic Astrophysics
    * ``'EP'`` :  Earth and Planetary Astrophysics
    * ``'HE'`` :  High Energy Astrophysical Phenomena
    * ``'IM'`` :  Instrumentataion and Methods for Astrophysics
    * ``'SR'`` :  Solar and Stellar Astrophysics

* ``author`` :  interested authors (``Family, Given`` or ``Given Family``)
* ``keyword`` :  interested keywords for the title and abstract
  (case insensitive)

To check the interests list:

.. code-block:: python

    >>> interest = apn.read_interest()
    >>> print(interest['author'])
    ['Caselli, Paola', 'Di Francesco, James', 'Neal J. Evans II']

To add additional interests::

    >>> apn.add_interest(subject='IM')
    'IM' is added to the 'subject' list.
    'interests.txt' was updated.
    >>> apn.add_interest(author='Philip C. Myers')
    'Philip C. Myers' is added to the 'author' list.
    'interests.txt' was updated.

Obvious duplicates cannot be added::

    >>> apn.add_interest(author=['Paola Caselli', 'Myers, P. C.'])
    'Paola Caselli' is already exist in the 'author' list.
    'Myers, P. C.' is already exist in the 'author' list.
    Nothing changed!

Keyword searches for titles and abstracts ignore case,
but are sensitive to spaces and hyphens::

    >>> apn.add_interest(keyword=['starless', 'protostellar'])
    'starless' is added to the 'keyword' list.
    'protostellar' is added to the 'keyword' list.
    'interests.txt' was updated.
    >>> apn.add_interest(keyword=['proto-stellar', 'pre-stellar'])
    'proto-stellar' is added to the 'keyword' list.
    'pre-stellar' is added to the 'keyword' list.
    'interests.txt' was updated.
    >>> print(apn.read_interest()['keyword'])
    ['dense core', 'filament', 'molecular cloud', 'pre-stellar', 'prestellar',
     'proto-stellar', 'protostellar', 'starless']

