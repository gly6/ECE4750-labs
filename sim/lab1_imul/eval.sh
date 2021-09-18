#!/bin/bash
arr=(small large lomask himask lohimask sparse)
> stats.txt
for i in "${arr[@]}"
do
  echo "$i dataset:" >> stats.txt
  echo "" >> stats.txt
  ./imul-sim  --impl base --input "$i" --stats >> stats.txt
  echo "" >> stats.txt
done

