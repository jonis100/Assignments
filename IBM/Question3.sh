#!/bin/bash
ls -1 $1 | grep .log > tempfile
for filename in  $(cat tempfile)
do
        lines=$(cat $1/$filename | grep ERROR | wc -l)
        echo $filename"-"$lines 
done
