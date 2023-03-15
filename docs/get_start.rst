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

.. important::

   In this :mod:`astroph_new` module,  downloading new submissions from
   `astro-ph`_, searching based on user interests, and making a summary
   report of the search results are performed in three steps by
   :func:`get_new`, :func:`search_new`, and :func:`make_report`.
   However, since each step automatically calls the previous step function,
   you can skip this section and only need to run :func:`make_report`.

The :func:`get_new` function opens `new <https://arxiv.org/list/astro-ph/new>`_
page of `astro-ph`_ in the virtual web browser using the :mod:`selenium` module
and downloads the page source. Abstracts in `astro-ph`_ are compiled with
`mathjax <https://www.mathjax.org/>`_, which takes some running time.
So, :func:`get_new` will repeat the download with an interval of 5 seconds
and check no changes to the page source. The :func:`get_new` returns the
processed download result as a Python dictionary with key names
``class``, ``link``, ``title``, ``author``, and ``abstract``.

>>> newsub = apn.get_new()
>>> newsub.keys()
dict_keys(['class', 'link', 'title', 'author', 'subject', 'abstract'])

The :func:`search_new` function searches interested new submissions
based on the user interests, which is saved in the running folder with the
given name by ``file``. The :func:`search_new` returns a python tuple
that contains the output of :func:`get_new` and an index list of the
interested submissions.

>>> newsub, idx = apn.search_new()
keyword 'molecular cloud' is found in the title of [10] (https://arxiv.org/abs/2303.07410)
keyword 'starless' is found in the title of [19] (https://arxiv.org/abs/2303.07501)
keyword 'molecular cloud' is found in the abstract of [10] (https://arxiv.org/abs/2303.07410)
keyword 'starless' is found in the abstract of [19] (https://arxiv.org/abs/2303.07501)
keyword 'molecular cloud' is found in the abstract of [36] (https://arxiv.org/abs/2303.07628)
keyword 'starless' is found in the abstract of [36] (https://arxiv.org/abs/2303.07628)
keyword 'molecular cloud' is found in the abstract of [41] (https://arxiv.org/abs/2303.07752)
keyword 'filament' is found in the abstract of [60] (https://arxiv.org/abs/2303.08088)

>>> print(idx)
[10, 19, 36, 41, 60]

Making summary report
=====================

The :func:`make_report` function creates an ``HTML`` document, which is the
summary report of the interested new submissions and can be quickly and
conveniently opened in any browser, such as ``Google Chrome`` or ``Safari``.

>>> apn.make_report()
keyword 'molecular cloud' is found in the title of [10] (https://arxiv.org/abs/2303.07410)
keyword 'starless' is found in the title of [19] (https://arxiv.org/abs/2303.07501)
keyword 'molecular cloud' is found in the abstract of [10] (https://arxiv.org/abs/2303.07410)
keyword 'starless' is found in the abstract of [19] (https://arxiv.org/abs/2303.07501)
keyword 'molecular cloud' is found in the abstract of [36] (https://arxiv.org/abs/2303.07628)
keyword 'starless' is found in the abstract of [36] (https://arxiv.org/abs/2303.07628)
keyword 'molecular cloud' is found in the abstract of [41] (https://arxiv.org/abs/2303.07752)
keyword 'filament' is found in the abstract of [60] (https://arxiv.org/abs/2303.08088)
'astro-ph_20230315.html' was saved.

The :func:`make_report` has the following options:

``prefix`` : string
    The prefix of the filename for saving the report HTML page.
    Default is ``'astro-ph'``

``datetag`` : bool
    Add a date tag at the end of the saved file name to prevent overwriting
    and preserve older reports. Default is ``True``.

``timetag`` : bool
    Add a time tag at the end of the saved file name. Default is ``False``.

``show`` : bool
    After the report is created, it is automatically displayed in the browser.
    Default is ``False``.

If you set the ``show`` option as ``True``, the :func:`make_report`
automatically displays the report page in the browser. For this feature,
you should set the ``'show'`` parameter, which is a shell command for opening
an HTML file in a browser, using :func:`set_params`. For example, if you use
``Google Chrome`` on the ``mac``, it is ``'open -a "Google Chrome"'``
(default).

>>> apn.set_params('show', 'open -a "Google Chrome"')
>>> apn.get_params('show')
'open -a "Google Chrome"'
>>> apn.make_report(show=True)

Scheduling for astroph_new
==========================

The :func:`run_apn` function executes :func:`make_report` at user-designated
time until the given end date. If the user-designated time has already passed
at the time starting :func:`run_apn`, :func:`make_report` will be executed
immediately, and from the next date, it will be executed at that time.

>>> apn.run_apn()
keyword 'molecular cloud' is found in the title of [10] (https://arxiv.org/abs/2303.07410)
keyword 'starless' is found in the title of [19] (https://arxiv.org/abs/2303.07501)
keyword 'molecular cloud' is found in the abstract of [10] (https://arxiv.org/abs/2303.07410)
keyword 'starless' is found in the abstract of [19] (https://arxiv.org/abs/2303.07501)
keyword 'molecular cloud' is found in the abstract of [36] (https://arxiv.org/abs/2303.07628)
keyword 'starless' is found in the abstract of [36] (https://arxiv.org/abs/2303.07628)
keyword 'molecular cloud' is found in the abstract of [41] (https://arxiv.org/abs/2303.07752)
keyword 'filament' is found in the abstract of [60] (https://arxiv.org/abs/2303.08088)
'astro-ph_20230315.html' was saved.
Next searching: 2023-03-16 11:00
Waiting ...

.. warning::

   The :func:`run_apn` is not a daemon that runs in the background,
   so it is terminated when you close the running Python shell or terminal.

You can designate the time and end date for :func:`run_apn`.

``at`` : string, ``'HH:MM'``
    a daily search and report generation time. Default is ``'11:00'``.

``end`` : string, ``'yyyy-mm-dd'``
    the end date of :func:`run_apn`. If not given, it is automatically set
    to 4 days later. For example, if you start :func:`run_apn` on Monday,
    the end date will be set Friday.

>>> apn.run_apn(at='12:30', end='2023-12-31')
Next searching: 2023-03-16 12:30
Waiting ...

The :func:`run_apn` delivers input arguments to the :func:`make_report` and
:func:`search_new`. So, you can set the ``file``, ``prefix``, ``datetag``,
``timetag``, and ``show`` options for all daily executions.

>>> apn.run_apn(at='11:00', end='2023-03-31', file='keywords_ppdisk',\
                prefix='ppdisk', show=True)
author 'Expert, P. Disk' is found in [#] (https://arxiv.org/abs/####.#####)
keyword 'protoplanetary disk' is found in [#] (https://arxiv.org/abs/####.#####)
keyword 'transitional disk' is found in [#] (https://arxiv.org/abs/####.#####)
'ppdisk_20230315.html' was saved.
Next searching: 2023-03-16 11:00
Waiting ...

.. contents::

