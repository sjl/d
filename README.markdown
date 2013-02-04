d
=

[Read the docs](http://sjl.bitbucket.org/d/).

os.listdir sorts by inode where a unix ls sort is wanted.  

http://www.znasibov.info/blog/post/inside-python-understanding-os-listdir.html has code to
adapt for a fix.

Fix in base: `os.listdir(src)` becomes `sorted(os.listdir(src))` .



