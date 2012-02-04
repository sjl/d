Installation
============

You just need Python and `pip`:

    :::bash
    pip install d

You can use `easy_install` if you really want:

    :::bash
    easy_install d

`d` uses Markdown, Pygments, and Pyquery to do some of the heavy lifting.

Troubleshooting
---------------

Some users have reported problems compiling the lxml library on OS X.  If you
get a message that looks like this when installing:

    src/lxml/lxml.etree.c:165674: fatal error: error writing to -: Broken pipe
        compilation terminated.
        lipo: can't open input file: /var/tmp//ccZmfWit.out (No such file or directory)
        error: command 'gcc-4.2' failed with exit status 1

Try running this command and installing again:

    export ARCHFLAGS="-arch i386 -arch x86_64"
