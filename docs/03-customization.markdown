Customization
=============

`d` is mostly designed for quick and dirty use.  There are a few customization
options, but if you find yourself wanting more you probably need a different
tool.

[TOC]

Project Title
-------------

`d` tries to intelligently guess your project's title.  You can override it by
creating a `title` file with the title inside.

Page Titles
-----------

`d` takes page titles from the first line of the file, which should be a level
1 Markdown heading.

Page URLs
---------

The URL for each page will be the filename of the page, without an extension.
For example, `usage.markdown` will have a URL of `/usage/`.

There is one exception: if a filename starts with a number and a dash, `d` will
ignore those for the URLs (but will sort on them, so you can use this to reorder
pages).

Footer
------

The contents of the footer are rendered from `footer.markdown`, or left blank if
you don't have it.
