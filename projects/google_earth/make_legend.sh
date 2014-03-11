#!/bin/bash

# assumes that we have a valid cpt file based on min to max
# with the 9th field in the first record of main block set to L
# and the 9th field in the last record of the main block set to U
# and the 9th field of all other records in the main block missing
#
# useage: make_legend cpt_file_name return_period legendFileName
# where return_period is a string ready for input into the title ie 100 not 100.0  
#
# requires GMT and imageMagick

cpt=$1
retp=$2
legendFileName=$3

#set some GMT parameters
gmtset ANNOT_FONT_SIZE 10p
gmtset LABEL_FONT_SIZE 12p
gmtset TICK_LENGTH 0.0c

#the caption includes the return period
caption="$retp Year Wave Height Exceedance at 100m Depth" 

#use GMT to make the postscript file
#note that psscale can also read the contents of the colour palette
#from stdin
psscale -C$cpt -D6.5/2/9.5/0.5h -B:"$caption":/:metres: -P -S > legend.ps

#use imagemagick to crop, add border and convert to png or jpg
convert legend.ps -trim  -border 2% -bordercolor white ${legendFileName}.png

#clean up
rm legend.ps



