Usage
=====

`d` is designed to be easy and intuitive to use.  Here's a whirlwind tour that
will get you up and running in five minutes.

[TOC]

Basic Flow
----------

Make a directory for your docs:

    :::bash
    mkdir docs
    cd docs

Write some docs:

    :::bash
    touch index.markdown
    touch installation.markdown
    touch usage.markdown

    vim .

Render your docs:

    :::bash
    d

Copy the output somewhere:

    :::bash
    rsync -d build/ myserver:/var/www/myproject

The Introduction Page
---------------------

The text of the main page (above the table of contents) comes from the
`index.markdown` file.

This page doesn't need a title.  Just write out the text you want to show above
the table of contents.

The Footer
----------

The contents of the footer comes from `footer.markdown`.

Documentation Files
-------------------

There are a few rules to follow when writing docs for use with `d`.  They should
be pretty intuitive once you try them out.

### Extensions

You can use `.markdown`, `.mdown`, or `.md` as the extension for your Markdown
files.  `d` doesn't care.

### Layout

Each Markdown file (other than the introduction and footer) is rendered as
a separate page.

### Page Titles

Every page other than the introduction needs a level 1 heading as the first
line.  It will be used as the title of the page.

If you don't have a level 1 heading as the first line, `d` will try to guess
that page title based on the filename.  It may or may not do a good job.

### Other Headings

There shouldn't be any other level 1 headings.  Levels 2/3/4/5/6 are fine.

### Links

Link to other documents by using their filenames with no extension.

For example: the URL for `usage.markdown` would be `/usage/`.

### Relative URLs

If you're planning on serving these docs at a URL other than `/` you should add
`..` before links to other pages.

For example: the URL for `usage.markdown` would now be `../usage/`.

**Note:** these relative URLs are safe to use even when you're serving the docs
at `/`, so there's no disadvantage to using them other than a bit more typing.

### Tables of Contents

Use `[TOC]` to display a table of contents for the current page, if you want
one.

Example
-------

Here's a sample documentation file to get you started:

    :::markdown
    Installation
    ============

    Here's how to install my project.

    If you just want to see how to use it, take a look at the [samples][] page.

    [samples]: /samples/

    [TOC]

    Linux
    -----

    Use your package manager.

    Windows
    -------

    It depends on what version of Windows you have.

    ### Windows XP

    ...

    ### Windows Vista

    ...

    ### Windows 7

    ...

