#!/usr/bin/env bash

rm -rf ./build
~/.virtualenvs/d/bin/python ../bin/d
hg -R ~/src/sjl.bitbucket.org pull -u
rsync --delete -a ./build/ ~/src/sjl.bitbucket.org/d
hg -R ~/src/sjl.bitbucket.org commit -Am 'd: Update site.'
hg -R ~/src/sjl.bitbucket.org push
