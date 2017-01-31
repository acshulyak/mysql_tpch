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

 
