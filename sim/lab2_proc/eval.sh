
arr=(vvadd-unopt vvadd-opt cmult bsearch mfilt)
design=(base)
>stats.txt
for i in "${arr[@]}"
 do
 for j in "${design[@]}"
  do
  echo "$j design:" >> stats.txt
  echo "$i function:" >> stats.txt
  echo "" >> stats.txt
  ./proc-sim --impl "$j" --input "$i" --verify --stats >> stats.txt
  echo "" >> stats.txt
  done
done
