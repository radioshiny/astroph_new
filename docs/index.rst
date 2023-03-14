===========
astroph_new
===========

:Release: |version|
:date: |today|

``astropy_new`` is a python functions to search for
`new astrophysics submissions <https://arxiv.org/list/astro-ph/new>`_
in `arXiv <https://arxiv.org>`_ based on the user interests and to create a
summarized document that can be easily opened in a browser.

..
    .. contents:: Table of Contents
        :depth: 2

Features
========

- Managing user interests (subjects, author names, and keywords)
- Searching for new submissions in
  `astro-ph <https://arxiv.org/list/astro-ph/new>`_ based on the user interests
- Creating a summary report for the interested submissions

Installation
============

Using pip
---------

Assuming you have Python already,
install ``astroph_new`` with ``pip`` simply run:

.. code-block:: bash

   pip install git+https://github.com/radioshiny/astroph_new

Checking installation
---------------------

If your installation is OK, you can import this module without any error:

.. code-block:: bash

   python -c 'import astroph_new'


Documentation
=============

.. toctree::
   :maxdepth: 2

   get_start

..
    Indices and tables
    ==================

    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`
