#!/bin/bash

for f in $(ls -f *.eval);do
  echo $f
  sed -n '/^C[0-9]\+ C[0-9]\+.*/p' $f > tmp
  mv tmp $f
done
