#!/bin/bash
source perf.conf

#queries=("q1.sql")
queries=("q1.sql" "q3.sql" "q6.sql" "q14.sql" "q19.sql")

for query in ${queries[@]}; do
# run bench
echo $query
  echo "${query:0:3}.tab" 
iostat -t 1 > io_results/${query:0:3}_io &
IOPID=$!
  # pre-running
  mysql -u root --password=\!ong\-horn tpch < $1$query > ${query:0:3}.tab
# post-running
kill $IOPID
done

