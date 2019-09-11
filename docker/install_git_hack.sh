#!/bin/sh

cd /
tar xvf /install/_git_closure.tar
GITBIN=`find /nix/store -path '*bin/git'`
if ! test -x "$GITBIN" ; then
  echo "Git closure doesn't contain git binary. Did you pass --git-hack to ./rundocker.sh? " >&2
  exit 1
fi

ln -s --verbose --force $GITBIN /usr/bin/git

