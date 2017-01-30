# mysql_tpch
This project provides the tools necessary to collect a variety of performance metrics on MySQL with the TPC-H benchmark suite. These tests were done with a single-node setup in all cases. In this README, I will detail the steps necessary to recreate my experiments.

#Setup
##Dependencies
###MySQL
Check if you already have MySQL installed and the version:
```
mysql --version
```
Follow the instruction found at https://dev.mysql.com/doc/refman/5.7/en/linux-installation-native.html for Ubuntu to install MySQL. Essentiall just do the following:
```
sudo apt-get install mysql-client mysql-server
```
Or for a specific version (we used version 5.5.53):
```
sudo apt-get install mysql-client-5.5.53 mysql-server-5.5.53
```

##TPC-H Benchmark Suite on MySQL
1. clone this repo
2. cd into the root directory
3. Build the database of <#>GB size.
  ```
  
  cd dbgen
  mkdir tables
  cd tables
  ../dbgen -s <#>
  ```

#Run
##Query Plan
##IO
##Perf
##PIN

 
