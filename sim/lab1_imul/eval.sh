#!/bin/bash
arr=(small large lomask himask lohimask sparse ones)
design=(base alt)
> stats.txt
for i in "${arr[@]}"
  do
  for j in "${design[@]}"
      do
      echo "$j design:" >> stats.txt 
      echo "$i dataset:" >> stats.txt
      echo "" >> stats.txt
      ./imul-sim  --impl "$j" --input "$i" --stats >> stats.txt
      echo "" >> stats.txt
  done
done

