#!/usr/bin/env bash

rm -rf ./build
~/.virtualenvs/d/bin/python ../bin/d
hg -R ~/src/docs.stevelosh.com pull -u
rsync --delete -a ./build/ ~/src/docs.stevelosh.com/d
hg -R ~/src/docs.stevelosh.com commit -Am 'd: Update site.'
hg -R ~/src/docs.stevelosh.com push
