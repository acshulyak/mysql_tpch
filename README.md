# mysql_tpch
This project provides the tools necessary to collect a variety of performance metrics on MySQL with the TPC-H benchmark suite. These tests were done with a single-node setup in all cases. In this README, I will detail the steps necessary to recreate my experiments.

#Setup
##Dependencies
###MySQL
Check if you already have MySQL installed and the version:
```
$ mysql --version
```
Follow the instruction found at https://dev.mysql.com/doc/refman/5.7/en/linux-installation-native.html for Ubuntu to install MySQL. Essentiall just do the following:
```
$ sudo apt-get install mysql-client mysql-server
```
Or for a specific version (we used version 5.5.53):
```
$ sudo apt-get install mysql-client-5.5.53 mysql-server-5.5.53
```

##TPC-H Benchmark Suite on MySQL
NOTE: Setting up MySQL requires root access to the server.

clone this repo

cd into the root directory

Prepare MySQL for the tpch database:
```
$ mysql --local-infile=1 -uroot --password=<root-password>
$ ql -u root -p
mysql> CREATE USER 'tpch'@'%' IDENTIFIED BY 'password';
mysql> CREATE DATABASE tpch;
mysql> GRANT ALL ON tpch.* to 'tpch'@'%';
mysql> USE tpch;
mysql> \. tpch/gen/dss.ddl
```

Then, in the gen directories, you can modify the query generator to generate queries that are as close as possible to what you need:

```
cd dbgen
cp makefile.suite makefile
#Modify makefile to use
# CC = gcc, DATABASE=SQLSERVER, MACHINE=LINUX, WORKLOAD=TPCH
#In tpcd.h, SQLSERVER section:
# change #define SET_DBASE "use %s;\n"
# change #define SET_ROWCOUNT "limit %d;\n\n"
# change #define START_TRAN "BEGIN WORK;"
# change #define END_TRAN "COMMIT WORK;"
make
```

Then you can start generating database data at the right scale factor in <#>GB.

```
./dbgen -s <#>
```

And also modify the constraints/indices file so that it's compatible with mysql:

```
# Modify dss.ri
# use a search and replace in order to remove "CONNECT TO TPCD", remove references to "TPCD." and remove the lines "COMMIT WORK;"
```

Then you can load all the data into the databases with

```
mysql -u tpch -p
mysql> use tpch;
mysql> LOAD DATA LOCAL INFILE 'customer.tbl' INTO TABLE CUSTOMER FIELDS TERMINATED BY '|';
# Same with orders, lineitem, nation, partsupp, part, region, supplier
mysql> \. dss.ri
```

You then need to change the case of the table names because the queries use lower-case table names I think whereas the dss.ddl uses upper-case names for the tables:

```
mysql> alter table NATION rename nation;
# Ditto for supplier, region, partsupp, part, orders, lineitem, customer
```

If you still have issues running the queries, please take a look at "mysql_stuff" in the root directory.

#Run
NOTE: corrected_queries and corrected_queries_query_plan only include queries 1, 3, 6, 14, and 19.

Cd into the perf directory and open the run.sh script. The queries variable includes a list of TPC-H queries that will be executed. Once you edit which queries you want to execute run the tests by executing
```
./run.sh ../corrected_queries
```
The results of the queries will be placed in q<#>.tab or q<#>..tab files in the perf directory.
##Query Plan
Cd into the perf directory and open the run.sh script. The queries variable includes a list of TPC-H queries that will be executed. Once you edit which queries you want to execute run the tests by executing
```
./run.sh ../corrected_queries_query_plan
```
The query plans will be placed in q<#>.tab or q<#>..tab files in the perf directory.
##IO
NOTE: I/O collection will give you CPU usage and disk I/O data rates.

Cd into the perf directory.

All perf results files will be placed in the io_results directory. If you desire, you can rename a previous io_results directory to save the previous logs and make a new io_results directory.

Open the run_io.sh script. The queries variable includes a list of TPC-H queries that will be executed. Once you edit which queries you want to execute run the tests by executing
```
./run_io.sh ../corrected_queries
```
##Perf
Cd into the perf directory.

All perf results files will be placed in the perf_results directory. If you desire, you can rename a previous perf_results directory to save the previous logs and make a new perf_results directory.

Open the run.sh script. The queries variable includes a list of TPC-H queries that will be executed. Edit which queries you want to execute.

Open the perf.conf configuration, which includes lists of performance monitoring counters. Select which list to use by renaming it PERF_TESTS. You can also make a custom list of PERF_TESTS. perf.conf also has an INTERVAL variable, which specifies the periodicity of collecting performance data over the course of the test, in milliseconds.

In order to collect the performance counter data on the bulk of MySQL execution, perf must attach to the mysqld process. execute ```pgrep mysqld``` to find the process ID of mysqld. Then execute
```
./run_perf.sh ../corrected_queries <PID>
```
##PIN
Cd into the perf directory and open the run_pin.sh script. The queries variable includes a list of TPC-H queries that will be executed. Edit which query you want to execute. The PIN_CMD found on line 24 includes the full command line to execute to start PIN binary instrumentation. Edit the absolute paths of the directory to match the location of PIN on your own machine. Because the majority of execution spawns from the already runing mysqld process, the PIN_CMD is a standalone command from launching the Hive query. -pid is used to attach to the mysqld process, and -follow_execv is used so Pin is attached to all child processes. For MySQL binary instrumentation, it is recommended to use thread safe Pintools only. You can use any pintool of your choosing. It is necessary to specify an absolute path for all Pintool log and output files because the default relative path is unknown. If you want to collect and instruction trace that can be used on the Runahead Prefetch simulator, please use the Pintool found at https://github.com/acshulyak/trace_gen.

In order to collect the instruction-level data on the bulk of MySQL execution, pin must attach to the mysqld process. run_pin.sh automatically find the mysqld PID.
```
./run_pin.sh ../corrected_queries
```
Depending on the Pintool of choice, and especially with the trace_gen Pintool, and large amount of data will be generated. To avoid filling up all available space on disk, monitor disk space periodically during the recording process with ```df```. If at any time you fill the need to end PIN recording short, do the following:

1. ^cmd\+C on running ./tpch_benchmark_pin.sh script (until it exits entirely), then
2. check that mysqld has restarted, and relaunch the mysqld process if it has not
