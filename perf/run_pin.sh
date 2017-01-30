#!/bin/bash
source perf.conf

PIN_CMD="/home/ashulyak/pin-3.0-76991-gcc-linux/pin -pid $PINID -follow_execv -t /home/ashulyak/pin-3.0-76991-gcc-linux/source/tools/Mix/obj-intel64/mix-mt.so -i -o /home/ashulyak/mysql_tcph/perf/pin_results_q6/mix.out"

#queries=("q1.sql" "q3.sql" "q6.sql" "q14.sql" "q19.sql")
queries=("q3.sql")
for query in ${queries[@]}; do
# run bench
echo $query
I=0
#for p_test in ${PERF_TESTS[@]}; do
  echo "Running Terasort Mapreduce: with ${PERF_TESTS[$I]}"
  PERF_T_N=$(echo ${PERF_TESTS[$I]} | sed 's/\:/\\\:/g')
  PERF_T_N=$(echo $PERF_T_N | sed 's/,/-/g')
  PERF_T_N=${PERF_T_N:0:20}
  echo $PERF_T_N
  echo "${query:0:3}.tab"
  PINID=`pgrep -x mysqld`
  echo "PINID = $PINID"
  #echo "PIN_CMD = $PIN_CMD"
  #$PIN_CMD 
  # /home/ashulyak/pin-3.0-76991-gcc-linux/pin -pid $PINID -follow_execv -t /home/ashulyak/pin-3.0-76991-gcc-linux/source/tools/MemTrace/obj-intel64/insbuffer.so -emit -num_intervals 1 -ins_interval 10000000000 -warmup_ins 10000000000 -snippet_size 1000000000 -smarts -o /tmp/${query}.insbuffer.out
  /home/ashulyak/pin-3.0-76991-gcc-linux/pin -pid $PINID -follow_execv -t /home/ashulyak/pin-3.0-76991-gcc-linux/source/tools/Mix/obj-intel64/mix-mt.so -i -o /tmp/${query}.mix-mt.out

  # pre-running
	echo "here1"
  #$PERF_CMD -a -e ${PERF_TESTS[$I]} -o "$PERF_DIR/mysql_${query}_perf_${PERF_T_N}" -- mysql -u root --password=\!ong\-horn tpch < $1$query > ${query:0:3}.tab
  #$PERF_CMD -p $2 -e ${PERF_TESTS[$I]} -o "$PERF_DIR/mysql_${query}_perf_${PERF_T_N}" -- mysql -u root --password=\!ong\-horn tpch < $1$query > ${query:0:3}.tab
  mysql -u root --password=\!ong\-horn tpch < $1$query > ${query:0:3}.tab
# post-running
  mysqladmin -uroot --password=\!ong\-horn shutdown
  #echo "kill $PINID"
  #kill $PINID
  I=$I+1
#done
done

