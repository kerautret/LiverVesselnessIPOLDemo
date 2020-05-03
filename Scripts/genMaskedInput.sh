#!/usr/local/bin/bash

NAME_INPUT=$1
MASK_SUFIX=$2
MASK_SRC=$3
COLOR="255 0 0 255"
TEMPDIR=$4
shift
shift
shift
shift 
# param


param=$*

for path in ${param}
do
    echo Processing $path
    itk2vol -i $path/${NAME_INPUT}.nii -o ${TEMPDIR}/${NAME_INPUT}${MASK_SUFIX}.vol --inputMin 0 --inputMax 700  -t double -m  $path/${MASK_SRC}.nii
    vol2itk -i ${TEMPDIR}/${NAME_INPUT}${MASK_SUFIX}.vol -o ${path}/${NAME_INPUT}${MASK_SUFIX}.nii 


done

