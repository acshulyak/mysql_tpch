#!/bin/bash
source perf.conf

#queries=("q3.sql" "q6.sql" "q14.sql" "q19.sql")
queries=("q3.sql")
for query in ${queries[@]}; do
# run bench
echo $query
I=0
for p_test in ${PERF_TESTS[@]}; do
  echo "Running Terasort Mapreduce: with ${PERF_TESTS[$I]}"
  PERF_T_N=$(echo ${PERF_TESTS[$I]} | sed 's/\:/\\\:/g')
  PERF_T_N=$(echo $PERF_T_N | sed 's/,/-/g')
  PERF_T_N=${PERF_T_N:0:30}
  echo $PERF_T_N
  echo "${query:0:3}.tab" 
  # pre-running
  #$PERF_CMD -a -e ${PERF_TESTS[$I]} -o "$PERF_DIR/mysql_${query}_perf_${PERF_T_N}" -- mysql -u root --password=\!ong\-horn tpch < $1$query > ${query:0:3}.tab
  #$PERF_CMD -p $2 -e ${PERF_TESTS[$I]} -o "$PERF_DIR/mysql_${query}_perf_${PERF_T_N}" -- mysql -u root --password=\!ong\-horn tpch < $1$query > ${query:0:3}.tab
  mysql -u root --password=\!ong\-horn tpch < $1$query > ${query:0:3}.tab
# post-running
  I=$I+1
done
done

