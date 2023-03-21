===========
astroph_new
===========

:Release: |version|
:date: |today|

``astropy_new`` is a python module to search for
`new astrophysics submissions <https://arxiv.org/list/astro-ph/new>`_
in `arXiv <https://arxiv.org>`_ based on the user interests and to create a
summarized document that can be easily opened in a browser.


Features
========

- Managing user interests (subjects, author names, and keywords)
- Searching for new submissions in
  `astro-ph <https://arxiv.org/list/astro-ph/new>`_ based on the user interests
- Creating a summarized HTML document of the interested submissions
- Daily automatic searching and summary on a set time.

Installation
============

Using pip
---------

Assuming you have Python already,
install ``astroph_new`` with ``pip`` simply run:

.. code-block:: bash

   pip install -U astroph-new

Checking installation
---------------------

If your installation is OK, you can import this module without any error:

.. code-block:: bash

   python -c 'import astroph_new'


Documentation
=============

.. toctree::
   :maxdepth: 4
   :glob:

   get_start*

..
    Indices and tables
    ==================

    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`
