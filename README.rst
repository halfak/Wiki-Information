A simple utility for extracting information about wikis from a MediaWiki API.

Provides a single utility/library called `wiki_info`.

Run ``./get_wiki_info -h`` for command line options.  You can also import
the library:

.. code-block:: python

    import wiki_info
    
    for wi in wiki_info.get("http://en.wikipedia.org"):
        print wi['wiki']
    
