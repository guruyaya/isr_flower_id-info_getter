#!/bin/bash

BASE_DIR="data/shrunk"

cd $BASE_DIR

find -maxdepth 2 -type f| while read file
do
  RAND=$(( ( RANDOM % 5 )  + 1 ))
  TO_DIR="train"
  if test $RAND -eq 3;  then
	TO_DIR="val"
  fi
  if test $RAND -eq 4;  then
	TO_DIR="test"
  fi
  mkdir -p `dirname $TO_DIR/$file`
  mv $file $TO_DIR/$file
done

