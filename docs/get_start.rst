.. _gs:

.. _astro-ph: https://arxiv.org/archive/astro-ph

***************
Getting started
***************

Configuring interests
=====================

Creating folder for astro-ph
----------------------------

Create a folder where the astro-ph daily summaries will be stored in an
easy-to-access and frequently viewed path (e.g., ``~/Desktop/``).

.. code-block:: bash

   % cd ~/Desktop
   Desktop % mkdir astro-ph
   Desktop % cd astro-ph

.. note::

   Initializing and managing interests in the REPL mode of the Python shell is
   convenient.

.. code-block:: bash

   astro-ph % python

Initializing interests
----------------------

:mod:`astroph_new` searches interested new submissions in `astro-ph`_
based on the user interests, a list of interested subjects, authors,
and keywords. To initialize your interests, you can make an empty interests
file by using :func:`init_interest`:

>>> import astroph_new as apn
>>> apn.init_interest()
'.interests' was initialized.

The default filename for saving your interests is ``.interests``,
but you can use different filenames with ``file='filename'`` for various
purposes, e.g., separating interests by area of interest:

>>> apn.init_interest(file='keywords_for_polarization')
'keywords_for_polarization' was initialized.

The :func:`init_interest` has three options:

``file`` : string
    file name to save the interests

``default`` : bool
    update the default filename to ``file``, default is ``False``

``overwrite`` : bool
    overwrite to the existing file, default is ``False``

You can change the default filename with an option of ``default=True`` or
with the :func:`set_params` function.

>>> apn.init_interest(file='.mykeywords', default=True)
The default file name was changed to '.mykeywords'.
'.mykeywords' was initialized.

>>> apn.set_params('file', '.interests')
>>> apn.init_interest(overwrite=True)
'.interests' was initialized.

Managing interests
------------------

The :mod:`astroph_new` module contains functions helpful in managing user
interests stored in the file name (or path) given by ``file``.

.. note::

   Functions that manage user interests, such as :func:`read_interest`,
   :func:`add_interest`, and :func:`remove_interest`, have an input parameter
   ``file`` specifying the name of the user interests file.
   If it is not given, the default file name is used, which was set in
   :func:`init_interest` or :func:`set_params` and can be checked with
   :func:`get_params`.

   >>> apn.get_params('file')
   '.interests'

You can add the interested categories of `astro-ph`_, interested author names,
and search keywords for the titles or abstracts into your interests list
using :func:`add_interest`.

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

The :func:`add_interest` has the following inputs,

``subject`` : string or list of strings
    interested categories in `astro-ph <https://arxiv.org/archive/astro-ph>`_

    * ``'GA'`` :  Astrophysics of Galaxies
    * ``'CO'`` :  Cosmology and Nongalactic Astrophysics
    * ``'EP'`` :  Earth and Planetary Astrophysics
    * ``'HE'`` :  High Energy Astrophysical Phenomena
    * ``'IM'`` :  Instrumentataion and Methods for Astrophysics
    * ``'SR'`` :  Solar and Stellar Astrophysics

``author`` :  string or list of strings
    interested authors (``Family, Given`` or ``Given Family``)

``keyword`` :  string or list of strings
    interested keywords for the title and abstract (case insensitive)

To check the interests list:

>>> interest = apn.read_interest()
>>> print(interest['author'])
['Caselli, Paola', 'Di Francesco, James', 'Neal J. Evans II']

To add additional interests:

>>> apn.add_interest(subject='IM')
'IM' is added to the 'subject' list.
'interests.txt' was updated.

>>> apn.add_interest(author='Philip C. Myers')
'Philip C. Myers' is added to the 'author' list.
'interests.txt' was updated.

Obvious duplicates cannot be added:

>>> apn.add_interest(author=['Paola Caselli', 'Myers, P. C.'])
'Paola Caselli' is already exist in the 'author' list.
'Myers, P. C.' is already exist in the 'author' list.
Nothing changed!

Keyword searches for titles and abstracts ignore case,
but are sensitive to spaces and hyphens:

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

To remove no longer used keywords of interest:

>>> apn.remove_interest(subject='IM', keyword='proto-stellar')
'IM' is removed from the 'subject' list.
'proto-stellar' is removed from the 'keyword' list.
'interests.txt' was updated.

.. note::

   You can access and update the saved user interests
   using text editors, such as ``vim`` or ``emacs``.

Searching based on interests
============================




