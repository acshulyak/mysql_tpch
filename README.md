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
$ mysql --local-infile=1 -uroot --password=\!ong\-horn
$ ql -u root -p
mysql> CREATE USER 'tpch'@'%' IDENTIFIED BY 'password';
mysql> CREATE DATABASE tpch;
mysql> GRANT ALL ON tpch.* to 'tpch'@'%';
mysql> USE tpch;
mysql> \. tpch/gen/dss.ddl
```
  
Then, in the gen directories, you can modify the query generator to generate queries that are as close as possible to what you need:

```
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

Then you can start generating database data at the right scale factor

```
./dbgen -s 1
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

Finally, you can test some of the queries

```
cp dists.dss queries
cd queries
../qgen -c tpch -s 1 1 
```

I think the queries still need to be modified a bit to be compatible. I think queries with a limit may need the semi-colon moved around, the precision indicator during date arithmetic in query 1 may need to be removed, and the method for naming columns in query 13 might need changing.

#Run
##Query Plan
##IO
##Perf
##PIN

 
