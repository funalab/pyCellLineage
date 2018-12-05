#!/bin/zsh
#          file: arrangeFiles.sh:
#       created: 2018-06-28:
#  last updated: :

if [ $# -ne 1 ]; then
  echo "specify 'Pos0' directory"
  exit
fi

dir405=$1/'405'
dir488=$1/'488'
dirBF=$1/'BF'

echo 'make directory '$dir405'...'
mkdir $dir405
if [ $? -eq 0 ];then
  echo 'done'
else
  echo "directory '405' already exists."
  exit
fi

echo 'make directory '$dir488'...'
mkdir $dir488
if [ $? -eq 0 ];then
  echo 'done'
else
  echo "directory '488' already exists."
  exit
fi

echo 'make directory '$dirBF'...'
mkdir $dirBF
if [ $? -eq 0 ];then
  echo 'done'
else
  echo "directory 'BF' already exists."
  exit
fi

for i in `ls $1 | grep 405`;do
  if [ $i != '405' ];then
    mv $1/$i $dir405
  fi
done

for i in `ls $1 | grep 488`;do
  if [ $i != '488' ];then
    mv $1/$i $dir488
  fi
done

for i in `ls $1 | grep Phase`;do
  if [ $i != 'BF' ];then
    mv $1/$i $dirBF
  fi
done
