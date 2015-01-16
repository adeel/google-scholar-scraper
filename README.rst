**********************
google-scholar-scraper
**********************

Version 0.2 works with Python3.

Installation
============

.. code-block:: bash

    $ pip install google-scholar-scraper


Command-line usage
==================

.. code-block:: bash

    $ gsscraper "neeman grothendieck duality"


will return the first result from Google Scholar matching this query, in XML
format.

.. code-block:: bash

    $ gsscraper "neeman grothendieck duality" -n 5


will return the five results from Google Scholar matching this query.  (Max is
10 results.)

Library usage
=============

.. code-block:: python

    import gsscraper

    query = "neeman grothendieck duality"
    gsscraper.get_result(query) # (a)
    gsscraper.get_results(query, 5) # (b)
    gsscraper.get_result_as_xml(query) # (c)


Here,

  (a) will return a Python dict with keys "title", "author", etc.;
  (b) will return a list of such Python dicts;
  (c) will return a list of strings in XML format.

License
=======

GPL

Authors
=======

Adeel Khan (@adeel)

Parts of the code are derived from the package `gscholar` by Bastian Venthur
(@venthur).