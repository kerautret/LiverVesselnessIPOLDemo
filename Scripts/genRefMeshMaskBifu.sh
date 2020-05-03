#!/usr/local/bin/bash

NAME_REF=$1
NAME_SUFIX_OUT=$2
MASK=$3

shift
shift
shift

param=$*


for path in ${param}
do
    echo Processing $path
    volMask -i $path/${NAME_REF}.nii -a $path/${MASK}.nii -o  ${path}/${NAME_REF}${NAME_SUFIX_OUT}.nii -m 255 -t double
done

